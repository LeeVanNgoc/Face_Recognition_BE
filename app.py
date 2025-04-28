from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from config import Config
from User.model import db, User
from sqlalchemy import inspect, text
from User.route import user_bp
from Attendance.route import attendance_bp
from recognition.routes import recognition_bp
import numpy as np

# Load .env variables
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Khởi tạo CORS
CORS(app)

# Kết nối Flask với SQLAlchemy
db.init_app(app)

@app.before_request
def create_tables():
    inspector = inspect(db.engine)
    if 'user' not in inspector.get_table_names():
        db.create_all()

@app.route("/test-db")
def test_db():
    try:
        db.session.execute(text('SELECT 1'))
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
    db.session.add_all([user1, user2])
    db.session.commit()
    return "Users added"

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(attendance_bp, url_prefix='/api')
app.register_blueprint(recognition_bp, url_prefix='/api')

if __name__ == "__main__":
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_RUN_PORT", 5000))
    debug = os.getenv("FLASK_ENV", "production") == "development"
    app.run(host=host, port=port, debug=debug)
