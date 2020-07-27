from pathlib import Path
from typing import List

from darker.black_diff import BlackArgs, run_black
from darker.chooser import choose_lines
from darker.diff import diff_and_get_opcodes, opcodes_to_chunks
from darker.utils import joinlines
from darker.verification import NotEquivalentError, verify_ast_unchanged


def format_file(
    src: Path, from_line: int, to_line: int, config: str = None,
) -> None:
    while True:
        black_args = BlackArgs(config=config)
        src_contents = src.read_text()
        original = src_contents.splitlines()
        formatted = run_black(src, src_contents, black_args)

        opcodes = diff_and_get_opcodes(original, formatted)
        black_chunks = list(opcodes_to_chunks(opcodes, original, formatted))

        max_line = len(original)
        to_line = (to_line + 1) or max_line
        linenums = list(range(from_line, to_line))

        chosen_lines: List[str] = list(choose_lines(black_chunks, linenums))

        result_str = joinlines(chosen_lines)

        try:
            verify_ast_unchanged(
                src_contents, result_str, black_chunks, linenums
            )
        except NotEquivalentError:
            from_line = max(1, from_line - 1)
            to_line = min(max_line, to_line + 1)
            if from_line == 1 and to_line == max_line:
                raise
            continue

        src.write_text(result_str)
        break
