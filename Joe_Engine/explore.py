# Joe_Engine — 상용화 가능한 다른 행성 탐색 독립 엔진 (API 레이어)
# 입력: 행성 스냅샷 dict / 출력: 거주가능성·불안정도 등 탐색 평가. CookiieBrain 무의존.

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from ._core import (
    DEFAULT_REF_MAX,
    DEFAULT_REF_MIN,
    instability_raw,
    normalize,
    planet_stress_raw,
    saturate,
)


@dataclass(frozen=True)
class PlanetAssessment:
    """다른 행성 탐색 결과: 스트레스·불안정도·거주가능성 라벨."""
    planet_stress: float   # 0~1 정규화
    instability: float    # 0~1
    habitability_label: str  # "low" | "moderate" | "high" | "extreme"
    summary: str


def _label_habit(stress: float, inst: float) -> str:
    if stress >= 0.7 or inst >= 0.7:
        return "extreme"
    if stress >= 0.4 or inst >= 0.4:
        return "low"
    if stress >= 0.2 or inst >= 0.2:
        return "moderate"
    return "high"


def assess_planet(
    snapshot: Dict[str, Any],
    *,
    ref_min: float = DEFAULT_REF_MIN,
    ref_max: float = DEFAULT_REF_MAX,
) -> PlanetAssessment:
    """
    상용화용 진입 API: 행성 스냅샷만 넣으면 탐색·거주가능성 평가 반환.
    다른 행성 탐색 독립 엔진으로 사용.
    """
    raw = planet_stress_raw(snapshot)
    planet_stress = normalize(raw, ref_min=ref_min, ref_max=ref_max)
    inst_raw = instability_raw(planet_stress, snapshot)
    instability = saturate(inst_raw)
    label = _label_habit(planet_stress, instability)
    summary = f"planet_stress={planet_stress:.3f}, instability={instability:.3f}, habitability={label}"
    return PlanetAssessment(
        planet_stress=planet_stress,
        instability=instability,
        habitability_label=label,
        summary=summary,
    )
