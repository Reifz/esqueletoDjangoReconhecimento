import cv2
import numpy as np
from deepface import DeepFace
from sklearn.metrics.pairwise import cosine_similarity

# Inicializa a captura de vídeo da webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Carrega a imagem de referência
reference_img = cv2.imread("img/foto4.jpg")
if reference_img is None:
    print("Erro: Imagem de referência não encontrada.")
    exit()

# Pré-computa o embedding da referência
reference_embedding = DeepFace.represent(
    reference_img, model_name="Facenet512", detector_backend="mtcnn", enforce_detection=False
)[0]["embedding"]

# Função para comparar embeddings
def compare_embeddings(embedding1, embedding2, threshold=0.7):
    similarity = cosine_similarity([embedding1], [embedding2])[0][0]
    return similarity > threshold, similarity

# Extrai embedding de um frame
def get_embedding(frame):
    try:
        embeddings = DeepFace.represent(
            frame, model_name="Facenet512", detector_backend="mtcnn", enforce_detection=False
        )
        return embeddings[0]["embedding"] if embeddings else None
    except:
        return None

counter = 0
face_match = False
confidence = 0.0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Falha ao capturar frame da webcam")
        break

    if counter % 15 == 0:
        embedding = get_embedding(frame.copy())
        if embedding is not None:
            face_match, confidence = compare_embeddings(embedding, reference_embedding)
    counter += 1

    # Exibe resultado
    status = "CORRESPONDENCIA" if face_match else "SEM CORRESPONDENCIA"
    color = (0, 255, 0) if face_match else (0, 0, 255)
    cv2.putText(frame, f"{status} ({confidence:.2%})", (20, 450),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("Reconhecimento Facial", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
