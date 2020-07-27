from pathlib import Path

from darkest.format import format_file

ORIGINAL = """\
a = [1,2,3,]

b = [5,6,7,]

c = [8,9,0,]
"""

EXPECTED = """\
a = [1,2,3,]

b = [
    5,
    6,
    7,
]

c = [8,9,0,]
"""


def test_fromat_file(tmpdir):
    sample = tmpdir / "sample.py"
    sample.write(ORIGINAL)
    format_file(src=Path(sample), from_line=3, to_line=3)
    result = sample.read()
    assert result == EXPECTED
