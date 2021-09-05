from pathlib import Path

from darker.__main__ import modify_file
from darker.black_diff import BlackConfig, run_black
from darker.chooser import choose_lines
from darker.diff import diff_and_get_opcodes, opcodes_to_chunks
from darker.utils import TextDocument
from darker.verification import (
    BinarySearch,
    NotEquivalentError,
    verify_ast_unchanged,
)


def format_file(
    src: Path,
    from_line: int,
    to_line: int,
    config: str = None,
):
    black_args = BlackConfig(config=config)
    edited = worktree_content = TextDocument.from_file(src)
    max_context_lines = len(edited.lines)
    minimum_context_lines = BinarySearch(0, max_context_lines + 1)
    edited_linenums = list(range(from_line, to_line + 1))

    while not minimum_context_lines.found:
        formatted = run_black(edited, black_args)
        opcodes = diff_and_get_opcodes(edited, formatted)
        black_chunks = list(opcodes_to_chunks(opcodes, edited, formatted))
        chosen = TextDocument.from_lines(
            choose_lines(black_chunks, edited_linenums),
            encoding=worktree_content.encoding,
            newline=worktree_content.newline,
        )

        try:
            verify_ast_unchanged(edited, chosen, black_chunks, edited_linenums)
        except NotEquivalentError:
            minimum_context_lines.respond(False)
        else:
            minimum_context_lines.respond(True)
            modify_file(src, chosen)
