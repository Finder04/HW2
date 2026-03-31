import os
from deepface import DeepFace

# 모델 로드 강제를 위한 사전 초기화 (서버 시작 시 지연 시간을 줄이기 위함)
# 처음 실행될 때 가중치 파일 다운로드를 위해 시간이 소요될 수 있습니다.
# 빠른 실행을 위해 가벼운 백엔드(opencv 또는 ssd 등)를 보통 사용하지만 기본 가중치를 그대로 써도 무방합니다.
try:
    print("Pre-loading DeepFace age model...")
    # 더미 이미지 경로 대신 초기화만 하도록 할 수 있으나 모델의 구조적 한계로 
    # 실제 요청 시 다운로드 및 로드가 발생할 수 있습니다. 
except Exception as e:
    pass

def predict_attributes(image_path: str) -> dict:
    """
    이미지 경로를 받아 DeepFace로 나이와 성별을 예측하는 함수.
    """
    try:
        # actions=['age', 'gender']를 주어 나이와 성별 예측
        # enforce_detection=False: 얼굴 인식이 간헐적으로 안 되더라도 오류를 덜 내도록 함
        result = DeepFace.analyze(
            img_path=image_path, 
            actions=['age', 'gender'], 
            enforce_detection=False
        )
        
        # 분석 결과는 리스트로 반환될 수 있음 (여러 명의 얼굴이 검출된 경우)
        if isinstance(result, list):
            # 얼굴들에 대한 나이와 성별 반환
            faces_info = []
            for face in result:
                faces_info.append({"age": face.get("age"), "gender": face.get("dominant_gender")})
            return {"status": "success", "predictions": faces_info}
        
        # 단일 얼굴일 경우
        return {
            "status": "success", 
            "predictions": [{"age": result.get("age"), "gender": result.get("dominant_gender")}]
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
