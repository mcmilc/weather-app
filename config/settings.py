import os
import json


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))


def load_json(file_path):
    """Load JSON data from a given file path."""
    with open(file_path, "r") as json_file:
        return json.load(json_file)


def load_cities():
    """Load city data from a JSON file."""
    return load_json(os.path.join(project_root, "config/cities.json"))["cities"]


def load_db_config(db_type="postgresql"):
    """Load database configuration from a JSON file
    based on the selected type (PostgreSQL/MySQL)."""
    config = load_json(os.path.join(project_root, "config/db_config.json"))
    if db_type not in config:
        raise ValueError(f"Unsupported database type: {db_type}")
    return config[db_type]


def load_query(file_path):
    """Read an SQL query from a file."""
    with open(os.path.join(project_root, file_path), "r") as sql_file:
        return sql_file.read()


def load_weather_format():
    """Load the date range for historical weather extraction."""
    return load_json(os.path.join(project_root, "config/weather_format_config.json"))
