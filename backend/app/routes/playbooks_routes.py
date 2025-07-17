from app.schemas.api_response_schema import APIResponseSchema
from app.services.playbook_service import PlaybookService
from app.helpers.yaml_helpers import remove_playbook_file, save_playbook_file
from app.constants import PLAYBOOKS_DIR
from flask import Blueprint, jsonify, request

playbooks_bp = Blueprint("playbooks", __name__, url_prefix="/playbooks")
service = PlaybookService()

@playbooks_bp.route("/list", methods=["GET"])
def get_playbooks():
    playbooks = service.list_playbooks()
    playbooks_data = [playbook.to_dict() for playbook in playbooks]
    response = APIResponseSchema(success=True, message="Playbooks fetched", data=playbooks_data, code=200)
    return jsonify(response.to_dict())

@playbooks_bp.route("/run", methods=["POST"])
def execute_playbook():
    data = request.get_json() or {}
    playbook_name = data.get("playbook")
    extra_vars = data.get("params", {})

    if not playbook_name:
        response = APIResponseSchema(success=False, message="Playbook name is required", code=400)
        return jsonify(response.to_dict()), 400

    result = service.run_playbook(playbook_name, extra_vars)
    response = APIResponseSchema(success=True, message="Playbook executed", data=result, code=200)
    return jsonify(response.to_dict())

@playbooks_bp.route("/manage", methods=["POST"])
def manage_playbook():
    data = request.get_json() or {}
    playbook_id = data.get("id")
    name = data.get("name")
    description = data.get("description")
    filepath = data.get("filepath")
    content = data.get("content")  # YAML content as string

    if not playbook_id:
        # Adding new requires name, description, filepath and content
        if not name or not description or not filepath or not content:
            response = APIResponseSchema(success=False, message="Missing required fields for new playbook", code=400)
            return jsonify(response.to_dict()), 400

        success, error = save_playbook_file(filepath, content)
        if not success:
            response = APIResponseSchema(success=False, message=error, code=500)
            return jsonify(response.to_dict()), 500

        new_playbook = service.add_playbook(name=name, description=description, filepath=filepath)
        response = APIResponseSchema(success=True, message="Playbook added successfully", data=new_playbook.to_dict(), code=201)
        return jsonify(response.to_dict()), 201

    else:
        playbook = service.get_by_id(playbook_id)
        if not playbook:
            response = APIResponseSchema(success=False, message="Playbook not found", code=404)
            return jsonify(response.to_dict()), 404

        if name:
            playbook.name = name
        if description:
            playbook.description = description

        if filepath and content:
            success, error = save_playbook_file(filepath, content)
            if not success:
                response = APIResponseSchema(success=False, message=error, code=500)
                return jsonify(response.to_dict()), 500
            playbook.filepath = filepath

        service.update_playbook(playbook)
        response = APIResponseSchema(success=True, message="Playbook updated successfully", data=playbook.to_dict(), code=200)
        return jsonify(response.to_dict()), 200


@playbooks_bp.route("/delete", methods=["DELETE"])
def delete_playbook():
    data = request.get_json() or {}
    playbook_id = data.get("id")

    if not playbook_id:
        response = APIResponseSchema(success=False, message="Playbook ID is required", code=400)
        return jsonify(response.to_dict()), 400

    playbook = service.get_by_id(playbook_id)
    if not playbook:
        response = APIResponseSchema(success=False, message="Playbook not found", code=404)
        return jsonify(response.to_dict()), 404

    # TODO: Add admin role verification here

    # Delete the playbook file from disk
    filepath = playbook.filepath
    result = remove_playbook_file(filepath)
    if not result.get("success"):
        return APIResponseSchema(success=False, message=f"Error deleting playbook file: {str(result.get('error'))}", code=500)

    # Delete playbook record from DB
    service.delete_playbook(playbook)

    response = APIResponseSchema(success=True, message="Playbook deleted successfully", code=200)
    return jsonify(response.to_dict()), 200
