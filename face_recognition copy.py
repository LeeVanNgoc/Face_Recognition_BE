import os
import cv2
import pickle
import numpy as np
from insightface.app import FaceAnalysis
from scipy.spatial.distance import cosine
import tim

# Khởi tạo ứng dụng ArcFace
app = FaceAnalysis(name='buffalo_l')  # Model Face Recognition từ InsightFace
app.prepare(ctx_id=0, det_size=(640, 640))  # Dùng GPU nếu có

# Đường dẫn lưu dữ liệu
DATASET_PATH = 'dataset1/'
FACES_FILE = os.path.join(DATASET_PATH, 'faces.pkl')
NAMES_FILE = os.path.join(DATASET_PATH, 'names.pkl')

# Tạo dataset nếu chưa có
os.makedirs(DATASET_PATH, exist_ok=True)

# Lấy tên người dùng
name = input('Enter your name --> ')

# Mở camera
camera = cv2.VideoCapture(0)
face_data = []
collected = 0

while collected < 10:
    ret, frame = camera.read()
    if not ret:
        print('Lỗi: Không thể lấy khung hình!')
        break
    
    faces = app.get(frame)
    for face in faces:
        embedding = face.embedding
        if collected < 10:
            face_data.append(embedding)
            collected += 1
        cv2.rectangle(frame, (int(face.bbox[0]), int(face.bbox[1])), 
                      (int(face.bbox[2]), int(face.bbox[3])), (255, 0, 0), 2)
    
    cv2.imshow('Capturing Faces', frame)
    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()

face_data = np.array(face_data)

# Lưu embeddings vào file
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

print("Dữ liệu đã được lưu thành công!")


# Lấy tên người dùng
name = input('Enter your name --> ')

# Mở camera
camera = cv2.VideoCapture(0)
face_data = []
collected = 0

while collected < 10:
    ret, frame = camera.read()
    if not ret:
        print('Lỗi: Không thể lấy khung hình!')
        break
    
    faces = app.get(frame)
    for face in faces:
        embedding = face.embedding
        if collected < 10:
            face_data.append(embedding)
            collected += 1
        cv2.rectangle(frame, (int(face.bbox[0]), int(face.bbox[1])), 
                      (int(face.bbox[2]), int(face.bbox[3])), (255, 0, 0), 2)
    
    cv2.imshow('Capturing Faces', frame)
    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()

face_data = np.array(face_data)

# Lưu embeddings vào file
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

print("Dữ liệu đã được lưu thành công!")

faces_file = 'dataset1/faces.pkl'
names_file = 'dataset1/names.pkl'

# Đọc nội dung names.pkl
if not os.path.exists(names_file):
    print("Không tìm thấy tệp names.pkl!")
else:
    with open(names_file, 'rb') as file:
        names = pickle.load(file)
    print("\n🔹 Nội dung của names.pkl:")
    print(names)

# Đọc nội dung faces.pkl
if not os.path.exists(faces_file):
    print("Không tìm thấy tệp faces.pkl!")
else:
    with open(faces_file, 'rb') as file:
        faces = pickle.load(file)
    
    print("\n🔹 Nội dung của faces.pkl:")
    print(faces.shape)  # In toàn bộ nội dung (có thể rất lớn!)


# =============== Nhận diện khuôn mặt ===============
print("Đang khởi động hệ thống nhận diện...")
with open(FACES_FILE, 'rb') as f:
    faces_db = pickle.load(f)
with open(NAMES_FILE, 'rb') as f:
    names_db = pickle.load(f)

camera = cv2.VideoCapture(0)
while True:
    ret, frame = camera.read()
    if not ret:
        print("Lỗi: Không thể lấy khung hình!")
        break
    
    faces = app.get(frame)
    for face in faces:
        embedding = face.embedding
        min_dist = float('inf')
        best_match = "Unknown"
        
        for idx, stored_embedding in enumerate(faces_db):
            dist = cosine(embedding, stored_embedding)
            if dist < min_dist:
                min_dist = dist
                best_match = names_db[idx]
        
        if min_dist > 0.5:
            best_match = "Unknown"
        
        x1, y1, x2, y2 = map(int, face.bbox)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, best_match, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('Live Face Recognition', frame)
    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()

# Đọc dữ liệu embeddings và tên
FACES_FILE = "dataset1/faces.pkl"
NAMES_FILE = "dataset1/names.pkl"

print("Đang khởi động hệ thống nhận diện...")
with open(FACES_FILE, 'rb') as f:
    faces_db = pickle.load(f)
with open(NAMES_FILE, 'rb') as f:
    names_db = pickle.load(f)

camera = cv2.VideoCapture(0)

last_frame = None  # Biến lưu ảnh cuối cùng đã xử lý

while True:
    ret, frame = camera.read()
    if not ret:
        print("Lỗi: Không thể lấy khung hình!")
        break

    faces = app.get(frame)

    for face in faces:
        embedding = face.embedding
        min_dist = float('inf')
        best_match = "Unknown"
        
        for idx, stored_embedding in enumerate(faces_db):
            dist = cosine(embedding, stored_embedding)
            if dist < min_dist:
                min_dist = dist
                best_match = names_db[idx]
        
        if min_dist > 0.5:
            best_match = "Unknown"
        
        x1, y1, x2, y2 = map(int, face.bbox)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, best_match, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Live Face Recognition', frame)

    last_frame = frame.copy()  # Lưu ảnh cuối cùng đã xử lý (có bounding box + tên)

    if cv2.waitKey(1) == 27:  # Nhấn ESC để thoát
        break

# Lưu ảnh cuối cùng (có bounding box và tên)
if last_frame is not None:
    cv2.imwrite("last_frame.jpg", last_frame)
    print("Ảnh cuối cùng đã được lưu: last_frame.jpg")

camera.release()
cv2.destroyAllWindows()

print("Đang khởi động hệ thống nhận diện...")
with open(FACES_FILE, 'rb') as f:
    faces_db = pickle.load(f)
with open(NAMES_FILE, 'rb') as f:
    names_db = pickle.load(f)

camera = cv2.VideoCapture(0)

SCAN_INTERVAL = 10  # Khoảng thời gian giữa các lần quét (giây)
DISPLAY_DURATION = 2  # Thời gian hiển thị bounding box và tên (giây)

last_scan_time = 0  # Thời gian quét cuối cùng
last_display_time = 0  # Thời gian bắt đầu hiển thị
last_faces_detected = []  # Lưu kết quả nhận diện gần nhất

while True:
    ret, frame = camera.read()
    if not ret:
        print("Lỗi: Không thể lấy khung hình!")
        break

    current_time = time.time()
    
    # Nếu đã đến thời gian quét tiếp theo
    if current_time - last_scan_time >= SCAN_INTERVAL:
        last_scan_time = current_time  # Cập nhật thời gian quét
        last_display_time = current_time  # Cập nhật thời gian bắt đầu hiển thị

        faces = app.get(frame)  # Lấy danh sách khuôn mặt
        last_faces_detected = []  # Reset danh sách khuôn mặt đã quét

        for face in faces:
            embedding = face.embedding
            min_dist = float('inf')
            best_match = "Unknown"

            for idx, stored_embedding in enumerate(faces_db):
                dist = cosine(embedding, stored_embedding)
                if dist < min_dist:
                    min_dist = dist
                    best_match = names_db[idx]

            if min_dist > 0.5:
                best_match = "Unknown"

            # Lưu bounding box và tên để hiển thị
            x1, y1, x2, y2 = map(int, face.bbox)
            last_faces_detected.append((x1, y1, x2, y2, best_match))

    # Hiển thị bounding box trong 2 giây
    if current_time - last_display_time <= DISPLAY_DURATION:
        for (x1, y1, x2, y2, name) in last_faces_detected:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Live Face Recognition', frame)

    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()