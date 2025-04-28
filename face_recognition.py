# face_recognition.py
import cv2
import pickle
import numpy as np
from insightface.app import FaceAnalysis
from scipy.spatial.distance import cosine

# Load model
app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0, det_size=(640, 640))

# Load data
with open('dataset1/faces.pkl', 'rb') as f:
    faces_db = pickle.load(f)
with open('dataset1/names.pkl', 'rb') as f:
    names_db = pickle.load(f)

def recognize_face(image_np):
    faces = app.get(image_np)
    results = []

    for face in faces:
        embedding = face.embedding
        min_dist = float('inf')
        best_match = "Unknown"

        for idx, stored_embedding in enumerate(faces_db):
            dist = cosine(embedding, stored_embedding)
            if dist < min_dist:
                min_dist = dist
                best_match = names_db[idx]

        if min_dist > 0.5:
            best_match = "Unknown"

        results.append({
            'name': best_match,
            'bbox': [int(x) for x in face.bbox]
        })

    return results
