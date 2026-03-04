# JOE Engine — 블록체인·서명 및 검증

## 서명 완료 (Release signing)

- **공식 릴리스**는 GPG 서명된 Git 태그 또는 GitHub Releases를 통해 배포됩니다.
- 태그 검증:  
  `git tag -v v0.1.0`  
  (GPG 공개키가 로컬에 등록되어 있어야 함.)
- GitHub Releases에 올라간 아티팩트(소스 zip/tar.gz)는 설명란에 **SHA-256 체크섬**을 기재합니다. 다운로드 후 아래와 같이 확인할 수 있습니다.

## 체크섬 확인 (예시)

```bash
# Linux/macOS
sha256sum -c joe_engine-v0.1.0.sha256
# 또는
shasum -a 256 -c joe_engine-v0.1.0.sha256
```

`.sha256` 파일 형식 예:

```
<hex>  Joe_Engine-0.1.0.tar.gz
<hex>  Joe_Engine-0.1.0.zip
```

## 재현 가능 빌드

- 이 리포지터리는 **외부 의존성 없음**(표준 라이브러리만 사용).
- 동일 커밋에서 `pip install -e .` 또는 `pip install .` 시 동일 바이트 결과를 기대할 수 있습니다.

## 블록체인·검증 정책

- **서명 완료**: 릴리스 태그 및 Release 아티팩트에 대한 서명·체크섬을 공개하여, 배포본이 공식 소스와 일치함을 검증할 수 있습니다.
- 추가로 블록체인 기반 해시 등록을 사용하는 경우, 해당 해시는 GitHub Release 노트 또는 이 파일에 갱신되어 공개됩니다.
