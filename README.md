# Age Prediction API

이 프로젝트는 `DeepFace` 모델을 사용하여 업로드된 사람 얼굴 이미지로부터 **나이를 예측(Age Prediction)** 하는 경량 API 서버입니다. Python 기반의 FastAPI로 동작하며, 로컬 데스크탑 또는 랩탑을 MLOps 파이프라인의 서버로 활용하기 위해 설계되었습니다.

## 기술 스택
- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Model / Inference**: [DeepFace](https://github.com/serengil/deepface)
- **Containerization**: [Docker](https://www.docker.com/)

---

## 프로젝트 구조 (Project Structure)
```
.
├── app/
│   ├── __init__.py      # 패키지 초기화
│   ├── main.py          # 라우팅 (FastAPI) 코드
│   └── services.py      # ML Model(DeepFace) 추론 서비스
├── Dockerfile           # 도커 컨테이너화 정보
├── README.md            # 사용 설명서
└── requirements.txt     # Python 패키지 의존성 파일
```

---

## 설치 및 실행 방법 (로컬 환경)

### 1. 가상 환경 설정 및 패키지 설치
Python 3.8 이상 버전을 권장합니다. 터미널(또는 CMD)에서 아래 명령어를 순차적으로 실행하세요.

```bash
# 가상 환경 생성 (옵션)
python -m venv venv
source venv/bin/activate  # Mac / Linux
# venv\Scripts\activate  # Windows

# 의존성 패키지 설치
pip install -r requirements.txt
```

### 2. 서버 실행
Uvicorn을 사용해 서버를 띄울 수 있습니다.

```bash
uvicorn app.main:app --reload
```
서버가 시작되면 웹 브라우저에서 `http://127.0.0.1:8000`으로 접속하여 접속 성공 여부를 확인할 수 있습니다.

---

## API 엔드포인트 테스트 방법

Postman과 같은 도구 없이 웹 브라우저의 자동으로 제공되는 Swagger UI 문서를 통해 나이 예측 테스트가 가능합니다. 

- 브라우저로 `http://127.0.0.1:8000/docs` 접속
- `/predict/age` (POST) 탭을 펼친 후 **Try it out** -> **Choose File** (얼굴 사진 업로드) -> **Execute** 클릭

---

## MLOps 활용 및 Docker 빌드

본인의 컴퓨터를 서버 환경으로 쓰거나 배포 환경 테스트를 진행하려면 Docker를 활용할 수 있습니다.

```bash
# 컨테이너 이미지 생성
docker build -t age-predictor-api .

# 백그라운드로 8000포트를 할당하여 실행
docker run -d -p 8000:8000 --name age-predictor age-predictor-api
```
이후 백그라운드로 서버가 계속 유지되며 서비스를 시작합니다.
