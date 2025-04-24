from flask import Blueprint
from User.controller import create_user, get_all_users, get_user_by_id, update_user, delete_user, sign_in_user, log_in_user

user_bp = Blueprint('user', __name__)

# Đăng ký các route cho API
user_bp.route('/users', methods=['POST'])(create_user)           # Tạo người dùng
user_bp.route('/users', methods=['GET'])(get_all_users)         # Lấy tất cả người dùng
user_bp.route('/auth/signup', methods=['POST'])(sign_in_user)   # Đăng ký tài khoản
user_bp.route('/auth/login', methods=['POST'])(log_in_user)     # Đăng nhập
user_bp.route('/users/<int:user_id>', methods=['GET'])(get_user_by_id)  # Lấy người dùng theo ID
user_bp.route('/users/<int:user_id>', methods=['PUT'])(update_user)     # Cập nhật người dùng
user_bp.route('/users/<int:user_id>', methods=['DELETE'])(delete_user)  # Xóa người dùng
