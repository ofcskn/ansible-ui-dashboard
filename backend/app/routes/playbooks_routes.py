from app.schemas.api_response_schema import APIResponseSchema
from app.services.playbook_service import PlaybookService
from flask import Blueprint, jsonify, request

playbooks_bp = Blueprint("playbooks", __name__, url_prefix="/playbooks")
service = PlaybookService()

@playbooks_bp.route("/list", methods=["GET"])
def get_playbooks():
    playbooks = service.list_playbooks()
    response = APIResponseSchema(success=True, message="Playbooks fetched", data=playbooks, code=200)
    return jsonify(response.to_dict())

@playbooks_bp.route("/run", methods=["POST"])
def execute_playbook():
    data = request.get_json()
    playbook_name = data.get("playbook")
    extra_vars = data.get("params", {})

    if not playbook_name:
        response = APIResponseSchema(success=False, message="Playbook name is required", code=400)
        return jsonify(response.to_dict()), 400

    result = service.run_playbook(playbook_name, extra_vars)
    response = APIResponseSchema(success=True, message="Playbook executed", data=result, code=200)
    return jsonify(response.to_dict())
