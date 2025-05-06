import base64
from io import BytesIO
from PIL import Image
import numpy as np
from flask import Flask, request, jsonify
from insightface.app import FaceAnalysis
from scipy.spatial.distance import cosine
import pickle

# Khởi tạo model InsightFace 1 lần
app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0, det_size=(640, 640))

# Hàm tính toán độ tương đồng cosine giữa 2 embedding
def cosine_similarity(emb1, emb2):
    return 1 - cosine(emb1, emb2)

# Hàm để tải cơ sở dữ liệu embedding và tên từ pickle
def load_database():
    try:
        with open('dataset1/faces.pkl', 'rb') as f:
            faces_db = pickle.load(f)
        with open('dataset1/names.pkl', 'rb') as f:
            names_db = pickle.load(f)
    except FileNotFoundError:
        faces_db = []
        names_db = []
    return faces_db, names_db

# Hàm nhận diện và trả về tên
def recognize(embedding):
    faces_db, names_db = load_database()
    threshold = 0.6  # Ngưỡng để nhận diện

    # Kiểm tra kiểu dữ liệu của từng embedding trong faces_db
    for i, (db_embedding, name) in enumerate(zip(faces_db, names_db)):
        
        if isinstance(db_embedding, tuple):
            db_embedding = db_embedding[0]  # Chuyển tuple thành NumPy array
        
        
        similarity = cosine_similarity(embedding, db_embedding)
        if similarity > threshold:  # Nếu độ tương đồng đủ cao, trả về tên
            return name

    return "Không nhận diện được"  # Nếu không có sự tương đồng cao

# Hàm nhận diện và trả về tên
# def recognize(embedding):
#     faces_db, names_db = load_database()
#     threshold = 0.6  # Ngưỡng để nhận diện
#     print("faces_db đã lấy:", len(faces_db))
#     print("Embedding đã lấy:", embedding.shape)
#     # Kiểm tra kiểu dữ liệu của từng embedding trong faces_db
#     for i, db_embedding, name in enumerate(faces_db, names_db):
#         print(f"Embedding {i} trong faces_db có kiểu dữ liệu: {type(db_embedding)}")
#         if isinstance(db_embedding, tuple):
#             print(f"Embedding {i} là tuple, chuyển đổi thành NumPy array.")
#             db_embedding = np.array(db_embedding)  # Chuyển tuple thành NumPy array
#             similarity = cosine_similarity(embedding, db_embedding)
#             if similarity > threshold:  # Nếu độ tương đồng đủ cao, trả về tên
#                 return name
#         print(f"Embedding {i} trong faces_db có kích thước: {db_embedding.shape}")

    # for db_embedding, name in zip(faces_db, names_db):
    #     similarity = cosine_similarity(embedding, db_embedding)
    #     if similarity > threshold:  # Nếu độ tương đồng đủ cao, trả về tên
    #         return name

    # return "Không nhận diện được"  # Nếu không có sự tương đồng cao

# Hàm để giải mã base64 và chuyển thành hình ảnh PIL
def decode_base64_image(base64_string):
    img_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(img_data))
    return np.array(image)

def get_embedding(image):
    # Nhận diện khuôn mặt
    faces = app.get(image)
    if faces:
        # Lấy embedding của khuôn mặt đầu tiên
        embedding = faces[0].embedding
        # Kiểm tra nếu embedding là numpy array và có chiều dài đúng
        if isinstance(embedding, np.ndarray) and embedding.shape == (512,):  # Giả sử embedding có kích thước 512            
            # Nhận diện người dùng và trả về tên
            name = recognize(embedding)
            return embedding, name
        else:
            return None, "Kích thước embedding không hợp lệ"
    return None, "Không phát hiện khuôn mặt"  # Nếu không có khuôn mặt
