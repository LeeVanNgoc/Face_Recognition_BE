from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from config.config import Config
from User.model import db, User
from sqlalchemy import inspect, text  # Thêm import 'inspect' từ sqlalchemy
from User.route import user_bp 

# Load .env variables
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Khởi tạo CORS
CORS(app)

# Kết nối Flask với SQLAlchemy
db.init_app(app)  # Đảm bảo db.init_app(app) được gọi sau khi tạo ứng dụng Flask

# Thay vì sử dụng `before_first_request`, bạn sẽ sử dụng `before_request`
@app.before_request
def create_tables():
    # Sử dụng inspect để kiểm tra bảng 'user' có tồn tại không
    inspector = inspect(db.engine)  # Tạo đối tượng inspector từ engine
    if 'user' not in inspector.get_table_names():  # Kiểm tra nếu bảng 'user' không có
        db.create_all()  # Tạo bảng nếu chưa có

@app.route("/test-db")
def test_db():
    try:
        # Đảm bảo câu truy vấn được bao bọc bởi text()
        db.session.execute(text('SELECT 1'))  # Phải sử dụng text() như thế này
        return jsonify({"status": "OK"})
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})
    
@app.route("/api/debug_users")
def debug_users():
    users = User.query.all()
    return f"Found {len(users)} users: {[user.name for user in users]}"

@app.route("/api/debug_add_users")
def debug_add_users():
    user1 = User(id="1", name="Aozama", email="lee.admin@gmail.com", phone="1")
    user2 = User(id="2", name="Aozama 2", email="lee.admin@gmail.com", phone="0934287342")
    user3 = User(id="3", name="Aozama3", email="lee.admin3@gmail.com", phone="0934287342")
    db.session.add_all([user1, user2, user3])
    db.session.commit()
    return "3 users added"

    
app.register_blueprint(user_bp, url_prefix='/api')

if __name__ == "__main__":
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_RUN_PORT", 5000))
    debug = os.getenv("FLASK_ENV", "production") == "development"
    app.run(host=host, port=port, debug=debug)
