from pathlib import Path

DEFAULT_DIR_PATH = Path(__file__).parent.resolve() / ".."


def getdefault(data: dict, key, default):
    return default if not data.__contains__(key) else data[key]


def prompt_path(file_name: str):
    return DEFAULT_DIR_PATH / "system_prompts" / file_name


def media_path(file_name: str):
    return DEFAULT_DIR_PATH / "media" / file_name
