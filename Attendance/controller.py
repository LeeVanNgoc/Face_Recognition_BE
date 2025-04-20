from flask import jsonify, request
from Attendance.model import db, Attendance  # Import model Attendance

# Hàm POST để tạo bản ghi chấm công mới
def create_attendance():
    data = request.get_json()  # Lấy dữ liệu từ request body

    # Kiểm tra xem các trường cần thiết có mặt không
    if not data or not data.get('userId') or not data.get('timeCheck') or not data.get('typeCheck'):
        return jsonify({"message": "Missing data"}), 400

    # Tạo một bản ghi chấm công mới
    new_attendance = Attendance(
        userId=data['userId'],
        timeCheck=data['timeCheck'],
        typeCheck=data['typeCheck']
    )

    try:
        db.session.add(new_attendance)  # Thêm bản ghi vào session
        db.session.commit()  # Commit để lưu vào cơ sở dữ liệu
        return jsonify({
            "message": "Attendance created",
            "attendance": {
                "id": new_attendance.id,
                "userId": new_attendance.userId,
                "timeCheck": new_attendance.timeCheck,
                "typeCheck": new_attendance.typeCheck
            }
        }), 201
    except Exception as e:
        db.session.rollback()  # Rollback nếu có lỗi
        return jsonify({"message": "Error creating attendance", "error": str(e)}), 500


# Hàm GET để lấy tất cả bản ghi chấm công
def get_all_attendances():
    attendances = Attendance.query.all()  # Lấy tất cả bản ghi từ DB
    if attendances:
        return jsonify([{
            'id': attendance.id,
            'userId': attendance.userId,
            'timeCheck': attendance.timeCheck,
            'typeCheck': attendance.typeCheck
        } for attendance in attendances]), 200
    else:
        return jsonify({"message": "No attendances found"}), 404


# Flask API: Lấy danh sách chấm công của một người dùng theo userId
def get_attendance_by_user(user_id):
    attendances = Attendance.query.filter_by(userId=user_id).all()  # Lọc theo userId
    if attendances:
        return jsonify([{
            'id': attendance.id,
            'userId': attendance.userId,
            'timeCheck': attendance.timeCheck,
            'typeCheck': attendance.typeCheck
        } for attendance in attendances]), 200
    else:
        return jsonify({"message": "No attendances found for this user"}), 404



# Hàm PUT để cập nhật thông tin bản ghi chấm công
def update_attendance(attendance_id):
    data = request.get_json()  # Lấy dữ liệu từ request body
    attendance = Attendance.query.get(attendance_id)
    
    if not attendance:
        return jsonify({"message": "Attendance not found"}), 404

    if data.get('userId'):
        attendance.userId = data['userId']
    if data.get('timeCheck'):
        attendance.timeCheck = data['timeCheck']
    if data.get('typeCheck') is not None:
        attendance.typeCheck = data['typeCheck']

    try:
        db.session.commit()  # Cập nhật vào DB
        return jsonify({
            'message': 'Attendance updated',
            'attendance': {
                'id': attendance.id,
                'userId': attendance.userId,
                'timeCheck': attendance.timeCheck,
                'typeCheck': attendance.typeCheck
            }
        }), 200
    except Exception as e:
        db.session.rollback()  # Rollback nếu có lỗi
        return jsonify({"message": "Error updating attendance", "error": str(e)}), 500


# Hàm DELETE để xóa bản ghi chấm công theo ID
def delete_attendance(attendance_id):
    attendance = Attendance.query.get(attendance_id)
    
    if not attendance:
        return jsonify({"message": "Attendance not found"}), 404
    
    try:
        db.session.delete(attendance)  # Xóa bản ghi
        db.session.commit()  # Commit thay đổi vào DB
        return jsonify({"message": "Attendance deleted"}), 200
    except Exception as e:
        db.session.rollback()  # Rollback nếu có lỗi
        return jsonify({"message": "Error deleting attendance", "error": str(e)}), 500
