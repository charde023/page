---
title: page — INDEX
type: index
generated: 2026-07-27
---
# page
> 지피터스 AI 스터디 강의 보고서·APOM 주간/임시 리포트·회의록·학습노트를 GitHub Pages로 퍼블리시하는 정적 사이트 저장소.

## 무엇인가
`publish-guide-page` 스킬(및 `wisper-page` 워크플로우)이 생성한 HTML 강의 가이드, 주간·임시 리포트, 회의록, 학습노트, APOM 내부 대시보드를 호스팅하는 GitHub Pages 사이트다(`charde023/page`, https://charde023.github.io/page/). 루트 `index.html`은 지피터스 22기 스터디 강의 모음 인덱스이며, 날짜 기반 디렉터리(`2026-02-14-ai-study-onboarding/` ~ `2026-07-17-hair-towel-emotional-design-pc-v3/` 등 48개)에 강의·이벤트별 보고서가 개별 `index.html`로 저장돼 있다.

## APOM 사업 연결
APOM R&D 신청 가이드·벤처 로드맵·분수물총 컨설팅·로지스틱스 팔레트 시안 등 비즈니스 의사결정 보고서가 이 사이트를 통해 팀 공유된다. `reports/weekly`(주간)·`reports/interim`(임시)는 APOM 운영 현황 보고 채널 역할을 한다.

## 주요 구조
| 경로 | 내용 |
|---|---|
| `index.html` | 전체 강의 가이드 모음 인덱스 (사이트 홈) |
| `2026-*/` | 날짜별 강의·이벤트 보고서 (48개, 2026-02-14 ~ 2026-07-17) |
| `apom/index.html` | APOM 내부 전용 페이지 |
| `reports/weekly/` | 주간 리포트 (2026-W22·W23, 각 `report.md` 동봉) |
| `reports/interim/` | 임시 보고서 (2026-07-03-bunsu-order) |
| `회의록/2026-06-02-주간회의-보고방법론/` | 주간 회의 방법론 회의록 |
| `study-anmok/` | 안목훈련 학습노트 발행본 (74개 하위 항목) |
| `study-notes/` | 스터디 학습노트 발행본 (129개 하위 항목) |
| `gpters/index.html` | gpters 관련 페이지 |

## 상태
활성(Active) — GitHub Pages 퍼블리시 사이트 (https://charde023.github.io/page/). 파일 유형: HTML 정적 페이지(빌드 도구 없음). 발행은 대부분 `publish-guide-page` 스킬이 자동 수행(임시 클론 → 커밋·푸시 → 200 확인).

## 관련 폴더
- `~/.claude/skills/publish-guide-page/` — 이 사이트에 md/HTML을 발행하는 워크플로우 스킬
- `wisper-page` — 강의 녹음 전사·보고서 생성 엔진(별도 저장소)
- `~/workspace-apom` 등 — APOM 기획·보고 문서 원천
