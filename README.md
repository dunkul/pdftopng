# PDF to PNG 변환기

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

PDF 파일의 각 페이지를 개별 PNG 이미지로 저장하는 도구입니다. GUI(`gui.py`)와 명령줄(`pdf_to_png.py`) 두 가지 방식을 지원합니다.

## 다운로드 (exe)

Python 설치 없이 바로 실행하고 싶다면 소스코드를 받을 필요 없이 [Releases](../../releases) 페이지에서 `PdfToPng.exe`를 내려받아 실행하면 됩니다.

- **Windows 10/11 64비트**에서만 동작합니다.
- 코드 서명이 되어 있지 않아 실행 시 **Windows Defender SmartScreen** 경고("알 수 없는 게시자")가 뜰 수 있습니다. "추가 정보 → 실행"을 클릭하면 실행됩니다.
- 백신 프로그램에 따라 드물게 오탐(false positive)이 발생할 수 있습니다. 문제가 있으면 예외 등록이 필요할 수 있습니다.

## 기능

- PDF의 모든 페이지를 페이지별 PNG로 저장
- 해상도(DPI) 조절 (기본 96dpi, 화면 표시 기준)
- 흑백(그레이스케일) 변환
- PNG 최적화 (컬러 256색 축소 + 재압축)로 파일 용량 절감

## 구성 파일

| 파일 | 설명 |
|---|---|
| `pdf_to_png.py` | 변환 로직 + 명령줄(CLI) 실행 |
| `gui.py` | tkinter 기반 GUI (내부적으로 `pdf_to_png.py` 사용) |
| `requirements.txt` | 필요한 패키지 목록 |

> `venv/`, `build/`, `dist/`, `*.spec`은 로컬에서 생성되는 산출물이라 `.gitignore`로 제외되어 있으며 저장소에는 포함되어 있지 않습니다. 아래 안내에 따라 직접 생성하면 됩니다.

---

## 1. 시작하기

```powershell
# 1. 저장소 클론
git clone https://github.com/dunkul/pdftopng.git
cd pdftopng

# 2. 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate

# 3. 패키지 설치
pip install -r requirements.txt
```

> Python 3.9 이상이 설치되어 있어야 합니다 (`python --version`으로 확인).

### GUI 실행

```powershell
venv\Scripts\python gui.py
```

1. **파일 불러오기** 버튼으로 PDF 선택
2. 필요하면 DPI / 흑백 / PNG 최적화 옵션 조정
3. **시작하기** 클릭 → PDF와 같은 이름의 폴더에 `파일명_001.png`, `파일명_002.png` ... 형식으로 저장

### CLI 실행

```powershell
venv\Scripts\python pdf_to_png.py 파일.pdf
```

옵션:

| 옵션 | 설명 | 기본값 |
|---|---|---|
| `-o, --output` | 출력 폴더 지정 | PDF와 같은 이름의 폴더 |
| `-d, --dpi` | 해상도(DPI) | 96 |
| `-g, --grayscale` | 흑백으로 저장 | 꺼짐 |
| `--optimize` | PNG 재압축 + 컬러 축소로 용량 절감 | 꺼짐 |

예시:

```powershell
venv\Scripts\python pdf_to_png.py 문서.pdf -d 150 -g --optimize -o 결과폴더
```

---

## 2. (선택) 소스에서 exe 직접 빌드하기

Releases의 exe 대신 직접 빌드하고 싶다면:

```powershell
# 가상환경 활성화 상태에서
pip install pyinstaller

pyinstaller --onefile --windowed --name PdfToPng gui.py
```

결과물은 `dist\PdfToPng.exe`에 생성됩니다.

---

## 문제 해결

- **파일 용량이 너무 큼** → DPI를 낮추거나(예: 72~96), "PNG 최적화" 옵션을 켜세요. DPI는 픽셀 수(면적)에 직접 비례하므로 용량 감소에 가장 효과적입니다.
- **exe 실행이 안 됨** → 64비트 Windows인지 확인하고, SmartScreen 경고가 뜨면 "추가 정보 → 실행"을 선택하세요.

## 라이선스

[MIT License](LICENSE)
