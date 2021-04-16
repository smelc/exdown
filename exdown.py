#!/usr/bin/python3

import argparse
import subprocess
import tempfile
import sys
from typing import List, Optional, Tuple

PARSER = argparse.ArgumentParser()
PARSER.add_argument("FILE", help="the file to parse", type=str)
PARSER.add_argument(
    "-f",
    "--focus",
    help="the only extension to consider. I.e. if interested in ```ocaml ...``` blocks, pass -f ocaml",
    type=str,
)
PARSER.add_argument(
    "-x",
    "--exec",
    help="command to execute on each snippet (split on spaces)",
    type=str,
)
ARGS = PARSER.parse_args()


def extract(f, *args, **kwargs):
    with open(f, "r") as handle:
        return from_buffer(handle, *args, **kwargs)


def from_buffer(
    f, max_num_lines=10000, focus=None
) -> List[Tuple[str, int, Optional[str]]]:
    """returns the list of snippet. Each snippet comes
    with its starting line number and its extension (if any)"""
    out = []
    previous_line = None
    k = 1

    while True:
        line = f.readline()
        k += 1
        if not line:
            # EOF
            break

        if line.lstrip()[:3] == "```":
            syntax = line.strip()[3:]
            num_leading_spaces = len(line) - len(line.lstrip())
            lineno = k - 1
            # read the block
            code_block = []
            while True:
                line = f.readline()
                k += 1
                if not line:
                    raise RuntimeError("Hit end-of-file prematurely. Syntax error?")
                if k > max_num_lines:
                    raise RuntimeError(
                        f"File too large (> {max_num_lines} lines). Set max_num_lines."
                    )
                # check if end of block
                if line.lstrip()[:3] == "```":
                    break
                # Cut (at most) num_leading_spaces leading spaces
                nls = min(num_leading_spaces, len(line) - len(line.lstrip()))
                line = line[nls:]
                code_block.append(line)

            if focus and focus != syntax.strip():
                continue
            if previous_line and previous_line.strip() == "<!-- exdown-skip -->":
                continue

            out.append(("".join(code_block), lineno, syntax))

        previous_line = line

    return out


def _exec(snippet: str, lineno: int, ext: Optional[str]):
    ext = ("." + ext) if ext else None
    with tempfile.NamedTemporaryFile(prefix="exdown_", suffix=ext) as tmp_file:
        print(snippet)
        tmp_file.write(snippet.encode("utf-8"))
        tmp_file.flush()
        cmd = ARGS.exec.split(" ") + [tmp_file.name]
        # cmd_str = " ".join(cmd)
        # print(f"> {cmd_str}")
        result = subprocess.run(cmd, check=False, stderr=sys.stderr, stdout=sys.stdout)
        rc = result.returncode
        if rc != 0:
            print(f"{ARGS.FILE}:{lineno} exdown snippet ERROR")
            sys.exit(rc)


def main():
    for f in [ARGS.FILE]:
        out = extract(f, focus=ARGS.focus)
        for p in out:
            code_str = p[0]
            if ARGS.exec:
                _exec(code_str, p[1], p[2])
            else:  # print snippet
                print(code_str)


if __name__ == "__main__":
    main()
