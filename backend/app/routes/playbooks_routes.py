import os
from threading import Thread
from app.schemas.api_response_schema import APIResponseSchema
from app.services.playbook_service import PlaybookService
from app.helpers.yaml_helpers import is_valid_yaml, remove_old_playbook_file, remove_playbook_file, save_playbook_file
from app.config import Config
from flask import Blueprint, jsonify, request
from app.extensions import redis_client, socketio
from flask_jwt_extended import get_jwt_identity, jwt_required

playbooks_bp = Blueprint("playbooks", __name__, url_prefix="/playbooks")
service = PlaybookService()

@playbooks_bp.route("/list", methods=["GET"])
@jwt_required()
def fetch_playbooks():
    user_id = int(get_jwt_identity())
    playbooks = service.fetch_by_user_id(user_id)
    playbooks_data = [playbook.to_dict() for playbook in playbooks]
    response = APIResponseSchema(success=True, message="Playbooks are fetched", data=playbooks_data, code=200)
    return jsonify(response.to_dict())

@playbooks_bp.route("/get/<int:id>", methods=["GET"])
@jwt_required()
def get_playbook(id):
    user_id = int(get_jwt_identity())
    playbook = service.get_by_id(id)
    if not playbook:
        response = APIResponseSchema(success=False, message="Playbook is not found.", code=404)
    response = APIResponseSchema(success=True, message="Playbook is fetched", data=playbook.to_dict(), code=200)
    return jsonify(response.to_dict())

@playbooks_bp.route("/run", methods=["POST"])
@jwt_required()
def execute_playbook():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    playbook_id = data.get("playbook_id")
    extra_vars = data.get("params", {})

    if not playbook_id:
        return jsonify(APIResponseSchema(False, "Playbook ID is required", 400).to_dict()), 400

    playbook = service.get_by_id(playbook_id)
    if not playbook:
        return jsonify(APIResponseSchema(False, "Playbook not found", 404).to_dict()), 404
    
    if playbook.user_id != user_id:
        return jsonify(APIResponseSchema(False, "No permission to run.", 400).to_dict()), 300

    lock_key = f"playbook:{playbook.id}:running"
    lock_acquired = redis_client.set(lock_key, "running", nx=True, ex=1800)

    if not lock_acquired:
        return jsonify(APIResponseSchema(False, "Playbook is already running", 409).to_dict()), 409

    def background_runner():
        try:
            socketio.emit("playbook_log", {"log": "Playbook started...", "id": playbook.id})

            for line in service.stream_playbook_logs(playbook, extra_vars):
                socketio.emit("playbook_log", {"log": line, "id": playbook.id})

            socketio.emit("playbook_done", {"message": "Playbook finished", "id": playbook.id})
        except Exception as e:
            socketio.emit("playbook_error", {"message": str(e), "id": playbook.id})
        finally:
            redis_client.delete(lock_key)

    thread = Thread(target=background_runner)
    thread.start()

    return jsonify(APIResponseSchema(True, "Playbook is running", code=202).to_dict())

@playbooks_bp.route("/manage", methods=["POST"])
@jwt_required()
def manage_playbook():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    playbook_id = data.get("id")
    name = data.get("name")
    description = data.get("description")
    filepath = data.get("filepath")
    content = data.get("content")  # YAML content as string

    if filepath and content:
        is_valid, error = is_valid_yaml(filepath, content)
        if not is_valid:
            response = APIResponseSchema(success=False, message=error, code=400)
            return jsonify(response.to_dict()), 400

    if not playbook_id:
        # Adding new requires name, description, filepath and content
        if not name or not description or not filepath or not content:
            response = APIResponseSchema(success=False, message="Missing required fields for new playbook", code=400)
            return jsonify(response.to_dict()), 400

        success, error = save_playbook_file(filepath, content)
        if not success:
            response = APIResponseSchema(success=False, message=error, code=500)
            return jsonify(response.to_dict()), 500

        new_playbook = service.add_playbook(name=name, description=description, filepath=filepath, user_id=user_id)
        response = APIResponseSchema(success=True, message="Playbook added successfully", data=new_playbook.to_dict(), code=201)
        return jsonify(response.to_dict()), 201

    else:
        playbook = service.get_by_id(playbook_id)
        old_filepath = playbook.filepath
        if not playbook:
            response = APIResponseSchema(success=False, message="Playbook not found", code=404)
            return jsonify(response.to_dict()), 404
        
        if name:
            playbook.name = name
        if description:
            playbook.description = description
            
            remove_old_playbook_file(old_filepath,filepath)

            success, error = save_playbook_file(filepath, content)
            if not success:
                response = APIResponseSchema(success=False, message=error, code=500)
                return jsonify(response.to_dict()), 500
            playbook.filepath = filepath

        service.update_playbook(playbook)
        response = APIResponseSchema(success=True, message="Playbook updated successfully", data=playbook.to_dict(), code=200)
        return jsonify(response.to_dict()), 200

@playbooks_bp.route("/yaml/get/<int:id>", methods=["GET"])
@jwt_required()
def get_content_of_file(id):
    user_id = int(get_jwt_identity())
    playbook = service.get_by_id(id)
    if not playbook:
        response = APIResponseSchema(success=False, message="Playbook not found", code=404)
        return jsonify(response.to_dict()), 200
    
    if playbook.user_id != user_id:
        return jsonify(APIResponseSchema(False, "No permission to get the content.", 400).to_dict()), 300

    full_path = os.path.join(Config.PLAYBOOKS_DIR, playbook.filepath)
    yaml_content = ""
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            yaml_content = f.read()
    except Exception:
        yaml_content = None 

    response =  APIResponseSchema(success=True, message="Playbook updated successfully", data=yaml_content, code=200)
    return jsonify(response.to_dict()), 200

@playbooks_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_playbook():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    playbook_id = data.get("id")

    if not playbook_id:
        response = APIResponseSchema(success=False, message="Playbook ID is required", code=400)
        return jsonify(response.to_dict()), 400

    playbook = service.get_by_id(playbook_id)
    if not playbook:
        response = APIResponseSchema(success=False, message="Playbook not found", code=404)
        return jsonify(response.to_dict()), 404
    
    if playbook.user_id != user_id:
        return jsonify(APIResponseSchema(False, "No permission to get the content.", 400).to_dict()), 300

    # Delete the playbook file from disk
    filepath = playbook.filepath
    result = remove_playbook_file(filepath)
    if not result.get("success"):
        response = APIResponseSchema(success=False, message=f"Error deleting playbook file: {str(result.get('error'))}", code=500)
        return jsonify(response.to_dict()), 500
        
    # Delete playbook record from DB
    service.delete_playbook(playbook)

    response = APIResponseSchema(success=True, message="Playbook deleted successfully", code=200)
    return jsonify(response.to_dict()), 200
