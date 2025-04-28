import os
import cv2
import pickle
import numpy as np
from insightface.app import FaceAnalysis

# Khởi tạo FaceAnalysis (dùng GPU nếu có)
app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0, det_size=(640, 640))

# Thư mục lưu dữ liệu
DATASET_PATH = 'dataset1'
FACES_FILE = os.path.join(DATASET_PATH, 'faces.pkl')
NAMES_FILE = os.path.join(DATASET_PATH, 'names.pkl')
os.makedirs(DATASET_PATH, exist_ok=True)

# Nhập tên người dùng
name = input('Enter your name --> ')

# Mở camera và thu 10 ảnh
camera = cv2.VideoCapture(0)
face_data = []
collected = 0

print("Bắt đầu thu thập khuôn mặt...")

while collected < 10:
    ret, frame = camera.read()
    if not ret:
        break

    faces = app.get(frame)
    for face in faces:
        face_data.append(face.embedding)
        collected += 1
        cv2.rectangle(frame, (int(face.bbox[0]), int(face.bbox[1])),
                      (int(face.bbox[2]), int(face.bbox[3])), (0, 255, 0), 2)
        if collected >= 10:
            break

    cv2.imshow('Enrolling...', frame)
    if cv2.waitKey(1) == 27:  # Nhấn ESC để hủy
        break

camera.release()
cv2.destroyAllWindows()

# Lưu embeddings vào file
face_data = np.array(face_data)

if os.path.exists(FACES_FILE):
    with open(FACES_FILE, 'rb') as f:
        faces_db = pickle.load(f)
    faces_db = np.vstack([faces_db, face_data])
else:
    faces_db = face_data

with open(FACES_FILE, 'wb') as f:
    pickle.dump(faces_db, f)

# Lưu tên vào file
if os.path.exists(NAMES_FILE):
    with open(NAMES_FILE, 'rb') as f:
        names_db = pickle.load(f)
    names_db.extend([name] * 10)
else:
    names_db = [name] * 10

with open(NAMES_FILE, 'wb') as f:
    pickle.dump(names_db, f)

print(f"✅ Đã lưu dữ liệu cho người: {name}")
