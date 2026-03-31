# 1. Base 이미지 설정 (Python 3.9 slim 버전 사용으로 경량화)
FROM python:3.9-slim

# 2. 작업 디렉토리 설정 및 환경 변수
# Python 버퍼링 제거 (로그 즉시 출력), DeepFace 모델 다운로드 경로를 컨테이너 내부로 설정
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV DEEPFACE_HOME=/app

# 3. 시스템 패키지 설치 (OpenCV 구동 등) 및 캐시 삭제
# 여러 RUN 명령어를 하나로 묶어 레이어 수 최소화
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 4. 의존성 먼저 복사 및 설치 (Docker 캐시(레이어) 활용)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. (최적화✨) 모델 가중치 사전 다운로드
# 빌드 시점에 모델 가중치를 미리 받아두어 서버 리부트/시작 시간을 비약적으로 단축
RUN python -c "from deepface import DeepFace; DeepFace.build_model('Age')" || echo "사전 다운로드 무시"

# 6. 애플리케이션 코드 복사
COPY ./app ./app

# 7. (보안✨) non-root 사용자 생성 및 권한 설정
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# 8. 포트 노출 및 앱 구동 명령어
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
