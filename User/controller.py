from flask import jsonify, request
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from datetime import datetime
from User.model import db, User

# Hàm POST để tạo người dùng
def create_user():
    data = request.get_json()  # Lấy dữ liệu từ request body

    # Kiểm tra xem các trường cần thiết có mặt không
    if not data or not data.get('id') or not data.get('fullName') or not data.get('email') or not data.get('phone') or not data.get('gender') or not data.get('address') or not data.get('image'):
        return jsonify({"message": "Missing data"}), 400

    # Tạo một người dùng mới
    new_user = User(id=data['id'], fullName=data['fullName'], email=data['email'], 
                phone=data['phone'], gender=data['gender'], address=data['address'], 
                image=data['image'])


    try:
        db.session.add(new_user)  # Thêm người dùng vào session
        db.session.commit()        # Commit để lưu vào cơ sở dữ liệu
        return jsonify({
            "message": "User created",
            "user": {
                "id": new_user.id,
                "fullName": new_user.fullName,
                "email": new_user.email,
                "phone": new_user.phone,
                "gender": new_user.gender,
                "address": new_user.address,
                "image": new_user.image,
            }
        }), 201
    except Exception as e:
        db.session.rollback()      # Rollback nếu có lỗi xảy ra
        return jsonify({"message": "Error creating user", "error": str(e)}), 500
    

def sign_in_user():
    data = request.get_json()

    # Kiểm tra các trường bắt buộc
    required_fields = ['id', 'fullName', 'email', 'phone', 'password']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"message": "Missing data"}), 400

    try:
        # Băm mật khẩu
        hashed_password = generate_password_hash(data['password'], method='sha256')

        # Tạo người dùng mới
        new_user = User(
            id=data['id'],
            fullName=data['fullName'],
            email=data['email'],
            phone=data['phone'],
            password=hashed_password,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "User created",
            "user": {
                "id": new_user.id,
                "fullName": new_user.fullName,
                "email": new_user.email,
                "phone": new_user.phone
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating user", "error": str(e)}), 500


# Hàm POST để đăng nhập người dùng
def log_in_user():
    data = request.get_json()

    # Kiểm tra dữ liệu đầu vào
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Missing email or password"}), 400

    # Tìm người dùng theo email
    user = User.query.filter_by(email=data['email']).first()

    # Kiểm tra mật khẩu (đã hash)
    if user and check_password_hash(user.password, data['password']):
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "fullName": user.fullName,
                "email": user.email,
                "phone": user.phone,
                "gender": user.gender,
                "address": user.address,
                "image": user.image
            }
        }), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

# Hàm GET để lấy tất cả người dùng
def get_all_users():
    users = User.query.all()  # Lấy tất cả người dùng từ DB
    if users:
        return jsonify([{
            'id': user.id,
            'fullName': user.fullName,
            'email': user.email,
            'phone': user.phone,
            "gender": user.gender,
            "address": user.address,
            "image": user.image
        } for user in users]), 200
    else:
        return jsonify({"message": "No users found"}), 404


# Hàm GET để lấy người dùng theo ID
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'fullName': user.fullName,
            'email': user.email,
            'phone': user.phone,
            "gender": user.gender,
            "address": user.address,
            "image": user.image
        }), 200
    else:
        return jsonify({"message": "User not found"}), 404


# Hàm PUT để cập nhật thông tin người dùng
def update_user(user_id):
    data = request.get_json()  # Lấy dữ liệu từ request body
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    if data.get('fullName'):
        user.fullName = data['fullName']
    if data.get('email'):
        user.email = data['email']
    if data.get('phone'):
        user.phone = data['phone']
    if data.get('gender'):
        user.gender = data['gender']
    if data.get('address'):
        user.address = data['address']

    try:
        db.session.commit()  # Cập nhật vào DB
        return jsonify({
            'message': 'User updated',
            'user': {
                'id': user.id,
                'fullName': user.fullName,
                'email': user.email,
                'phone': user.phone,
                "gender": user.gender,
                "address": user.address,
                "image": user.image
            }
        }), 200
    except Exception as e:
        db.session.rollback()  # Rollback nếu có lỗi
        return jsonify({"message": "Error updating user", "error": str(e)}), 500


# Hàm DELETE để xóa người dùng theo ID
def delete_user(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    try:
        db.session.delete(user)  # Xóa người dùng
        db.session.commit()  # Commit thay đổi vào DB
        return jsonify({"message": "User deleted"}), 200
    except Exception as e:
        db.session.rollback()  # Rollback nếu có lỗi
        return jsonify({"message": "Error deleting user", "error": str(e)}), 500
