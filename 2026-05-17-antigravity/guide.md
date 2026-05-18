---
title: Antigravity 설치 가이드
eyebrow: 지피터스 22기 · 끌림 영상 스터디
subtitle: 2026-05-17 라이브 강의 정리본
source: 지피터스-2026-05-17-안티그래비티-설치방법.mp4
description: 지피터스 22기 끌림 영상 스터디 — Antigravity 설치 가이드 (2026-05-17 라이브 정리본)
date: 2026-05-17
---

# Antigravity 설치 가이드

> 지피터스 22기 끌림 영상 스터디 · 2026-05-17 라이브 강의 정리본
> 원본: `지피터스-2026-05-17-안티그래비티-설치방법.mp4` (1시간 56분)

---

## 결론 (TL;DR)

**Google의 AI 코드 에디터 Antigravity로 "AI가 영상을 만드는 환경"을 1회성으로 세팅하는 강의입니다.**
이번 강의에서 만든 환경은 앞으로 4주 동안의 스터디 실습에서 그대로 재사용됩니다.

- **이 페이지 한 장만 따라하면** Windows / Mac 어느 쪽이든 30분~1시간 안에 설치 완료
- **꼭 챙겨야 하는 2가지** ① Python 설치 시 `Add python.exe to PATH` 체크박스 ✅ ② Antigravity Settings에서 `Agent Non-Workspace File Access` ❌ (실제 D드라이브 포맷 사례 있음)
- **설치는 한 번만**, 외울 필요 없음 — 다음 수업부터는 본격 영상 제작 실습

## 강의는 어떤 내용이었나

지피터스 22기 끌림 영상 스터디의 **첫 수업(셋업 세션)**으로, 80명 규모 줌 라이브로 1시간 56분 진행됐습니다.
스터디장은 모든 수강생이 같은 출발선에 서도록 OS별(Windows → Mac) 화면을 두 번 반복하며 다음 6단계를 함께 설치했습니다.

1. **Antigravity** 에디터 다운로드 · 설치
2. **에디터 자동 저장** 설정
3. **Antigravity 안전 설정** (특히 파일 접근 권한 차단)
4. **Node.js** LTS 설치 + 터미널 검증
5. **Python** 3.11~3.14 설치 + PATH 체크
6. **Live Server** VS Code 확장 설치

설치 외에도 (a) Google Ultra 6인 공유 요금제 안내, (b) 부산·서울 오프라인 스터디 안내가 함께 진행됐습니다.

---

## 0. 한눈에 보는 설치 순서

설치는 **이날 한 번만** 해두면 끝. 외울 필요 없습니다. 순서대로 6단계만 따라하면 OK.

1. **Antigravity** (Google이 만든 AI 코드 에디터) 다운로드 & 설치
2. **에디터 세팅** — Auto Save = After Delay
3. **Antigravity 세팅** — 자동 실행 허용 + ⚠️ Workspace 외 파일 접근 차단
4. **Node.js** 설치 (LTS 버전)
5. **Python** 설치 (Windows는 "Add to PATH" 체크 필수)
6. **Live Server** 확장 설치

> 6번까지 끝나면 바이브 코딩 환경 준비 완료입니다.

---

## 1. Antigravity 설치

### 1-1. 다운로드

1. 구글에서 `antigravity` 검색
2. 첫 번째 결과(공식 사이트)로 접속
3. 우측 상단 **Download** 클릭

### 1-2. OS별 설치 파일 선택

| OS | 선택 |
|---|---|
| **Windows** | Windows용 인스톨러 1개만 표시됨 → 그대로 다운로드 |
| **Mac (Apple Silicon)** | M1 / M2 / M3 / M4 / M5 사용자 → **Apple Silicon** 빌드 |
| **Mac (Intel)** | M1 이전 모델 → **Intel** 빌드 |

> 본인 Mac 칩 확인: `Apple 메뉴` → `이 Mac에 관하여` → "칩" 항목

### 1-3. 첫 실행

- 설치 완료 후 실행하면 환영 화면이 나옵니다.
- **Fresh Start** 추천 (기존 설정 가져오지 않고 새로 시작).
- 이후 옵션들(테마, 폰트 등)은 모두 **Next** 눌러 넘겨도 됩니다. 나중에 다 바꿀 수 있습니다.

### 1-4. (Mac만) 보안 권한 허용

설치 후 "허용되지 않은 앱" 같은 메시지가 뜨면:

`시스템 설정` → `개인정보 보호 및 보안` → **Antigravity 허용** 클릭

---

## 2. 에디터 세팅 — Auto Save

좌측 하단 ⚙️(톱니바퀴) → **Editor Settings** → **User** 탭.

- 맨 위 **Auto Save** 항목을 **After Delay** 로 변경

> **왜?** AI가 여러 파일을 동시에 편집하기 때문에 수동 저장을 깜빡하면 작업 내용이 적용되지 않습니다. After Delay는 변경 후 거의 즉시 저장합니다.

> 그 외 폰트, 사이즈 등은 모두 취향. 건드리지 않아도 됩니다.

---

## 3. Antigravity 세팅 (가장 중요한 단계)

같은 ⚙️ 메뉴에서 파란 글씨 **Antigravity Settings** 클릭.

### 3-1. Agent 섹션

| 항목 | 권장 설정 | 이유 |
|---|---|---|
| Stream Mode | **끄기** | 강의 진행에 불필요 |
| Review Polit | **Always** | 매번 확인 안 받고 자동 진행 |
| Terminal Command Auto Execution | **Always** | 터미널 명령도 자동 실행 |
| Artifact (Auto-edit) | **Always** | 코드 수정 자동 반영 |

> Review를 켜고 싶은 분은 코드를 읽을 수 있어야 의미가 있습니다. 안 읽을 거면 Always가 효율적입니다.

### 3-2. ⚠️ File Access — 반드시 끄기

스크롤 내려서 **Agent Non-Workspace File Access** 항목을 찾습니다.

- **이 항목은 무조건 OFF** 로 두세요.

> **왜 꺼야 하나?** 실제로 이 옵션을 켜둔 채 사용하다 **D드라이브가 통째로 포맷된 사례**가 있습니다.
> 켜져 있으면 AI가 현재 작업 폴더 밖의 모든 파일(C, D 드라이브 등)에 접근 가능합니다.
> AI가 "D드라이브를 삭제할까요?"를 영어로 길게 묻는데, 무심코 Yes를 누르면 되돌릴 수 없습니다.
> 끄더라도 작업 폴더 안에서는 자유롭게 동작하므로 실용성에 손해 없습니다.

### 3-3. 추가 권장

- **Terminal Sandbox** → 켜기 (격리 환경에서 명령 실행 → 안전성↑, 약간 느림)
- **Auto Open Edited Files** → 켜기
- **Agent Auto Fix Lint** → 켜기

### 3-4. 사이드 에이전트 패널 열기

`Ctrl + L` (Mac: `⌘ + L`) → 우측에 에이전트 채팅 패널 토글

> 메뉴에서도 가능: `View` → `Toggle Agent`

---

## 4. Node.js 설치

### 4-1. 다운로드

- 공식 사이트: **https://nodejs.org**
- 상단 **Download** 클릭
- **권장 버전: 22.x LTS** 또는 **24.15+ LTS** 중 하나
- 화면에 OS / 칩에 맞는 옵션이 자동 선택됨 (Windows x64, Mac Apple Silicon 등)

> **LTS = Long-Term Support**, 안정 버전. 최신(Current) 버전은 호환성 이슈가 생길 수 있어 권장하지 않습니다.

### 4-2. 설치 검증

Antigravity 에서 터미널 열기:

- 메뉴: `View` → `Terminal` → `New Terminal`
- 단축키: `Ctrl + ` ` (백틱, 1 옆 키)

터미널에 입력:

```
node -v
```

`v22.19.0` 같은 버전 번호가 나오면 성공. 아무것도 안 나오거나 "command not found"면 4-3 참고.

### 4-3. 인식 안 될 때

1. Antigravity를 완전히 종료했다가 다시 실행
2. 그래도 안 되면 PC 재부팅
3. 그래도 안 되면 Node.js를 한 번 더 설치

> 이미 설치되어 있던 분(`v22.05` 이상)은 그대로 사용. 새로 설치할 필요 없습니다.

---

## 5. Python 설치

### 5-1. 다운로드

- 공식 사이트: **https://www.python.org/downloads**
- **권장 버전: 3.12** (3.11 ~ 3.14 사이라면 모두 OK)

> ❌ 2.x 버전(앞이 `2.`)은 **절대 안 됨**
> ❌ 3.6 이하 너무 낮은 버전도 피하세요
> ❌ 너무 최신(릴리스 직후) 버전도 호환성 이슈 가능

### 5-2. 🚨 Windows 사용자 — 가장 중요한 한 가지

설치 마법사 첫 화면 **맨 아래** 에 아주 작게 적힌 체크박스:

```
☑ Add python.exe to PATH
```

**반드시 체크하세요.** 무심코 Next를 빨리 누르면 놓치기 쉽습니다.

> **놓치면 어떻게 되나?** Python이 다운로드 받은 폴더에서만 동작하고, 다른 폴더에서는 명령이 인식되지 않습니다.
> Antigravity 터미널에서 `py --version` 했을 때 인식 안 되는 가장 흔한 원인입니다.

### 5-3. Mac 사용자

Mac은 PATH 체크박스 같은 게 없습니다. 그냥 다운로드 → 설치 → 끝.

### 5-4. 설치 검증

터미널에 입력:

```bash
# Windows
py --version

# Mac
python3 --version
```

`Python 3.12.x` 같은 결과가 나오면 성공.

### 5-5. 안 될 때

- **Windows**: "Add to PATH"를 체크 안 한 것. **재설치하면서 체크박스 켜기**가 가장 빠릅니다.
- **Antigravity 인식 못 함**: 설치 직후 Antigravity를 껐다 다시 켜기.

---

## 6. Live Server 확장 설치

HTML 결과를 브라우저에서 바로 미리보기 위한 필수 확장.

### 6-1. 설치

1. 좌측 사이드바에서 **Extensions** 아이콘 클릭 (블록 4개 모양)
2. 검색창에 **Live Server** 입력
3. 결과 맨 위 항목 클릭 → **Install** 클릭

### 6-2. 사용법 (스터디에서 본격 사용)

HTML 파일을 우클릭 → **Open with Live Server**

> 내 컴퓨터가 그 순간 작은 웹 서버가 되어, 브라우저로 HTML 결과를 실시간으로 확인할 수 있습니다.
> 코드 저장하면 브라우저도 자동 새로고침 — AI가 만든 결과물을 즉시 눈으로 확인 가능.

---

## 7. 마지막 검증 체크리스트

터미널에서 모두 정상 출력되면 설치 완료:

| 명령 (Windows) | 명령 (Mac) | 기대 출력 |
|---|---|---|
| `node -v` | `node -v` | `v22.x.x` |
| `py --version` | `python3 --version` | `Python 3.12.x` (또는 3.11~3.14) |
| Extensions 탭 | Extensions 탭 | Live Server에 **Uninstall** 버튼 표시 |

---

## 8. 자주 막히는 곳 정리

| 증상 | 원인 / 해결 |
|---|---|
| `node -v` 안 됨 | Antigravity 재시작 → 안 되면 재부팅 → 안 되면 Node 재설치 |
| `py --version` 안 됨 (Windows) | Python 설치 시 **Add to PATH** 미체크 → 재설치 |
| Mac에서 "허용되지 않은 앱" | 시스템 설정 → 개인정보 보호 및 보안 → 허용 |
| 사이드 에이전트 패널 안 보임 | `Ctrl/⌘ + L` 또는 `View → Toggle Agent` |
| AI가 자꾸 확인 요청 | Antigravity Settings의 Review/Terminal/Artifact를 **Always** 로 |
| 어두운 테마라 글씨 안 보임 | Editor Settings → Theme → Light 계열 선택 |

---

## 9. 부록 — 강의 중 안내된 부가 정보

- **Google Ultra 6인 공유**: 6명이 묶이면 월 3만원으로 36만원짜리 Ultra 요금제(Veo 영상 무제한 + Nano Banana 등) 사용 가능. 별도 공지로 모집 예정.
- **오프라인 스터디**: 매주 서울 역삼 팁스타운 19:00~. 1주차에 한해 부산역 앞에서도 진행.
- **녹화본**: 지피터스 22기 끌림 영상 스터디 페이지에서 VOD 제공.

---

## 10. 끝맺음

> "설치는 한 번만 하면 됩니다. 외울 필요 없고, 그냥 따라해서 내 컴퓨터에 깔리기만 하면 끝."

여기까지 따라오셨다면, 다음 수업부터 본격적으로 AI 에이전트로 영상 만들기 실습이 진행됩니다.

— *2026-05-17 라이브 정리본*
