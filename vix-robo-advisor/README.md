# VIX 로보 어드바이저

VIX 지수를 기반으로 현금, SPY, QQQ의 포트폴리오 비율을 매주 제공하는 스마트 로보 어드바이저 웹 애플리케이션입니다.

## 주요 기능

- **실시간 시장 데이터**: VIX 지수, SPY, QQQ의 실시간 가격 및 변동률 제공
- **자동 포트폴리오 배분**: VIX 수준에 따른 자동 자산 배분 전략
- **포트폴리오 계산기**: 투자 금액에 따른 상세 포트폴리오 시뮬레이션
- **VIX 히스토리 차트**: 30일 VIX 추이 시각화
- **반응형 웹 디자인**: 모바일, 태블릿, 데스크톱 지원

## 투자 전략

VIX 지수에 따라 4가지 전략을 자동으로 적용합니다:

### 1. 공격적 전략 (VIX < 15)
- 현금: 10%
- SPY: 50%
- QQQ: 40%
- **특징**: 낮은 변동성 환경에서 성장주 중심의 공격적 투자

### 2. 균형 전략 (VIX 15-20)
- 현금: 20%
- SPY: 45%
- QQQ: 35%
- **특징**: 정상 변동성 환경에서 균형잡힌 포트폴리오

### 3. 보수적 전략 (VIX 20-30)
- 현금: 40%
- SPY: 40%
- QQQ: 20%
- **특징**: 높은 변동성 환경에서 안전자산 비중 확대

### 4. 매우 보수적 전략 (VIX > 30)
- 현금: 60%
- SPY: 30%
- QQQ: 10%
- **특징**: 극도의 변동성 환경에서 현금 중심의 방어적 운용

## 설치 및 실행

### 필수 요구사항
- Python 3.8 이상
- pip

### 설치

```bash
# 의존성 설치
pip install -r requirements.txt
```

### 실행

```bash
# Flask 애플리케이션 실행
python app.py
```

애플리케이션이 실행되면 브라우저에서 `http://localhost:5000`으로 접속하세요.

## API 엔드포인트

### 1. 주간 추천 조회
```
GET /api/recommendation
```
현재 VIX 지수 기반 포트폴리오 추천을 반환합니다.

### 2. 시장 데이터 조회
```
GET /api/market-data
```
VIX, SPY, QQQ의 현재 가격 및 변동률을 반환합니다.

### 3. 특정 VIX 값에 대한 배분 조회
```
GET /api/allocation/<vix_value>
```
지정된 VIX 값에 대한 포트폴리오 배분을 반환합니다.

### 4. 포트폴리오 계산
```
POST /api/portfolio-calculator
Content-Type: application/json

{
  "investment": 10000
}
```
투자 금액에 따른 상세 포트폴리오를 계산합니다.

### 5. VIX 히스토리
```
GET /api/vix-history/<days>
```
지정된 기간의 VIX 히스토리 데이터를 반환합니다.

### 6. 헬스 체크
```
GET /health
```
서비스 상태를 확인합니다.

## 프로젝트 구조

```
vix-robo-advisor/
├── app.py                 # Flask 애플리케이션
├── robo_advisor.py        # 로보 어드바이저 핵심 로직
├── requirements.txt       # Python 의존성
├── README.md             # 프로젝트 문서
├── templates/
│   └── index.html        # 메인 웹 페이지
└── static/
    ├── style.css         # 스타일시트
    └── script.js         # 클라이언트 JavaScript
```

## 기술 스택

- **백엔드**: Python, Flask
- **데이터**: yfinance (Yahoo Finance API)
- **프론트엔드**: HTML5, CSS3, JavaScript
- **차트**: Chart.js

## 면책 조항

이 애플리케이션은 교육 및 정보 제공 목적으로만 사용됩니다. 투자 결정을 내리기 전에 전문 재무 고문과 상담하시기 바랍니다. 과거 성과가 미래 결과를 보장하지 않습니다.

## 라이선스

MIT License

## 기여

버그 리포트와 기능 제안을 환영합니다!
