import os
from app.constants import PLAYBOOKS_DIR

def save_playbook_file(rel_path, yaml_content):
    if not yaml_content:
        return False, "Playbook content missing"
    full_path = os.path.join(PLAYBOOKS_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)
    return True, None

def remove_playbook_file(filepath):
    if filepath:
        full_path = os.path.join(PLAYBOOKS_DIR, filepath)
        try:
            if os.path.exists(full_path):
                os.remove(full_path)
            return {"success": True, "code": 200}
        except Exception as e:
            return {"success": False, "code": 500, "error": e}
