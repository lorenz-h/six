import pathlib
import platform
import logging

def projpath(relative_path: str) -> pathlib.Path:
    return _get_proj_dir() / relative_path


def _get_proj_dir() -> pathlib.Path:
    p = pathlib.Path(__file__)
    return p.parent.parent.resolve()

def check_platform_compatibility():
    assert "linux" in platform.system().lower(), "Invalid Platform: Must be Unix"
    logging.debug(f"Detected platform {platform.system()}")

