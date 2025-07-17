from app.services.ansible_runner import list_playbooks, run_playbook
from flask import Blueprint, request, jsonify

playbooks_bp = Blueprint('playbooks', __name__, url_prefix="/playbooks")

@playbooks_bp.route("/list", methods=["GET"])
def get_playbooks():
    return jsonify(list_playbooks())

@playbooks_bp.route("/run", methods=["POST"])
def execute_playbook():
    data = request.get_json()
    playbook_name = data.get("playbook")
    extra_vars = data.get("params", {})
    
    if not playbook_name:
        return jsonify({"error": "Playbook name is required"}), 400

    result = run_playbook(playbook_name, extra_vars)
    return jsonify(result)
