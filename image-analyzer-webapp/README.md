# 이미지 분석기 v1.1.0

웹에서 이미지를 불러와 AI가 자동으로 분석하고 설명해주는 모바일 웹앱입니다.

## 주요 기능

- 📸 **이미지 URL 입력**: 웹상의 이미지 URL을 입력하여 이미지를 불러옵니다
- 🔍 **AI 이미지 분석**: Claude AI가 이미지를 자세히 분석하고 설명합니다
- 🖼️ **이미지 미리보기**: 분석 전에 이미지를 미리 확인할 수 있습니다
- 🔐 **자동 API 키 로드**: config.js 파일에서 API 키를 자동으로 불러옵니다
- 💾 **API 키 저장**: 브라우저 localStorage에 API 키를 안전하게 저장합니다
- 📱 **모바일 최적화**: 반응형 디자인으로 모바일에서 편리하게 사용 가능

## 설치 및 설정

### 1. API 키 설정

Claude API 키가 필요합니다. [Anthropic Console](https://console.anthropic.com/)에서 발급받을 수 있습니다.

#### 방법 1: config.js 파일 사용 (권장)

1. `config.example.js` 파일을 `config.js`로 복사합니다:
   ```bash
   cp config.example.js config.js
   ```

2. `config.js` 파일을 열고 API 키를 입력합니다:
   ```javascript
   const CONFIG = {
       CLAUDE_API_KEY: 'sk-ant-api03-your-actual-api-key-here'
   };
   ```

3. 웹앱을 열면 자동으로 API 키가 로드됩니다.

> **보안 참고**: `config.js` 파일은 `.gitignore`에 포함되어 있어 Git에 커밋되지 않습니다.

#### 방법 2: 웹 페이지에서 직접 입력

config.js를 설정하지 않은 경우, 웹 페이지에서 직접 API 키를 입력할 수 있습니다. 입력한 키는 브라우저의 localStorage에 저장됩니다.

### 2. 웹앱 실행

#### 로컬 서버 실행

로컬에서 테스트하려면 간단한 HTTP 서버를 실행하세요:

```bash
# Python 3를 사용하는 경우
python3 -m http.server 8000

# Node.js를 사용하는 경우
npx http-server -p 8000
```

그 다음 브라우저에서 접속:
```
http://localhost:8000/s01.html
```

#### 웹 서버에 업로드

`image-analyzer-webapp` 폴더를 웹 서버에 업로드하고 `s01.html` 파일에 접속하면 됩니다.

## 사용 방법

1. **API 키 확인**: 페이지를 열면 config.js에서 자동으로 API 키가 로드됩니다
   - API 키가 자동으로 로드되면 녹색 메시지가 표시됩니다
   - 자동 로드되지 않으면 직접 입력할 수 있습니다

2. **이미지 URL 입력**: 분석하고 싶은 이미지의 URL을 입력합니다
   ```
   예: https://example.com/image.jpg
   ```

3. **이미지 불러오기**: "이미지 불러오기" 버튼을 클릭하여 이미지를 미리 봅니다

4. **이미지 분석**: "이미지 분석하기" 버튼을 클릭하여 AI 분석을 시작합니다

5. **결과 확인**: AI가 분석한 이미지 설명을 확인합니다

## 파일 구조

```
image-analyzer-webapp/
├── s01.html              # 메인 웹앱 파일
├── config.js             # API 키 설정 파일 (사용자가 생성)
├── config.example.js     # API 키 설정 예제 파일
├── .gitignore           # Git 무시 파일 목록
└── README.md            # 이 문서
```

## 지원 이미지 형식

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)

## 기술 스택

- **HTML5**: 웹 구조
- **CSS3**: 모바일 반응형 디자인
- **JavaScript (Vanilla)**: 클라이언트 사이드 로직
- **Claude API**: AI 이미지 분석
- **Fetch API**: 이미지 로드 및 API 통신

## 주요 디자인 특징

- 🎨 그라디언트 배경 (보라색 계열)
- 🎴 깔끔한 카드 형태의 UI
- 📱 모바일 최적화 (viewport 설정, 터치 친화적)
- ⚡ 로딩 애니메이션
- ⚠️ 사용자 친화적인 오류 메시지

## 보안 고려사항

1. **API 키 관리**:
   - `config.js` 파일은 `.gitignore`에 포함되어 Git에 커밋되지 않습니다
   - localStorage에 저장되는 API 키는 브라우저 내에서만 사용됩니다

2. **CORS 문제**:
   - 일부 이미지 URL은 CORS 정책으로 인해 로드되지 않을 수 있습니다
   - 이 경우 CORS를 허용하는 다른 이미지 URL을 사용하세요

## 버전 히스토리

### v1.1.0 (현재)
- config.js를 통한 자동 API 키 로드 기능 추가
- API 키 입력 필드 개선 (선택적 입력)
- 자동 로드 상태 표시 추가
- 보안 강화 (.gitignore 추가)

### v1.0.0
- 초기 버전 릴리스
- 이미지 URL 입력 및 미리보기
- Claude API를 통한 이미지 분석
- 모바일 반응형 UI
- localStorage를 통한 API 키 저장

## 문제 해결

### Q: API 키가 자동으로 로드되지 않아요
**A**: `config.js` 파일이 올바르게 생성되었는지 확인하세요. `config.example.js`를 복사하고 실제 API 키를 입력해야 합니다.

### Q: 이미지를 불러올 수 없어요
**A**: 다음을 확인하세요:
- 이미지 URL이 올바른지 확인
- 이미지가 실제로 존재하는지 확인
- CORS 정책을 확인 (일부 사이트는 외부 접근을 차단합니다)

### Q: API 오류가 발생해요
**A**: 다음을 확인하세요:
- API 키가 올바른지 확인
- API 크레딧이 충분한지 확인
- 인터넷 연결 상태 확인

### Q: 모바일에서 레이아웃이 이상해요
**A**: 최신 버전의 모바일 브라우저를 사용하고 있는지 확인하세요. Safari, Chrome, Firefox 최신 버전을 권장합니다.

## 라이선스

MIT License

## 개발자

이 웹앱은 Claude Code로 개발되었습니다.

## 기여

버그 리포트나 기능 제안은 GitHub Issues를 통해 제출해주세요.

---

**참고**: 이 앱은 Claude API를 사용하므로 API 사용량에 따라 요금이 부과될 수 있습니다. [Anthropic 가격 정책](https://www.anthropic.com/pricing)을 확인하세요.
