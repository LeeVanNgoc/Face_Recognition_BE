from config.config import db

class Attendance(db.Model):
    __tablename__ = 'attendance'  # Tên bảng trong DB (tùy chọn, nếu không thì mặc định là tên lớp)

    id = db.Column(db.Integer, primary_key=True)  # Khóa chính
    userId = db.Column(db.String(100))  # userId, kiểu dữ liệu là String
    timeCheck = db.Column(db.Date)  # Thay String bằng Date nếu lưu ngày tháng
    typeCheck = db.Column(db.Integer)  # typeCheck không cần unique, chỉ cần lưu trạng thái

    @classmethod
    def get_all_attendances(cls):
        """Lấy tất cả bản ghi từ bảng attendance."""
        return cls.query.all()

    @classmethod
    def get_attendance_by_id(cls, attendance_id):
        """Lấy thông tin chấm công theo ID."""
        return cls.query.get(attendance_id)
