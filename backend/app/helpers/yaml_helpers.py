import os

from yaml import YAMLError, safe_load
import yaml
from yaml import YAMLError

from app.config import Config

def save_playbook_file(rel_path, yaml_content):
    if not yaml_content:
        return False, "Playbook content missing"
    full_path = os.path.join(Config.PLAYBOOKS_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)
    return True, None

def remove_playbook_file(filepath):
    if filepath:
        full_path = os.path.join(Config.PLAYBOOKS_DIR, filepath)
        try:
            if os.path.exists(full_path):
                os.remove(full_path)
            return {"success": True, "code": 200}
        except Exception as e:
            return {"success": False, "code": 500, "error": e}

def is_valid_yaml(filepath: str, content: str) -> tuple[bool, str]:
    # Check file extension
    if not filepath.endswith((".yaml", ".yml")):
        return False, "Filepath must end with .yaml or .yml"

    try:
        # Try to parse the YAML safely (no object constructors)
        parsed = yaml.safe_load(content)

        # Enforce basic structure like dict or list
        if not isinstance(parsed, (dict, list)):
            return False, "YAML must be a dictionary or list at the top level"

    except YAMLError as e:
        return False, f"Invalid YAML content: {str(e)}"

    return True, "YAML is valid and safe"

def remove_old_playbook_file(old_rel_path: str, new_rel_path: str):
    old_full_path = os.path.join(Config.PLAYBOOKS_DIR, old_rel_path)
    new_full_path = os.path.join(Config.PLAYBOOKS_DIR, new_rel_path)

    if new_full_path != old_full_path and os.path.exists(old_full_path):
        try:
            os.remove(old_full_path)
            return {"success": True, "code": 200}
        except Exception as e:
            return {"success": False, "code": 500, "error": e}

    return {"success": True, "code": 200}
