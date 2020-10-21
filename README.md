Stripped down version of the [official exdown](https://github.com/nschloe/exdown/)

# Usage

```bash
chmod +x exdown.py
./exdown.py [FILES]
```

Automatically send `ocaml` to [utop](https://opam.ocaml.org/packages/utop/)
upon changes to the markdown file:

```
echo file.md | entr -s 'exdown.py file.md | utop -stdin'
```
