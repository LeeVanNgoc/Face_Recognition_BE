from config.config import db
class User(db.Model):
    __tablename__ = 'user'  # 👉 tên bảng trong DB (tùy chọn, nếu không thì mặc định là `user`)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(120), unique=True)

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
