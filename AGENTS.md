# AGENTS.md
> 이 레포의 문서·커밋은 한국어. 같은 톤으로 작업한다.
> 표준 → 스킬 `cha-proj-init`(체급 S). 지침 SSOT는 이 파일. `CLAUDE.md`는 `@AGENTS.md` 한 줄.

## 무엇인가
GitHub Pages 발행 전용 정적 사이트 저장소(`charde023/page`, public, branch `main`, root에서 서빙 → https://charde023.github.io/page/). 지피터스 AI 스터디 강의 보고서, APOM 주간·임시 리포트, 회의록, 학습노트(`study-notes/`, `study-anmok/`)를 날짜/슬러그 폴더 단위의 자체완결형 HTML로 호스팅한다. 루트 `index.html`이 전체 강의 모음 홈이다.
- 스택: 정적 HTML/CSS(빌드 파이프라인 없음, Pretendard 웹폰트 CDN 로드).

## 명령어
```bash
open index.html           # 로컬에서 홈(강의 모음) 미리보기
git push origin main       # 커밋을 GitHub Pages에 반영(수 분 내 자동 빌드·배포)
```

## 컨벤션
- **발행은 대부분 `publish-guide-page` 스킬**(`~/.claude/skills/publish-guide-page/`)이 수행한다 — md를 자체완결형 HTML로 변환 → `charde023/page`를 임시 클론 → `YYYY-MM-DD-<영문-슬러그>/index.html`로 커밋·푸시 → URL 200 확인까지 자동. 이 로컬 체크아웃(`/Users/charde023/workspace/page`)에서 직접 커밋할 때도 같은 폴더 명명 규칙을 따른다.
- 폴더명은 `YYYY-MM-DD-<영문-슬러그>/`, 파일은 `index.html` 고정 — 한글 파일명은 URL 인코딩이 깨지기 쉽다(기존 `회의록/` 하위 한글 폴더는 과거 관례로 유지, 신규엔 적용 안 함).
- 이 저장소는 **공개(public)**다 — 민감 자료 폴더 전체를 올리지 않고, 공유 가능한 내용만 자체완결 HTML 한 장으로 올린다.
- 콘텐츠 원천 구분: `apom/`=APOM 내부 전용 페이지, `reports/weekly|interim`=주간·임시 리포트(원본 md 동봉), `회의록/`=회의 정리, `study-notes/`·`study-anmok/`=학습노트 발행본, `gpters/`=gpters 관련 페이지, 그 외 `YYYY-MM-DD-*/`=강의·이벤트별 보고서.

## 불변식·금지
- 루트 `index.html`(강의 모음 인덱스)의 기존 링크 목록을 삭제·재배열하지 않는다 — 새 강의는 추가만, 링크만 아는 사람이 접근하는 개별 폴더 URL 패턴을 깨지 않는다.
- 새 발행 폴더는 항상 영문 슬러그 + `index.html` — 한글 폴더/파일명 신규 생성 금지.

## 완료의 정의(DoD)·검증
- 완료 = 커밋 후 `git push origin main` 반영 + 해당 URL(`https://charde023.github.io/page/<폴더>/`)이 200 응답. "커밋만 했다"는 인정 안 함.

## 문서 지도
- 폴더 지도·상태: [INDEX.md](INDEX.md)
- 발행 워크플로우 정본: `~/.claude/skills/publish-guide-page/SKILL.md`
- 콘텐츠 생성 엔진(강의 보고서 등): `wisper-page`(별도 저장소)
