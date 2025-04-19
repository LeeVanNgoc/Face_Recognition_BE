from flask import jsonify, request
from User.model import db, User

# Hàm POST để tạo người dùng
def create_user():
    data = request.get_json()  # Lấy dữ liệu từ request body

    # Kiểm tra xem các trường cần thiết có mặt không
    if not data or not data.get('id') or not data.get('name') or not data.get('email') or not data.get('phone'):
        return jsonify({"message": "Missing data"}), 400

    # Tạo một người dùng mới
    new_user = User(id=data['id'], name=data['name'], email=data['email'], phone=data['phone'])

    try:
        db.session.add(new_user)  # Thêm người dùng vào session
        db.session.commit()        # Commit để lưu vào cơ sở dữ liệu
        return jsonify({
            "message": "User created",
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "phone": new_user.phone
            }
        }), 201
    except Exception as e:
        db.session.rollback()      # Rollback nếu có lỗi xảy ra
        return jsonify({"message": "Error creating user", "error": str(e)}), 500


# Hàm GET để lấy tất cả người dùng
def get_all_users():
    users = User.query.all()  # Lấy tất cả người dùng từ DB
    if users:
        return jsonify([{
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'phone': user.phone
        } for user in users]), 200
    else:
        return jsonify({"message": "No users found"}), 404


# Hàm GET để lấy người dùng theo ID
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'phone': user.phone
        }), 200
    else:
        return jsonify({"message": "User not found"}), 404


# Hàm PUT để cập nhật thông tin người dùng
def update_user(user_id):
    data = request.get_json()  # Lấy dữ liệu từ request body
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    if data.get('name'):
        user.name = data['name']
    if data.get('email'):
        user.email = data['email']
    if data.get('phone'):
        user.phone = data['phone']

    try:
        db.session.commit()  # Cập nhật vào DB
        return jsonify({
            'message': 'User updated',
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone
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
