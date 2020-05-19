# darkest
Apply Black formatting for specified lines

## Install
`pip install git+https://github.com/Mystic-Mirage/darkest.git`

## Setup PyCharm
Add to External Tools:
* Name: `Darkest`
* Program: `<path_to_darkest_script>`
* Arguments: `--from=$SelectionStartLine$ --to=$SelectionEndLine$ $FilePath$`
