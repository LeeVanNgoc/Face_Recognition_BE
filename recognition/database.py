import pickle
import os
import numpy as np

FACES_FILE = 'dataset1/faces.pkl'
NAMES_FILE = 'dataset1/names.pkl'

def load_database():
    if not os.path.exists(FACES_FILE) or not os.path.exists(NAMES_FILE):
        return np.array([]), []

    with open(FACES_FILE, 'rb') as f:
        faces_db = pickle.load(f)
    with open(NAMES_FILE, 'rb') as f:
        names_db = pickle.load(f)

    return faces_db, names_db

def save_to_database(embedding, name):
    faces_db, names_db = load_database()

    # Thêm mới
    faces_db = list(faces_db)
    names_db = list(names_db)
    faces_db.append(embedding)
    names_db.append(name)

    # Lưu lại
    with open(FACES_FILE, 'wb') as f:
        pickle.dump(faces_db, f)
    with open(NAMES_FILE, 'wb') as f:
        pickle.dump(names_db, f)
