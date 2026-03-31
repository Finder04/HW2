from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
import shutil
import os
import uuid
from .services import predict_attributes

app = FastAPI(
    title="Age Prediction API", 
    description="MLOps pipeline API for Age Prediction (Local Server)",
    version="1.0.0"
)

# 업로드 파일 저장을 위한 디렉터리 경로 설정
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    with open(html_file, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/predict/attributes")
async def predict_attributes_endpoint(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="유효한 이미지 파일이 아닙니다.")

    # 파일명을 고유하게 만들기 (유니크한 임시 식별자)
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # 이미지 파일 저장
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 저장 오류: {str(e)}")
    finally:
        file.file.close()

    # 모델 추론 진행
    print(f"Starting inference on {file_path}")
    response = predict_attributes(file_path)

    # (옵션) 모델 추론 후 서버 저장 공간 절약을 위해 파일을 지웁니다.
    # 만약 MLOps의 재학습(Retraining) 데이터셋 구축을 하려면 남길 수도 있습니다.
    if os.path.exists(file_path):
        os.remove(file_path)

    if response.get("status") == "error":
        raise HTTPException(status_code=500, detail=response.get("message"))

    return {
        "filename": file.filename,
        "prediction": response.get("predictions")
    }
