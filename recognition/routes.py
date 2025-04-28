from flask import Blueprint, request, jsonify
import cv2
import numpy as np
import base64
from .detector import get_embedding
from .matcher import find_best_match
from .database import load_database
from .database import save_to_database

recognition_bp = Blueprint('recognition', __name__)

# Load cơ sở dữ liệu khi khởi động
faces_db, names_db = load_database()

def decode_base64_image(base64_string):
    """Chuyển base64 thành ảnh numpy array"""
    img_data = base64.b64decode(base64_string.split(',')[1])  # Bỏ qua phần prefix 'data:image/jpeg;base64,'
    np_arr = np.frombuffer(img_data, dtype=np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

@recognition_bp.route('/recognize', methods=['POST'])
def recognize_face():
    data = request.get_json()
    image_data = data.get('image')  # Nhận dữ liệu hình ảnh base64 từ frontend

    try:
        image = decode_base64_image(image_data)  # Giải mã ảnh base64 thành numpy array
        embedding, name = get_embedding(image)  # Lấy embedding và tên từ hàm get_embedding

        if embedding is not None:
            # Trả về tên và embedding
            response = {'status': 'success', 'name': name, 'embedding': embedding.tolist()}
            return jsonify(response)
        else:
            return jsonify({'status': 'error', 'message': 'No face detected'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@recognition_bp.route('/enroll', methods=['POST'])
def enroll():
    file = request.files.get('image')
    name = request.form.get('name')

    if not file or not name:
        return jsonify({'error': 'Cần ảnh và tên'}), 400

    img_array = np.frombuffer(file.read(), np.uint8)
    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    embedding = get_embedding(frame)
    if embedding is None:
        return jsonify({'error': 'Không tìm thấy khuôn mặt'}), 400

    # Lưu vào database
    save_to_database(embedding, name)

    return jsonify({'message': f'Đã thêm {name} vào cơ sở dữ liệu.'})