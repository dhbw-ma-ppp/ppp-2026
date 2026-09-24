"""Checks run by CI on every pull request.

1. Students may only change files in students/<their-github-login>/exNN/.
2. ruff (lint + format) on the changed Python files and notebooks.
3. pytest in every exercise folder the PR touches.

Run locally (from the repository root) to see what CI will say:

    uv run python .github/scripts/check_pr.py --author <github-login>
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

LINTED_SUFFIXES = {".py", ".ipynb"}
PYTEST_NO_TESTS_COLLECTED = 5


def git_changed_files(base: str, *, include_deleted: bool) -> list[str]:
    diff_filter = [] if include_deleted else ["--diff-filter=d"]
    result = subprocess.run(
        ["git", "diff", "--name-only", *diff_filter, f"{base}...HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def error(message: str) -> None:
    # "::error::" makes GitHub show the message prominently in the PR checks
    print(f"::error::{message}")


def check_paths(changed: list[str], author: str) -> bool:
    allowed = re.compile(rf"^students/{re.escape(author)}/ex\d\d/")
    wrong = [path for path in changed if not allowed.match(path)]
    for path in wrong:
        error(f"{path} is outside your folder. Put your files in students/{author}/exNN/.")
    return not wrong


def check_module_names(files: list[str]) -> bool:
    # tests can only `import` a file whose name is a valid Python name
    wrong = [
        path for path in files if Path(path).suffix == ".py" and not Path(path).stem.isidentifier()
    ]
    for path in wrong:
        error(
            f"{path}: the file name cannot be imported by tests. "
            "Use only letters, digits and underscores, e.g. ex01.py."
        )
    return not wrong


def run_ruff(files: list[str]) -> bool:
    if not files:
        return True
    ok = True
    print(f"\n=== ruff check ({len(files)} files)")
    if subprocess.run(["ruff", "check", *files], check=False).returncode != 0:
        error("ruff check found problems. Run `uv run ruff check --fix <file>` locally.")
        ok = False
    print(f"\n=== ruff format --check ({len(files)} files)")
    if subprocess.run(["ruff", "format", "--check", *files], check=False).returncode != 0:
        error("Files are not formatted. Run `uv run ruff format <file>` locally.")
        ok = False
    return ok


def run_pytest(folders: list[str]) -> bool:
    ok = True
    for folder in folders:
        print(f"\n=== pytest {folder}")
        returncode = subprocess.run(["pytest", folder], check=False).returncode
        if returncode == PYTEST_NO_TESTS_COLLECTED:
            print(f"::warning::No tests found in {folder}.")
        elif returncode != 0:
            error(f"Tests failed in {folder}.")
            ok = False
    return ok


def exercise_folders(files: list[str]) -> list[str]:
    folders = set()
    for path in files:
        match = re.match(r"^(students/[^/]+/ex\d\d)/", path)
        if match and Path(match.group(1)).is_dir():
            folders.add(match.group(1))
    return sorted(folders)


def main() -> int:
    # flush our own output immediately, so it appears in order with ruff's and pytest's
    sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default=os.environ.get("BASE_SHA", "origin/main"))
    parser.add_argument("--author", default=os.environ.get("PR_AUTHOR"))
    args = parser.parse_args()
    if not args.author:
        parser.error("--author (or PR_AUTHOR) is required")

    instructors = os.environ.get("INSTRUCTORS", "").split()
    all_changed = git_changed_files(args.base, include_deleted=True)
    existing = git_changed_files(args.base, include_deleted=False)
    print(f"PR by {args.author}, {len(all_changed)} changed files:")
    for path in all_changed:
        print(f"  {path}")

    ok = True
    if args.author not in instructors:
        ok = check_paths(all_changed, args.author) and ok

    student_files = [path for path in existing if path.startswith("students/")]
    ok = check_module_names(student_files) and ok
    ok = run_ruff([path for path in student_files if Path(path).suffix in LINTED_SUFFIXES]) and ok
    ok = run_pytest(exercise_folders(student_files)) and ok

    print("\nAll checks passed." if ok else "\nSome checks failed, see the errors above.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
