#!/usr/bin/env python3
"""
Run an example in the current directory.

Author: Muhammad Mohsin Khan
Date: October 27, 2026
License: MIT
Repository: https://github.com/mkhan138/calculix-fea-examples
"""

from pathlib import Path
import subprocess
import sys


def main():
    # Use the directory from which the command was invoked.
    example_dir = Path.cwd()
    run_file = example_dir / "run.py"

    # Avoid accidentally running the launcher itself.
    launcher_file = Path(__file__).resolve()

    if not run_file.is_file():
        print(
            f"ERROR: No run.py found in {example_dir}",
            file=sys.stderr,
        )
        sys.exit(1)

    if run_file.resolve() == launcher_file:
        print(
            "ERROR: Cannot execute the launcher as an example.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Running example: {example_dir.name}")
    print(f"Directory: {example_dir}")
    print("-" * 60)

    try:
        subprocess.run(
            [sys.executable, str(run_file)],
            cwd=example_dir,
            check=True,
        )
    except subprocess.CalledProcessError as error:
        print(
            f"\nFAILED: Example exited with code {error.returncode}",
            file=sys.stderr,
        )
        sys.exit(error.returncode)


if __name__ == "__main__":
    main()