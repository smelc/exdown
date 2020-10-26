Stripped down version of the
[official exdown](https://github.com/nschloe/exdown/). The main difference
is that in this fork,
[exdown.py](https://github.com/smelc/exdown/blob/master/exdown.py)
is a standalone main.

The `exdown.py` scripts extracts code snippets from markdown files.

# Usage

```bash
chmod +x exdown.py
./exdown.py [FILES]
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

# Example: live executing Ocaml markdown snippets

Automatically send `ocaml` snippets to [utop](https://opam.ocaml.org/packages/utop/)
upon changes to the markdown file:

```
echo file.md | entr -s 'exdown.py file.md | utop -stdin'
```
