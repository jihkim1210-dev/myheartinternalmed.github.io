# 내마음내과 홈페이지 (myheartinternalmed.kr)

정적 HTML 사이트. 빌드 도구 없이 Vercel에 그대로 올리면 됩니다.

- 병원 정보(전화, 주소, 진료시간 등)는 `build.py` 위쪽 `CLINIC`, `HOURS` 에서 고칩니다.
- 고친 뒤 `python3 build.py` 를 실행하면 `*.html` 이 다시 만들어집니다.
- 노란색 `확인 필요` 표시는 아직 확인되지 않은 정보입니다. 공개 전에 모두 채워야 합니다.

## Vercel 배포
1. 이 폴더 전체를 Vercel 프로젝트에 연결된 GitHub 저장소에 올립니다.
2. Vercel 설정: Framework Preset `Other`, Build Command 비움, Output Directory 비움(루트).
3. 도메인 `myheartinternalmed.kr` 은 이미 Vercel에 추가되어 있고, DNS(A @ 216.198.79.1)는 hosting.kr 에 설정되어 있습니다.
