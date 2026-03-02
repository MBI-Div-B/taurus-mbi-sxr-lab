# core/utils.py

import yaml
from pathlib import Path

def load_yaml(path):
    """Load YAML file and return as a Python dictionary.
    """
    yaml_path = Path(path)
    if not yaml_path.exists():
        raise FileNotFoundError(f'YAML config not found: {path}')
    
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    
    return data

def select_attributes(lab_attrs, display_names):
    """Return only attributes that should be displayed for this screen"""
    return [attr for attr in lab_attrs if attr['name'] in display_names]