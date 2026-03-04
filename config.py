import json

def load_config(config_file='config.json'):
    """Load JSON config from file."""
    with open(config_file, 'r') as f:
        return json.load(f)

