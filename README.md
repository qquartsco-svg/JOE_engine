# JOE Engine — 완전 독립 행성 탐색 엔진

**Macro Observer · Pre-Creation Phase · PANGEA §4**

조(JOE) 엔진은 **천지창조 1일 이전** — 행성이 형성되기 전 거시적 조건을 탐색하는 독립 엔진입니다.  
CookiieBrain·solar·기타 프로젝트에 **의존하지 않으며**, 다른 행성·외계 환경 탐색·거주가능성 평가에 그대로 쓸 수 있는 **상용화 가능한 단일 패키지**입니다.

---

## 서사적 위치 (Narrative)

- **시점**: Creation Day 0 이전 (Pre-Genesis). 빛이 있기 전, 궤도와 질량·물·판 구조가 정해지는 단계.
- **역할**: Macro Observer — 행성 스냅샷만으로 **planet_stress**(행성 스트레스)와 **instability**(불안정도)를 산출하고, 거주가능성 라벨을 부여.
- **수식**: PANGEA §4 (판·물·자전·수순환 가중 합 → 정규화·포화).
- **출처**: CookiieBrain/solar 레이어에서 유래했으나, **현재 이 리포지터리는 독립 배포용**이며 서사·설계만 공유합니다.

---

## 완전 독립 모델

| 항목 | 내용 |
|------|------|
| **의존성** | 표준 라이브러리만 사용. `requirements.txt` 없음(또는 빈 파일). |
| **패키지** | 단일 디렉터리 `Joe_Engine/` — 복사만 하면 어디서든 `python -m Joe_Engine` 또는 `from Joe_Engine import assess_planet` 사용 가능. |
| **상용화** | 별도 라이선스로 재배포·상용 제품에 삽입 가능. |

---

## 설치

```bash
# 이 리포지터리 클론 후
cd Joe_Engine
pip install -e .
# 또는 상위에서 (pyproject.toml이 00_PLANET_LAYER에 있는 경우)
cd 00_PLANET_LAYER && pip install -e .
```

---

## 사용 — 탐색 API

```python
from Joe_Engine import assess_planet, PlanetAssessment

snap = {
    "W_surface": 1e9,
    "W_total": 1.4e9,
    "sigma_plate": 0.1,
    "P_w": 0.5,
    "S_rot": 0.0,
    "dW_surface_dt_norm": 0.0,
}
result = assess_planet(snap)
# result.planet_stress, result.instability, result.habitability_label, result.summary
```

저수준 API (숫자만 필요할 때):

```python
from Joe_Engine import compute_planet_stress_and_instability_from_snapshot

stress, inst = compute_planet_stress_and_instability_from_snapshot(snap)
```

---

## CLI

```bash
python -m Joe_Engine
# 또는 스냅샷 JSON 파일 경로 전달
python -m Joe_Engine /path/to/snapshot.json
```

---

## 스냅샷 키

`sigma_plate`, `P_w`, `S_rot`, `W_surface`, `W_total`, `dW_surface_dt_norm` 등. 없으면 0 또는 기본값으로 처리됩니다.

---

## 블록체인·서명 및 검증

- **릴리스 검증**: 공식 릴리스는 서명된 Git 태그로 배포됩니다.  
  `git tag -v v0.1.0` (GPG 서명된 태그) 또는 GitHub Releases의 체크섬으로 무결성 확인을 권장합니다.
- **서명 완료**: 배포 아티팩트(소스 트리 또는 압축체)에 대한 체크섬·서명 정보는 [SIGNATURE.md](./SIGNATURE.md) 및 GitHub Releases 설명에 기재됩니다.
- **재현 가능 빌드**: 동일 커밋에서 `pip install -e .` 시 의존성 없음으로 동일 결과를 기대할 수 있습니다.

자세한 검증 절차는 [SIGNATURE.md](./SIGNATURE.md) 참고.

---

## 폴더 구조

```
Joe_Engine/
├── __init__.py      # assess_planet, compute_planet_stress_and_instability_from_snapshot, __version__
├── explore.py       # 행성 탐색 API: assess_planet(snapshot) → PlanetAssessment
├── _core.py         # PANGEA §4 로직 (planet_stress_raw, instability_raw 등)
├── __main__.py      # CLI
├── README.md
├── SIGNATURE.md     # 블록체인·서명 및 검증 안내
└── requirements.txt # (비어 있음 — 표준 라이브러리만 사용)
```

---

## 라이선스

독립 엔진이므로 별도 라이선스로 상용화 가능. 리포지터리 루트의 LICENSE 파일을 확인하세요.

---

## GitHub 업데이트 (배포)

```bash
# 1) JOE_engine 리포지터리 클론 (또는 00_PLANET_LAYER/Joe_Engine 내용을 JOE_engine 리포에 맞춤)
git clone https://github.com/qquartsco-svg/JOE_engine.git
cd JOE_engine

# 2) 이 README·SIGNATURE.md 등 최신 내용 반영 후
git add .
git commit -m "docs: README 서사·블록체인 서명 안내, 완전 독립 모델 명시"
git tag -s v0.1.0 -m "JOE Engine v0.1.0 — 완전 독립 행성 탐색 엔진"   # GPG 서명 태그
git push origin main
git push origin v0.1.0
```

GPG 서명 없이 태그만 달려면 `git tag -a v0.1.0 -m "..."` 후 `git push origin v0.1.0`.
