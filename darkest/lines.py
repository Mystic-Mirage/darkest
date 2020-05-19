from pathlib import Path
from typing import List, Optional, Tuple


def read_lines(path: Path) -> List[str]:
    text = path.read_text()
    lines = text.splitlines(keepends=True)
    return lines


def write_lines(path: Path, lines: List[str]) -> None:
    text = "".join(lines)
    path.write_text(text)


def split_lines(
    lines: List[str], from_line: int, to_line: Optional[int],
) -> Tuple[List[str], List[str], List[str]]:
    begin = from_line - 1
    end = to_line or len(lines)

    head = lines[:begin]
    body = lines[begin:end]
    tail = lines[end:]

    for line in body[:]:
        if line.strip():
            break
        head.append(line)
        body = body[1:]

    for line in reversed(body[:]):
        if line.strip():
            break
        tail.insert(0, line)
        body = body[:-1]

    return head, body, tail
