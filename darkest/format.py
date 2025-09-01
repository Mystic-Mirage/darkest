from pathlib import Path

from darker.__main__ import modify_file
from darker.chooser import choose_lines
from darker.diff import diff_and_get_opcodes, opcodes_to_chunks
from darker.formatters.black_formatter import BlackFormatter
from darker.formatters.formatter_config import BlackCompatibleConfig
from darker.verification import ASTVerifier, BinarySearch
from darkgraylib.utils import TextDocument


def format_file(
    src: Path,
    from_line: int,
    to_line: int,
    config: str = None,
):
    black_config = BlackCompatibleConfig(config=config)
    edited = worktree_content = TextDocument.from_file(src)
    max_context_lines = len(edited.lines)
    minimum_context_lines = BinarySearch(0, max_context_lines + 1)
    edited_line_nums = list(range(from_line, to_line + 1))

    while not minimum_context_lines.found:
        formatter = BlackFormatter()
        formatter.config = black_config
        formatted = formatter.run(edited, src)
        opcodes = diff_and_get_opcodes(edited, formatted)
        black_chunks = list(opcodes_to_chunks(opcodes, edited, formatted))
        chosen = TextDocument.from_lines(
            choose_lines(black_chunks, edited_line_nums),
            encoding=worktree_content.encoding,
            newline=worktree_content.newline,
        )

        if ASTVerifier(edited).is_equivalent_to_baseline(chosen):
            minimum_context_lines.respond(True)
            modify_file(src, chosen)
        else:
            minimum_context_lines.respond(False)
