# Joe_Engine — 상용화 가능한 다른 행성 탐색 독립 엔진. CookiieBrain 무의존.

from __future__ import annotations

from typing import Any, Dict, Tuple

from ._core import (
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
    ref_min: float = DEFAULT_REF_MIN,
    ref_max: float = DEFAULT_REF_MAX,
) -> Tuple[float, float]:
    """스냅샷 → (planet_stress, instability). 저수준 API."""
    raw = planet_stress_raw(snapshot)
    planet_stress = normalize(raw, ref_min=ref_min, ref_max=ref_max)
    inst_raw = instability_raw(planet_stress, snapshot)
    instability = saturate(inst_raw)
    return (planet_stress, instability)


__all__ = [
    "assess_planet",
    "PlanetAssessment",
    "compute_planet_stress_and_instability_from_snapshot",
    "__version__",
]
