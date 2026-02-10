# Samsung Vision AI Companion — 모바일 서비스 소개 페이지

Galaxy S25에 최적화된 Samsung TV Vision AI Companion 서비스 소개 모바일 웹앱입니다.

## 데모 앱 다운로드

`index.html` 단일 파일이 Vision AI Companion 데모 앱 전체입니다. 다운로드 후 브라우저에서 바로 실행할 수 있습니다.

### 데모 앱 바로 다운로드

> **[index.html 데모 앱 다운로드](https://raw.githubusercontent.com/roy-so-chae/Test/claude/samsung-vac-mobile-page-BDk20/samsung-vac/index.html)**
>
> 위 링크 클릭 → `Ctrl+S` (PC) 또는 `공유 → 저장` (모바일)으로 저장한 뒤 브라우저에서 열어주세요.

| | 링크 |
|---|---|
| **데모 앱 다운로드 (index.html)** | [index.html](https://raw.githubusercontent.com/roy-so-chae/Test/claude/samsung-vac-mobile-page-BDk20/samsung-vac/index.html) |
| **전체 파일 ZIP 다운로드** | [ZIP 다운로드](https://github.com/roy-so-chae/Test/archive/refs/heads/claude/samsung-vac-mobile-page-BDk20.zip) |
| **GitHub Pages에서 바로 보기** | [https://roy-so-chae.github.io/Test/samsung-vac/](https://roy-so-chae.github.io/Test/samsung-vac/) |

### PWA 전체 파일 (오프라인 지원 시 필요)

| 파일 | 설명 | 다운로드 |
|------|------|----------|
| **index.html** | 데모 앱 본체 | [다운로드](https://raw.githubusercontent.com/roy-so-chae/Test/claude/samsung-vac-mobile-page-BDk20/samsung-vac/index.html) |
| **manifest.json** | PWA 설정 | [다운로드](https://raw.githubusercontent.com/roy-so-chae/Test/claude/samsung-vac-mobile-page-BDk20/samsung-vac/manifest.json) |
| **sw.js** | Service Worker | [다운로드](https://raw.githubusercontent.com/roy-so-chae/Test/claude/samsung-vac-mobile-page-BDk20/samsung-vac/sw.js) |

> `index.html` 하나만 다운로드해도 데모 앱은 완전히 동작합니다. PWA(홈 화면 추가, 오프라인) 기능이 필요한 경우에만 3개 파일을 모두 같은 폴더에 저장하세요.

### Git Clone

```bash
git clone -b claude/samsung-vac-mobile-page-BDk20 https://github.com/roy-so-chae/Test.git
cd Test/samsung-vac
open index.html   # macOS / xdg-open index.html (Linux)
```

---

## 미리보기

> "TV가 당신을 이해합니다"

리모컨의 AI 버튼 하나로 시작되는 멀티 AI 에이전트 경험.
Bixby, Microsoft Copilot, Perplexity가 함께 동작하는 세계 최초 멀티 AI 에이전트 TV 서비스를 소개합니다.

## 페이지 구성

| 섹션 | 설명 |
|------|------|
| Hero | 메인 비주얼 + CTA |
| TV Mockup | 16:9 TV 목업 안에 Vision AI UI 시연 |
| Multi-AI Agents | Bixby, Microsoft Copilot, Perplexity 소개 |
| Vision AI Features | 클릭 투 서치, 생성형 배경화면, 실시간 번역, AI 게이밍 모드, AI Picture, Soccer Mode Pro |
| AI Conversation | 리모컨 AI 버튼 대화 데모 (배우 검색 + SmartThings 조명 제어) |
| Stats | 10개 언어 · 7년 OS 업그레이드 · 4.3억 SmartThings 기기 |
| Smart Care | Pet Care, Family Care, 제스처 컨트롤 |
| Supported Devices | Neo QLED, OLED, Micro RGB, QLED, The Frame 등 |
| How to Use | 3단계 사용 가이드 |
| Languages | 10개 지원 언어 그리드 |
| CTA | 지원 모델 확인 유도 |

## 기술 스택

- **Pure HTML/CSS/JS** — 프레임워크 없음, 빌드 없음
- **PWA** — `manifest.json` + Service Worker로 홈 화면 추가 및 오프라인 지원
- **Galaxy S25 최적화** — FHD+ 2340×1080 (CSS 390px) 뷰포트 기준 반응형
- **120Hz 애니메이션** — `will-change`, `prefers-reduced-motion` 대응
- **Safe Area** — 펀치홀/노치 영역 `env(safe-area-inset-*)` 적용
- **배터리 절약** — 배터리 20% 이하 시 애니메이션 자동 비활성화
- **햅틱 피드백** — 터치 시 `navigator.vibrate` 지원

## 실행 방법

별도 빌드 과정 없이 `index.html`을 브라우저에서 열면 바로 확인할 수 있습니다.

```bash
# 로컬 서버로 실행 (PWA 기능 테스트 시)
npx serve samsung-vac

# 또는 Python
python3 -m http.server 8000 -d samsung-vac
```

Galaxy S25에서 확인하려면 같은 네트워크에서 `http://<IP>:8000`으로 접속하세요.

## 파일 구조

```
samsung-vac/
├── index.html      # 메인 서비스 소개 페이지 (HTML + CSS + JS 단일 파일)
├── manifest.json   # PWA 매니페스트
├── sw.js           # Service Worker (오프라인 캐싱)
└── README.md
```

## 주요 기능 상세

### 멀티 AI 에이전트

| AI | 역할 |
|----|------|
| **Bixby** | 음성 TV 제어 + 시청 맥락 이해 |
| **Microsoft Copilot** | 콘텐츠 관련 정보 검색 + 추천 |
| **Perplexity** | 출처 기반 심층 답변 (Pro 12개월 무료) |

### Vision AI 핵심 기능

- **클릭 투 서치** — 시청 중 한 번의 클릭으로 배우, 장소, 상품 정보 검색
- **생성형 배경화면** — AI가 취향에 맞는 아트워크를 생성하여 TV를 인테리어로 변환
- **실시간 번역** — 6개 언어 실시간 자막 번역
- **AI Picture & Sound** — 콘텐츠와 환경에 맞게 화질/음향 자동 최적화
- **Pet & Family Care** — TV 꺼진 상태에서 반려동물/가족 모니터링 + 모바일 알림

### 지원 모델 (2025년형)

Neo QLED 8K/4K · OLED · Micro RGB · QLED · The Frame Pro · The Frame · The Movingstyle · M7/M8/M9 Monitor

## 참고 자료

- [Samsung Vision AI TV (공식)](https://www.samsung.com/sec/tvs/vision-ai-tv/)
- [Samsung Vision AI 소개](https://www.samsung.com/sec/tvs/smart-tv/samsung-vision-ai/)
- [CES 2025 비전 AI 공개 — Samsung Newsroom](https://news.samsung.com/kr/%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90-ces-2025-%ED%8D%BC%EC%8A%A4%ED%8A%B8%EB%A3%A9%EC%97%90%EC%84%9C-%EC%B4%88%EA%B0%9C%EC%9D%B8%ED%99%94-ai-%EC%8A%A4%ED%81%AC%EB%A6%B0-%EA%B2%BD%ED%97%98%EC%9D%84)

## 라이선스

이 프로젝트는 Samsung Vision AI Companion 서비스의 소개 목적으로 제작된 데모 페이지입니다.
Samsung, Galaxy, Vision AI 등은 Samsung Electronics Co., Ltd.의 상표입니다.
