from scipy.spatial.distance import cosine

def find_best_match(embedding, faces_db, names_db, threshold=0.5):
    min_dist = float('inf')
    best_match = "Unknown"

    for idx, stored_embedding in enumerate(faces_db):
        dist = cosine(embedding, stored_embedding)
        if dist < min_dist:
            min_dist = dist
            best_match = names_db[idx]

    if min_dist > threshold:
        best_match = "Unknown"

    return best_match, min_dist
