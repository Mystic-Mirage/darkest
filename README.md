# darkest
Apply Black formatting for specified lines

## Install
`pip install darkest`

## Setup PyCharm
Add to External Tools:
* Name: `Darkest`
* Program: `<path_to_darkest_script>`
* Arguments: `--from=$SelectionStartLine$ --to=$SelectionEndLine$ $FilePath$`
