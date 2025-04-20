# Attendance.route.py
from flask import Blueprint
from Attendance.controller import create_attendance, get_all_attendances, get_attendance_by_user, update_attendance, delete_attendance

attendance_bp = Blueprint('attendance', __name__)

# Đăng ký các route cho API
attendance_bp.route('/attendance', methods=['POST'])(create_attendance)           # Tạo bản ghi chấm công mới
attendance_bp.route('/attendance', methods=['GET'])(get_all_attendances)         # Lấy tất cả bản ghi chấm công

# Đảm bảo đường dẫn rõ ràng cho các thao tác lấy, cập nhật và xóa bản ghi chấm công theo ID
attendance_bp.route('/attendance/<user_id>', methods=['GET', 'OPTIONS'])(get_attendance_by_user)  # Lấy bản ghi chấm công theo ID
attendance_bp.route('/attendance/<int:attendance_id>', methods=['PUT'])(update_attendance)     # Cập nhật bản ghi chấm công
attendance_bp.route('/attendance/<int:attendance_id>', methods=['DELETE'])(delete_attendance)  # Xóa bản ghi chấm công
