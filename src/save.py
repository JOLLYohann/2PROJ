import json
import os

from src.level import find_level


def _save_path():
    project_root = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(project_root, "cache", "save.json")


def load_save():
    with open(_save_path(), encoding="utf-8") as file:
        return json.load(file)


def write_save(data):
    with open(_save_path(), "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def set_save(level_id):
    data = load_save()
    player_level = data["player"]["level"]

    level_ids = sorted(find_level().keys())
    if level_id not in level_ids:
        return

    position = level_ids.index(level_id) + 1

    if position == player_level:
        data["player"]["level"] += 1
        write_save(data)