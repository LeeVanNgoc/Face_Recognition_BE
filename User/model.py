from datetime import datetime
from config import db

class User(db.Model):
    __tablename__ = 'user'  # 👉 tên bảng trong DB (tùy chọn, nếu không thì mặc định là `user`)
    
    id = db.Column(db.Integer, primary_key=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fullName = db.Column(db.String(500))
    gender = db.Column(db.String(1))
    email = db.Column(db.String(500), unique=True)
    password = db.Column(db.String(500), nullable=True)
    phone = db.Column(db.String(20), unique=True)
    address = db.Column(db.String(500))
    image = db.Column(db.Text)

    @classmethod
    def get_all_users(cls):
        """Lấy tất cả người dùng từ bảng user."""
        return cls.query.all()

    @classmethod
    def get_user_by_id(cls, user_id):
        """Lấy thông tin người dùng theo ID."""
        return cls.query.get(user_id)

    @classmethod
    def get_user_by_email(cls, email):
        """Lấy thông tin người dùng theo email."""
        return cls.query.filter_by(email=email).first()
