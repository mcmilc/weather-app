import json


def load_db_config(db_type="postgresql"):
    """Load database configuration from a JSON file
    based on the selected type (PostgreSQL/MySQL)."""
    with open("config/db_config.json", "r") as config_file:
        config = json.load(config_file)
    if db_type not in config:
        raise ValueError(f"Unsupported database type: {db_type}")
    return config[db_type]


def load_json(file_path):
    """Load JSON data from a given file path."""
    with open(file_path, "r") as json_file:
        return json.load(json_file)
