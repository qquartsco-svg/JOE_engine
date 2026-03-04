# Joe_Engine — 상용화 가능한 다른 행성 탐색 독립 엔진. CookiieBrain 무의존.

from __future__ import annotations

from typing import Any, Dict, Tuple

from ._core import (
    DEFAULT_CONFIG,
    DEFAULT_REF_MAX,
    DEFAULT_REF_MIN,
    instability_raw,
    normalize,
    planet_stress_raw,
    saturate,
)
from .explore import PlanetAssessment, assess_planet

__version__ = "0.1.0"


def compute_planet_stress_and_instability_from_snapshot(
    snapshot: Dict[str, Any],
    *,
    config: None | Dict[str, Any] = None,
    ref_min: float = DEFAULT_REF_MIN,
    ref_max: float = DEFAULT_REF_MAX,
) -> Tuple[float, float]:
    """스냅샷 → (planet_stress, instability). config로 계수 오버라이드 가능."""
    r = assess_planet(snapshot, config=config, ref_min=ref_min, ref_max=ref_max)
    return (r.planet_stress, r.instability)


__all__ = [
    "assess_planet",
    "PlanetAssessment",
    "compute_planet_stress_and_instability_from_snapshot",
    "DEFAULT_CONFIG",
    "__version__",
]
