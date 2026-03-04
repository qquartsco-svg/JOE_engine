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
| **패키지** | 패키지 디렉터리 `joe_engine/`을 PYTHONPATH에 두거나 `pip install -e .` 후 `python -m joe_engine` 또는 `from joe_engine import assess_planet` 사용 가능. |
| **상용화** | 별도 라이선스로 재배포·상용 제품에 삽입 가능. |

---

## 개념·수식 정리

### 엔진의 정체

- JOE는 **행성 시뮬레이터가 아니다.**  
  중력·탈출속도·회전 안정성 등을 **직접 적분하거나 역산하지 않는다.**
- JOE는 **거시 관찰자/평가기(Observer/Assessor)** 이다.  
  이미 주어진 **표준 스냅샷 6키**를 읽어, **가중 합 두 개**로 stress·instability를 산출하고, 구간별로 **habitability 라벨**을 붙인다.
- 물리량(σ_plate, P_w, S_rot, W_*, dW_norm)은 **호출 측**에서 채우거나, CookiieBrain의 solar/joe **Feature Layer**(물리→스냅샷 변환) 규약을 참고해 구성한다.

### PANGEA §4 수식 (이 패키지에 구현된 유일한 수식)

**(1) 행성 스트레스 (거시 압력 지표)**

```
planet_stress_raw = a1·σ_plate + a2·(P_w / p_ref) + a3·S_rot
                   + a4·(W_surface / W_total) + a5·dW_surface_dt_norm
```

- **예외 처리**: 코드에서는 `W_total ≤ 0`일 때 `W_total = 1`로 대체한다 (0 나눗셈 방지). 즉 `W_total = max(W_total, 1.0)` 적용.
- `ref_min`, `ref_max` 기준으로 선형 정규화 후 [0, 1] 클램프 → **planet_stress**.

**(2) 불안정도 (시스템 붕괴 위험 proxy)**

```
instability_raw = b1·planet_stress + b2·(W_surface / W_total) + b3·dW_surface_dt_norm
```

- 그대로 [0, 1] 포화 → **instability**.

**(3) 기본 계수 (DEFAULT_CONFIG)**

| 키 | 기본값 | 의미 |
|----|--------|------|
| a1, a2, a3, a4, a5 | 0.25, 0.20, 0.20, 0.20, 0.15 | stress_raw 5항 가중치 |
| b1, b2, b3 | 0.60, 0.20, 0.20 | instability_raw 3항 가중치 |
| p_ref | 1.0 | P_w 정규화 기준 |
| ref_min, ref_max | 0.0, 2.0 | stress_raw 정규화 범위 |

- 실행 시 `assess_planet(snapshot, config={...})` 로 오버라이드 가능.  
- 반환값 **PlanetAssessment.config_used**에 실제 사용된 계수가 기록되어 **재현·감사**에 사용한다.

### 스냅샷 6키 (CORE_KEYS)

| 키 | 의미 | 본 패키지에서 계산 여부 |
|----|------|--------------------------|
| **sigma_plate** | 판 구조/텍토닉 활성도 proxy | ❌ 스냅샷에서 읽기만 |
| **P_w** | 내부 유체 압력 proxy | ❌ 스냅샷에서 읽기만 |
| **S_rot** | 자전 관련 무차원 지표 [0,1] | ❌ 스냅샷에서 읽기만. (표준 정의: S_rot = clamp01((ω²R)/g) — 본 패키지는 이 식을 구현하지 않음.) |
| **W_surface** | 표면 수량 (단위 무관) | ❌ 스냅샷에서 읽기만 |
| **W_total** | 총 수량. W_total=0이면 1로 취급 | ❌ 스냅샷에서 읽기만 |
| **dW_surface_dt_norm** | 표면 수량 변화율 정규화 [0,1] | ❌ 스냅샷에서 읽기만 |

→ **견고성**: 키가 없거나 타입이 맞지 않으면 `_get_float`가 기본값 0.0(또는 W_total만 1.0)으로 처리하여 에러 없이 동작한다.

### 거주가능성 라벨 (habitability_label)

- **물리 법칙이 아니라** stress·instability 구간에 따른 **분류 규칙**:
  - `planet_stress ≥ 0.7` 또는 `instability ≥ 0.7` → **extreme**
  - `planet_stress ≥ 0.4` 또는 `instability ≥ 0.4` → **low**
  - `planet_stress ≥ 0.2` 또는 `instability ≥ 0.2` → **moderate**
  - 그 외 → **high**

### CookiieBrain solar/joe와의 관계

- **본 패키지**: PANGEA §4 **Aggregator만** 포함. (스냅샷 → stress, instability, label.)
- **solar/joe**: 동일 Aggregator 위에 **Feature Layer**(00_cosmic, 01_mass_rotation, 02_retention, 03_water_plate_proxy)가 있어, **g=GM/R²**, **v_escape=√(2GM/R)**, **S_rot=clamp01((ω²R)/g)**, **F_star=L/(4πr²)** 등 물리 수식을 계산한 뒤 스냅샷 키를 채워 Aggregator에 넣는 **2단계 파이프라인**을 가진다.
- 독립 엔진은 **스냅샷을 호출 측에서 채우거나**, solar/joe의 `feature_layers.build_joe_snapshot` 규약을 참고해 구성하면 된다.

---

## 설치

이 패키지는 **pyproject.toml을 포함한 표준 Python 패키지 구조**를 사용합니다.

```bash
# 이 리포지터리 클론 후
cd joe_engine
pip install -e .
# 또는 상위에서 (pyproject.toml이 00_PLANET_LAYER에 있는 경우)
cd 00_PLANET_LAYER && pip install -e .
```

---

## 사용 — 탐색 API

```python
from joe_engine import assess_planet, PlanetAssessment, DEFAULT_CONFIG

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
# result.config_used — 사용된 계수 (재현 가능한 리포트)
```

계수 오버라이드 (CONFIG):

```python
result = assess_planet(snap, config={"ref_max": 2.5, "a1": 0.3})
# result.config_used 에 실제 사용된 값 기록됨
```

저수준 API (숫자만 필요할 때):

```python
from joe_engine import compute_planet_stress_and_instability_from_snapshot

stress, inst = compute_planet_stress_and_instability_from_snapshot(snap, config=...)  # config 선택
```

---

## CLI

```bash
python -m joe_engine
# 또는 스냅샷 JSON 파일 경로 전달
python -m joe_engine /path/to/snapshot.json
```

---

## 스냅샷 키

`sigma_plate`, `P_w`, `S_rot`, `W_surface`, `W_total`, `dW_surface_dt_norm` 등. 없으면 0 또는 기본값으로 처리됩니다.

---

## 재현 가능성

- 계수는 `_core.DEFAULT_CONFIG`에 정의되며, `assess_planet(..., config=...)`로 오버라이드 가능.
- 반환값 **PlanetAssessment.config_used**에 실제 사용된 계수가 기록되므로, 동일 결과 재현 및 감사에 사용 가능.

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
joe_engine/
├── __init__.py      # assess_planet, compute_planet_stress_and_instability_from_snapshot, DEFAULT_CONFIG, __version__
├── explore.py       # 행성 탐색 API: assess_planet(snapshot, config=?) → PlanetAssessment
├── _core.py         # PANGEA §4 로직 (planet_stress_raw, instability_raw) + DEFAULT_CONFIG
├── __main__.py      # CLI
├── README.md
├── SIGNATURE.md     # 블록체인·서명 및 검증 안내
├── pyproject.toml  # 표준 Python 패키지 설정 (pip install -e . 에 필요)
└── requirements.txt # (비어 있음 — 표준 라이브러리만 사용)
```

---

## 라이선스

독립 엔진이므로 별도 라이선스로 상용화 가능. 리포지터리 루트의 LICENSE 파일을 확인하세요.

---

## GitHub 업데이트 (배포)

```bash
# 1) JOE_engine 리포지터리 클론 (또는 00_PLANET_LAYER/joe_engine 내용을 JOE_engine 리포에 맞춤)
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
