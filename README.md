# 🖼️ 배경 회색 → 흰색 변환기

이미지(PNG, JPG, WEBP)의 회색 배경을 깔끔한 흰색으로 자동 변환하는 데스크톱 앱입니다.

> Flood-fill 방식으로 **이미지 가장자리에서 연결된 배경만** 흰색으로 바꿉니다.
> 제품 본체의 회색은 건드리지 않고, 바닥 음영(3D 그림자)만 정확히 처리합니다.

---

## 📥 다운로드

### Windows .exe (바로 실행)

> **[⬇ GrayToWhite.exe 다운로드](https://github.com/roy-so-chae/Test/releases/latest/download/GrayToWhite.exe)**
>
> 설치 없이 더블클릭만으로 바로 사용할 수 있습니다.

### Python으로 직접 실행 (Windows / Mac / Linux)

```bash
git clone https://github.com/roy-so-chae/Test.git
cd Test/image-analyzer-webapp
pip install Pillow numpy scipy
python gray_to_white.py
```

### 웹 버전 (브라우저에서 사용)

| 방법 | 링크 |
|------|------|
| **HTML 직접 다운로드** | [⬇ gray-to-white.html](https://github.com/roy-so-chae/Test/raw/claude/gray-to-white-background-az1yC/image-analyzer-webapp/gray-to-white.html) (우클릭 → 다른 이름으로 저장) |
| **ZIP 전체 다운로드** | [⬇ ZIP 다운로드](https://github.com/roy-so-chae/Test/archive/refs/heads/claude/gray-to-white-background-az1yC.zip) |

---

## ✨ 주요 기능

| 기능 | 설명 |
|------|------|
| **Flood-fill 배경 감지** | 가장자리에서 연결된 회색만 변환 — 제품 본체는 보존 |
| **바닥 음영 처리** | 3D 촬영의 그라데이션 그림자도 함께 제거 |
| **파일/폴더 열기** | 개별 파일 또는 폴더 단위 일괄 처리 |
| **밝기 범위 조절** | 회색으로 판단할 밝기 구간 설정 (기본: 80~245) |
| **채도 허용치** | 약간 색이 있는 배경도 포함 가능 (기본: 35) |
| **경계 부드럽게** | 배경↔제품 경계를 자연스럽게 블렌딩 (기본: 15) |
| **저장 형식** | PNG / JPG / WebP 선택 |
| **원본 vs 결과 미리보기** | 나란히 비교 확인 |

---

## 🔧 사용 방법

1. **파일 열기** 또는 **폴더 열기**로 이미지 선택
2. **슬라이더 조절** — 회색 밝기 범위, 채도 허용치, 경계 부드러움 설정
3. **변환하기** 클릭 — 배경만 흰색으로 변환
4. **저장하기** — 원하는 형식으로 저장

---

## 🎯 활용 예시

- 제품 사진의 회색 배경 + 바닥 음영 제거
- 쇼핑몰 상품 이미지 배경을 흰색으로 통일
- 스캔 문서의 회색 배경 정리
- 프레젠테이션용 이미지 배경 보정

---

## ⚙️ 기술 스택

- **Python + Tkinter** — 크로스 플랫폼 데스크톱 GUI
- **Pillow / NumPy** — 이미지 로드 및 픽셀 처리
- **SciPy** — distance_transform으로 경계 부드럽게 처리
- **Flood-fill (BFS)** — 가장자리에서 연결된 배경만 정확히 감지
- **PyInstaller** — 단일 .exe 패키징
