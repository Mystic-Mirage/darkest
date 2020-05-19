from pathlib import Path
from typing import List

from darker.black_diff import read_black_config
from black import FileMode, format_str


def format_lines(path: Path, lines: List[str]) -> str:
    text = "".join(lines)
    defaults = read_black_config(path, None)
    mode = FileMode(**defaults)
    formatted = format_str(text, mode=mode)
    return formatted
