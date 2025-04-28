import cv2

def open_camera():
    """
    Mở camera và trả về đối tượng VideoCapture.
    """
    return cv2.VideoCapture(0)

def save_last_frame(frame, file_path='static/last_frame.jpg'):
    """
    Lưu ảnh cuối cùng vào một file.
    """
    cv2.imwrite(file_path, frame)
