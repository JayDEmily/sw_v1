"""Compatibility entry point: python build.py status | next | accept | run ..."""
import subprocess
import sys
from src.queue import main

if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, FileNotFoundError, subprocess.SubprocessError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        sys.exit(2)
