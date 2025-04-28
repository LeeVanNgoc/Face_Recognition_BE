# config.py
import os
from flask_sqlalchemy import SQLAlchemy

# Đường dẫn lưu trữ dữ liệu
DATASET_PATH = 'dataset1/'
FACES_FILE = os.path.join(DATASET_PATH, 'faces.pkl')
NAMES_FILE = os.path.join(DATASET_PATH, 'names.pkl')

# Mô hình InsightFace (ArcFace)
MODEL_NAME = 'buffalo_l'

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:''@localhost/facerecognition' # Hoặc MySQL/PostgreSQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy()