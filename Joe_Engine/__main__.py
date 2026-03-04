"""
상용화 가능한 다른 행성 탐색 독립 엔진 — CLI.
실행: python -m Joe_Engine   또는  python -m Joe_Engine /path/to/snapshot.json
"""
import json
import sys
from pathlib import Path

# 상위(00_PLANET_LAYER)가 path에 있어야 함
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from Joe_Engine import __version__, assess_planet

DEFAULT_SNAPSHOT = {
    "W_surface": 1e9,
    "W_total": 1.4e9,
    "sigma_plate": 0.1,
    "P_w": 0.5,
    "S_rot": 0.2,
}


def main():
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        if path.exists():
            snap = json.loads(path.read_text())
        else:
            snap = DEFAULT_SNAPSHOT
    else:
        snap = DEFAULT_SNAPSHOT

    print("Joe_Engine (다른 행성 탐색 독립 엔진)", __version__)
    result = assess_planet(snap)
    print("  planet_stress:", result.planet_stress)
    print("  instability: ", result.instability)
    print("  habitability:", result.habitability_label)
    print("  ", result.summary)
    if getattr(result, "config_used", None):
        print("  config_used:", list(result.config_used.keys()))


if __name__ == "__main__":
    main()
