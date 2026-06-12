---
title: 4주차 실습세션 — 자기소개 페이지 만들고 Vercel로 배포하기
eyebrow: 지피터스 22기 · 끌림 영상 스터디
subtitle: 2026-06-09 라이브 강의 정리본
source: "2026-06-09 [지피터스] 22기 4주차 실습세션.mp4"
description: GitHub 계정 생성부터 Git 설치, 저장소 클론, HTML 자기소개 페이지 작성, Vercel 배포까지 — 코드 한 줄 없이 직접 인터넷에 올리는 4주차 실습 전 과정.
date: 2026-06-09
---

# 4주차 실습세션 — 자기소개 페이지 만들고 Vercel로 배포하기

> 지피터스 22기 · 끌림 영상 스터디 · 2026-06-09 라이브
> 원본: `2026-06-09 [지피터스] 22기 4주차 실습세션.mp4` · 약 1시간 17분

---

## 결론 (TL;DR)

> **GitHub에 저장소를 만들고 GPT로 HTML을 생성한 뒤 Vercel에 배포하면, 코딩 지식 없이 자기소개 페이지가 인터넷에 뜬다. 한 번 연결하면 이후엔 add·commit·push만으로 자동 반영된다.**

### 핵심 흐름 요약

| 단계 | 도구 | 결과 |
|---|---|---|
| 계정 생성 | GitHub.com | 코드 저장소 보유 |
| Git 설치 | Git installer (Windows) / Homebrew (Mac) | 로컬에서 버전 관리 가능 |
| 저장소 생성·클론 | GitHub New → `git clone` | 로컬에 폴더 다운로드 |
| HTML 생성 | GPT로 자기소개 프롬프트 실행 | `index.html` 파일 완성 |
| Git push | `git add · commit · push` | GitHub 저장소에 파일 업로드 |
| 배포 | Vercel Import → Deploy | 공개 URL 발급, 이후 자동 배포 |

### 챙겨야 할 6가지

| # | 메시지 | 한 줄 |
|---|---|---|
| 1 | GitHub = 물류센터, Git = 택배 포장 도구 | 개념을 먼저 잡으면 이후 단계가 헷갈리지 않는다. |
| 2 | 저장소는 Public + README 체크 | Private이면 Vercel 연동 시 권한 문제가 생길 수 있다. |
| 3 | 첫 push 때 인증 팝업이 뜰 수 있다 | 당황하지 말고 브라우저 인증 후 다시 진행한다. |
| 4 | 확장자 `.txt` → `.html` 로 바꾸는 걸 놓치기 쉽다 | 폴더 옵션에서 확장자 표시를 켜고 작업한다. |
| 5 | Vercel 배포는 최초 1회만 설정한다 | 이후 push만 해도 자동으로 새 버전이 배포된다. |
| 6 | Windsurf나 VS Code로 열면 AI 수정이 편하다 | HTML을 직접 고치는 대신 AI에게 자연어로 요청한다. |

---

## 강의는 어떤 내용이었나

2026-06-09 지피터스 22기 4주차 실습세션으로, 강사(cskim4238)가 진행한 라이브 강의다. 스터디 참가자들이 처음으로 자신의 이름이 적힌 웹페이지를 인터넷에 올리는 경험을 목표로 삼았다. GitHub 가입부터 시작해 Git 설치, 저장소 생성과 클론, GPT로 HTML 생성, push, Vercel 배포까지 전 과정을 실시간으로 함께 진행했다.

강사는 당일 업무 계정 잠금과 급조된 저사양 PC라는 악조건에서 실습을 이어갔고, Vercel 로그아웃이 불가능한 상황을 투명하게 공유하면서 진행했다. 강의 후반에는 Git·Vercel 이후 단계인 바이브 코딩 환경(Windsurf, VS Code, Cursor, Claude Code), 워크스페이스 개념, AI 에이전트 팀 구성까지 참고 자료로 소개했다.

| 파트 | 내용 | 특이사항 |
|---|---|---|
| 개요 | 오늘 목표와 Git/GitHub 개념 설명 | "택배 포장 도구 vs 물류센터" 비유 |
| GitHub 가입 | Sign Up, 이메일 가입 | 구글 계정 / 개인 이메일 모두 가능 |
| Git 설치 | Windows installer, macOS Homebrew | 강사는 Windows 환경 시연 |
| Git 초기 설정 | `git config --global` 이름·이메일 설정 | 가입 아이디를 이름으로 사용 권장 |
| 저장소 생성 & 클론 | GitHub New → Public + README → `git clone` | C 드라이브에 클론 |
| HTML 파일 만들기 | GPT로 자기소개 HTML 생성 → index.txt → .html | 확장자 변경이 자주 막히는 포인트 |
| Git push | `git add · commit · push` → GitHub 확인 | 첫 push 시 인증 팝업 발생 가능 |
| Vercel 배포 | Sign Up → Import → Deploy → URL 확인 | Adjust GitHub App Permission 필요 |
| 바이브 코딩 참고 | Windsurf, VS Code, Cursor, Claude Code 소개 | 워크스페이스·AI팀 구성 개념 소개 |
| Q&A | index.html 수정 방법, 편집 도구 추천 | Windsurf 설치 데모 시도 |

---

## 0. 한눈에 보는 자기소개 페이지 배포 흐름

1. GitHub.com에 가입한다 — 이메일 또는 구글 계정 사용 가능.
2. Git을 로컬에 설치한다 — Windows: installer, Mac: Homebrew.
3. `git config --global`로 이름과 이메일을 설정한다.
4. GitHub에서 New Repository를 만든다 — Public + Add README 체크.
5. 터미널에서 `git clone <저장소 주소>`로 로컬에 내려받는다.
6. GPT에 자기소개 정보를 넣어 HTML 코드를 생성한다.
7. 생성된 HTML을 `index.txt`로 저장 후 확장자를 `.html`로 바꾼다.
8. `git add · git commit · git push`로 GitHub에 올린다.
9. Vercel에 GitHub 계정으로 가입한다.
10. Vercel에서 Adjust GitHub App Permission → Import → Deploy한다.
11. 발급된 공개 URL로 자기소개 페이지가 뜨는지 확인한다.

---

## 1. GitHub 계정 만들기

GitHub은 인터넷에 코드를 저장하는 서비스다. Google Drive가 문서를 저장하듯, GitHub은 웹사이트 코드를 저장한다.

> **Git은 택배를 포장하는 도구고, GitHub는 택배를 보관하는 물류센터다.**

GitHub.com에 접속 후 Sign Up을 클릭한다. 구글 이메일로 가입할 수도 있고 개인 이메일로 가입할 수도 있다. 가입할 때 사용한 아이디와 이메일은 이후 Git 초기 설정에서 그대로 사용하므로 기억해 둔다.

---

## 2. Git 설치와 초기 설정

**Git 설치**

| 환경 | 설치 방법 |
|---|---|
| Windows | Git 공식 installer 다운로드 → Next·Next·Install·Finish |
| macOS | Homebrew로 설치 (`brew install git`) |

설치 후 터미널(Windows: Git Bash 또는 PowerShell)에서 아래 명령으로 설치를 확인한다.

```
git --version
```

**초기 설정 — 이름과 이메일 등록**

GitHub 가입 아이디를 이름으로, 가입 이메일을 이메일로 설정한다. 이 값이 이후 commit 기록에 남는다.

```
git config --global user.name "가입한 아이디"
git config --global user.email "가입한 이메일"
```

설정이 잘 됐는지 확인:

```
git config --global user.name
git config --global user.email
```

입력한 값이 그대로 출력되면 성공이다.

---

## 3. 저장소 만들기와 클론

GitHub에 로그인 후 New → Create a new repository를 클릭한다.

| 항목 | 설정값 | 이유 |
|---|---|---|
| Repository name | 자기 아이디 등 원하는 이름 | 나중에 Vercel 연동 시 식별 용도 |
| Visibility | **Public** | Private이면 Vercel 연동이 까다로울 수 있다 |
| Add a README file | **체크** | 빈 저장소 클론 시 오류 방지 |

Create repository를 클릭하면 저장소가 생성된다. 저장소 주소(`.git`으로 끝나는 HTTPS URL)를 복사한다.

터미널에서 C 드라이브로 이동 후 클론한다:

```
cd C:\
git clone <복사한 저장소 주소>
```

C 드라이브에 저장소 이름의 폴더가 생기면 성공이다.

> 클론 중 인증 팝업이 뜨면 브라우저에서 GitHub 계정으로 로그인해 인증한다. 계정이 이미 로그인되어 있으면 자동으로 인증되는 경우도 있다.

---

## 4. HTML 자기소개 페이지 만들기

GPT에 아래 형식으로 자기 정보를 넣어 HTML 코드를 받는다:

- 이름
- 직업 (예: 프리랜서)
- 자기소개 한 줄
- 이메일

GPT가 HTML 코드를 출력하면 전체를 복사한다.

**파일 저장 방법**

1. 클론된 폴더 안에 `index.txt` 파일을 새로 만든다.
2. GPT에서 받은 HTML 코드를 `index.txt`에 붙여넣는다.
3. 파일 이름의 확장자를 `.txt`에서 `.html`로 바꾼다.

> 확장자가 보이지 않으면: 파일 탐색기 상단 메뉴 → 보기 → 파일 이름 확장명 체크.

파일을 더블클릭하면 브라우저에서 자기소개 페이지가 미리 보인다.

---

## 5. GitHub에 올리기 — add·commit·push

클론된 폴더 안에서 아래 명령을 순서대로 실행한다:

```
git add .
git commit -m "자기소개 페이지 추가"
git push
```

| 명령 | 역할 |
|---|---|
| `git add .` | 변경된 파일을 "포장 준비" 상태로 만든다 |
| `git commit -m "..."` | 변경 내용을 설명하며 포장 완료 |
| `git push` | 포장된 파일을 GitHub(물류센터)으로 보낸다 |

GitHub 저장소 페이지를 새로고침하면 `index.html` 파일이 보인다. 파일이 보이면 push가 완료된 것이다.

---

## 6. Vercel로 배포하기

**Vercel 가입**

Vercel.com에서 Sign Up → Continue with GitHub으로 가입한다.

**프로젝트 Import와 Deploy**

1. Vercel 대시보드에서 Add New Project를 클릭한다.
2. 목록에 아까 만든 GitHub 저장소가 보이지 않으면 **Adjust GitHub App Permission** 클릭 → All Repositories 또는 해당 저장소를 선택 → Install.
3. 저장소 옆 **Import** 클릭.
4. 설정을 그대로 두고 **Deploy** 클릭.

배포가 완료되면 공개 URL이 발급된다. 그 URL을 브라우저에서 열면 자기소개 페이지가 인터넷에서 보인다.

> **이후 수정은 추가 Vercel 설정 없이 가능하다.** `index.html`을 수정하고 `git add · commit · push`만 하면 Vercel이 자동으로 새 버전을 배포한다.

---

## 7. 다음 단계 — 바이브 코딩 환경

배포까지 완료됐으면, 이후 페이지를 바꾸거나 새 기능을 추가할 때 추천하는 방법이다.

**편집 도구 선택**

| 도구 | 특징 | 추천 대상 |
|---|---|---|
| Windsurf | AI가 더 많이 알아서 해준다. 코드 편집·미리보기가 통합됨 | 처음 바이브 코딩을 시작하는 사람 |
| VS Code + Claude Code | 세밀한 제어 가능. AI 스킬·에이전트 연동이 풍부함 | 어느 정도 익숙해진 뒤 |
| Cursor | VS Code 기반. AI 코딩 보조 강함 | VS Code에 익숙한 사람 |

**바이브 코딩 흐름**

- 편집 도구에서 클론한 폴더를 연다.
- AI 채팅창에 자연어로 요청한다. 예: "방문자가 이름을 입력하면 안녕하세요 뭐뭐님이라고 인사해주는 기능 추가해줘"
- AI가 코드를 수정해 주면 저장하고, 브라우저에서 미리 확인한다.
- 만족스러우면 `git add · commit · push` → Vercel 자동 배포.

**워크스페이스 개념 (참고)**

자신만의 워크스페이스를 만들어 두면 점차 아래로 발전시킬 수 있다:

1. 기본 — 폴더만 있는 작업 공간
2. 중급 — 자주 쓰는 작업을 커맨드 하나로 묶기
3. 고급 — AI 에이전트 팀 구성 (PM·개발자·코드리뷰어·QA 에이전트를 각각 세팅해 자동으로 돌리기)

---

## 8. 자주 막히는 곳

| 증상 | 대응 |
|---|---|
| GitHub 저장소가 Vercel에 안 보인다 | Adjust GitHub App Permission → Install (해당 저장소 또는 All) |
| `git clone` 후 인증 팝업이 뜬다 | 브라우저에서 GitHub 로그인으로 인증, 완료 후 다시 push 시도 |
| 확장자가 `.txt`로 그대로다 | 파일 탐색기 → 보기 → 파일 이름 확장명 체크 후 이름 변경 |
| `index.html`을 클릭하니 브라우저에 코드가 그대로 보인다 | 파일이 `.html`로 저장됐는지 확인. `.txt`면 확장자 변경 필요 |
| push 후 GitHub에 파일이 안 보인다 | `git add .` → `git commit` 을 다시 확인. commit 없이 push하면 올라가지 않는다 |
| Vercel Deploy 후 URL이 아무것도 안 보인다 | 배포 로그에서 오류 확인. `index.html` 파일명이 정확한지 확인 |
| HTML을 수정했는데 Vercel에 반영이 안 된다 | `git push`가 완료됐는지 확인. Vercel 대시보드에서 새 배포가 시작됐는지 본다 |
| 강사 화면이 잘 안 보인다 | 교재(공유 링크)에 모든 명령어가 복사 가능하게 정리되어 있으므로 교재를 직접 따라간다 |

---

## 부록 — 명대사

> "Git은 택배를 포장하는 도구고, GitHub는 택배를 보관하는 물류센터다." — 강사

> "한 번 이렇게 세팅을 해 놓으시면 다시 Vercel에 들어가서 뭔가 확인하는 작업까지 안 하셔도 자동으로 진행이 됩니다." — 강사

> "처음 하시는 분들은 Windsurf가 편하고요. 개발을 좀 제대로 해보시는 분들은 VS Code를 많이 하세요, Claude Code를 활용해서." — 강사
