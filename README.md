# Google 최신 동향 검색기

실시간 Google 인기 검색어를 한눈에 확인할 수 있는 웹앱입니다.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 주요 기능

- **실시간 트렌드 수집** - Google Trends RSS 피드에서 각 국가별 인기 검색어를 실시간으로 가져옵니다
- **15개 지역 지원** - 한국, 미국, 일본, 영국, 독일, 프랑스 등 주요 국가 지원
- **관련 뉴스 표시** - 각 트렌드의 관련 뉴스 기사와 썸네일 이미지를 함께 표시
- **검색량 확인** - 각 키워드의 대략적인 검색량을 확인 가능
- **API 키 불필요** - 별도의 설정 없이 바로 사용 가능
- **단일 HTML 파일** - 의존성 없이 브라우저에서 바로 실행

## 지원 지역

| 지역 | 코드 | 지역 | 코드 |
|------|------|------|------|
| 한국 | KR | 캐나다 | CA |
| 미국 | US | 대만 | TW |
| 일본 | JP | 이탈리아 | IT |
| 영국 | GB | 스페인 | ES |
| 독일 | DE | 멕시코 | MX |
| 프랑스 | FR | 러시아 | RU |
| 인도 | IN | 호주 | AU |
| 브라질 | BR | | |

## 사용법

1. `google-trends-threat-webapp/index.html` 파일을 브라우저에서 엽니다
2. 드롭다운에서 원하는 지역을 선택합니다
3. **검색** 버튼을 클릭합니다
4. 인기 검색어 목록이 순위별로 표시됩니다
5. 각 항목을 클릭하면 관련 뉴스 기사를 볼 수 있습니다

## 다운로드

[**웹앱 다운로드 페이지**](https://roy-so-chae.github.io/Test/)에서 직접 다운로드하거나 미리보기를 확인할 수 있습니다.

또는 직접 파일을 다운로드:
```bash
curl -O https://raw.githubusercontent.com/roy-so-chae/Test/main/google-trends-threat-webapp/index.html
```

## 기술 스택

- **HTML5** - 시맨틱 마크업
- **CSS3** - 반응형 디자인, CSS 변수
- **JavaScript (ES6+)** - Fetch API, DOM 조작
- **Google Trends RSS** - 실시간 트렌드 데이터

## 라이선스

MIT License - 자유롭게 사용, 수정, 배포할 수 있습니다.
