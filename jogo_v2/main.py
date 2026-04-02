import sys
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from game.app import HorizontalRacingApp


if __name__ == "__main__":
    raise SystemExit(HorizontalRacingApp().run())
