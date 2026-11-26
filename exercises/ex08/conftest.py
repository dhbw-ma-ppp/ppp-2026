"""Not part of the AI's code: puts the DWD data file where the AI's app looks for it.

The app reads `weather-service/mannheim.txt` as soon as it is imported. The file is 4.8 MB and
git ignores every copy of it, so in CI (and if you forgot to copy it) this copies it from
exercises/ex07/ before the tests start.
"""

import shutil
from pathlib import Path

DATA_FILE = Path(__file__).parent / "weather-service" / "mannheim.txt"

if not DATA_FILE.exists():
    for folder in Path(__file__).resolve().parents:
        original = folder / "exercises" / "ex07" / "mannheim.txt"
        if original.exists():
            shutil.copy(original, DATA_FILE)
            break
