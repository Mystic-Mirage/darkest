from argparse import ArgumentParser
from pathlib import Path

from .format import format_file


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("path", metavar="PATH", type=Path)
    parser.add_argument("--from", type=int, default=1, dest="from_line")
    parser.add_argument("--to", type=int, default=-1, dest="to_line")
    parser.add_argument("--config")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    format_file(args.path, args.from_line, args.to_line, args.config)


if __name__ == "__main__":
    main()
