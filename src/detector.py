import mediapipe as mp

class Detector():
    def __init__(self) -> None:
        mp_pose = mp.solutions.pose
        self.pose =  mp_pose.Pose(static_image_mode=False, model_complexity=2, enable_segmentation=False, min_detection_confidence=0.5) 

    def detect(self, image):
        self.result = self.pose.process(image)
        self.height, self.width, _ = image.shape
        return self.result 

    def calculate_xy(self, result):
        if result.pose_landmarks:
            x, y, z = 0, 0, 0
            for idx in [0, 11, 12]:
                x += result.pose_landmarks.landmark[idx].x 
                y += result.pose_landmarks.landmark[idx].y
                z += result.pose_landmarks.landmark[idx].z

            x = x*self.width/3
            y = y*self.height/3
            z = z/3

        return x, y, z

    def plot(self, result):
        if result.pose_landmarks:
            for idx in [0, 11, 12]:
                x = result.pose_landmarks.landmark[idx].x
                y = result.pose_landmarks.landmark[idx].y
                z = result.pose_landmarks.landmark[idx].z

            print(x, y, z, end="\r")
