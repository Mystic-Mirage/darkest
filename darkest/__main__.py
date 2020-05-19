from argparse import ArgumentParser
from pathlib import Path

from .format import format_lines
from .lines import read_lines, split_lines, write_lines


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("path", metavar="PATH", type=Path)
    parser.add_argument("--from", type=int, default=1, dest="from_line")
    parser.add_argument("--to", type=int, dest="to_line")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    lines = read_lines(args.path)
    head, body, tail = split_lines(lines, args.from_line, args.to_line)

    formatted = format_lines(args.path, body)

    new_lines = head + [formatted] + tail
    write_lines(args.path, new_lines)


if __name__ == "__main__":
    main()
