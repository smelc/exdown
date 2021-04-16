![quality](https://github.com/smelc/exdown/actions/workflows/lint.yml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Stripped down version of the
[official exdown](https://github.com/nschloe/exdown/). The main difference
is that in this fork,
[exdown.py](https://github.com/smelc/exdown/blob/master/exdown.py)
is a standalone main. In addition it supports the following options:

* `-f/--focus` to only consider snippets of the given extension
* `-x/--exec` to execute a command on each snippet

The `exdown.py` scripts extracts code snippets from markdown files.

# Usage

```bash
usage: exdown.py [-h] [-f FOCUS] [-x EXEC] FILE

positional arguments:
  FILE                  the file to parse

optional arguments:
  -h, --help            show this help message and exit
  -f FOCUS, --focus FOCUS
                        the only extension to consider. I.e. if interested in ```ocaml ...``` blocks, pass -f ocaml
  -x EXEC, --exec EXEC  command to execute on each snippet (split on spaces).
```

To ignore a snippet, add the following line before it:

```html
<!-- exdown-skip -->
```

Tip: to run a snippet that is not shown in your output document, put
it in html comments:

```html
    <!-- Load libraries for later snippets
    ```ocaml
    #require "lwt"
    #require "lwt.unix"
    ```
      -->
```

To execute a command on each snippet, use `-x` or `--exec`. For example
to check the syntax of each json snippet in a file, execute
`exdown.py -x 'jq .'`. This will cause each snippet to be written to
a temporary file and `jq . tmp_file` to be executed. If a call fails,
`exdown.py` stops.

## Example: live executing Ocaml markdown snippets

Automatically send `ocaml` snippets to [utop](https://opam.ocaml.org/packages/utop/)
upon changes to the markdown file:

```
echo file.md | entr -s 'exdown.py file.md | utop -stdin'
```

## Example: live checking that json snippets are well-formed

```
echo file.md | entr -s 'exdown.py -x "jq ." file.md'
```
