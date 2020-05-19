from pathlib import Path
from typing import List, Optional

from black import FileMode, InvalidInput, format_str
from blib2to3.pgen2.tokenize import TokenError
from darker.black_diff import read_black_config

from .lines import read_lines, split_lines, write_lines


def format_file(path: Path, from_line: int, to_line: Optional[int]) -> None:
    lines = read_lines(path)

    length = len(lines) + 1
    begin = from_line - 1
    end = to_line or length

    while end <= length:
        head, body, tail = split_lines(lines, begin, end)

        try:
            formatted = format_lines(path, body)
        except (InvalidInput, TokenError):
            end += 1
            continue

        new_lines = head + [formatted] + tail
        return write_lines(path, new_lines)


def format_lines(path: Path, lines: List[str]) -> str:
    text = "".join(lines)
    defaults = read_black_config(path, None)
    mode = FileMode(**defaults)
    formatted = format_str(text, mode=mode)
    return formatted
