import cv2

camera = cv2.VideoCapture()
camera_active = False

def activate_camera():
    """
    Activates the robot camera
    """
    global camera
    global camera_active
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    camera_active = True

def get_camera_image():
    """
    Retrieves current image from robot camera or video
    Returns none if the video is done or camera failed
    """
    global camera
    global camera_active
    if not camera_active:
        raise Exception("Camera is not active. Call vision.activate_camera() or vision.load_video()")
    _, img = camera.read()
    return img
