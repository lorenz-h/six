import pathlib


def projpath(relative_path: str) -> pathlib.Path:
    return _get_proj_dir() / relative_path


def _get_proj_dir() -> pathlib.Path:
    p = pathlib.Path(__file__)
    return p.parent.parent.resolve()
