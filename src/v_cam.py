import pyvirtualcam
import cv2

class VirtualCamera():
    def __init__(self, width, height, fps) -> None:
        self.v_cam = pyvirtualcam.Camera(width=width, height=height, fps=fps)

    def _send(self, image):
        # image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.v_cam.send(image)
        self.v_cam.sleep_until_next_frame()
