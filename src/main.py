import cv2
import os
import math
from time import sleep
import time
import shutil
import sys

sys.path.append(os.path.join(os.getcwd(), "config"))

from cfg import *



from v_cam import VirtualCamera
from detector import Detector 


class Webcam():
    def __init__(self, width=1280, height=720, cam_id=0) -> None:
        self.cap = cv2.VideoCapture(cam_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.width = width
        self.height = height

def init_video(video_path):
    tmp_dir = "tmp"
    if not os.path.isdir(tmp_dir):
        os.mkdir("./tmp")
    if not os.path.exists(video_path):
        with open(video_path, 'w') as fp: pass


cam = Webcam()
detector = Detector()
v_cam = VirtualCamera(width=cam.width, height=cam.height, fps=30)

init_video(video_path=v_path)
fourcc = cv2.VideoWriter_fourcc('X','V','I','D')


video = cv2.VideoCapture(v_path)
ret, frame = cam.cap.read()

while cam.cap.isOpened():
    time_elapsed = time.time() - prev
    key =  cv2.waitKey(15)

    if key == 27:
        break


    color = (0, 255, 0) 
    ret, frame = cam.cap.read()
    frame = cv2.flip(frame, 1)
    frame_copy = frame.copy()
    
    if key == ord('r'):
        x_ref, y_ref = x, y
        cv2.imwrite("tmp/tmp_capture.png", frame)
        start = cv2.imread("tmp/tmp_capture.png")
        record = ~record
        frame = cv2.addWeighted(frame, 0.5, start, 0.5, 1)
        fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
        if record:
            videoWriter = cv2.VideoWriter(v_path, fourcc, 30.0, (cam.width, cam.height))
        else:
            videoWriter.release()
    if key == ord("p"):
        try:
            ret_video, frame_video = video.read()
            cv2.imwrite("tmp/tmp_start.png", frame_video)
        except:
            pass
        sleep(1)
        play = ~play
        x_ref, y_ref = x, y


    frame.flags.writeable = False
    results = detector.detect(frame)
    frame.flags.writeable = True

    try:
        x, y = detector.calculate_xy(results)
    except:
        pass

    if record:
        contrast = cv2.bitwise_not(start)
        frame = cv2.addWeighted(frame, 0.5, contrast, 0.5, 1)
        color = (0, 0, 255)
        videoWriter.write(frame_copy)
        dist = math.sqrt( (x - x_ref)**2 + (y - y_ref)**2 )
        
    if play:        
        if time_elapsed > 1./frame_rate:
            prev = time.time()
            try:
                ret_video, frame_video = video.read()
                contrast = cv2.bitwise_not(frame_video)
            except:
                print("No recording.")
            if ret_video:
                try:
                    dist = math.sqrt( (x - x_ref)**2 + (y - y_ref)**2 )
                except:
                    pass
                v_cam._send(frame_video)
            else:
                video = cv2.VideoCapture(v_path)
    else:
        v_cam._send(frame_copy)

    if play:
        try:
            frame = cv2.addWeighted(frame_copy, 0.5, contrast, 0.5, 1)
            dist = math.sqrt( (x - x_ref)**2 + (y - y_ref)**2 )
        except:
            pass    
    if not play and not record:
        try:
            video_start = cv2.imread("tmp/tmp_start.png")
            frame = cv2.addWeighted(frame_copy, 0.5, cv2.bitwise_not(video_start), 0.5, 1)
        except:
            pass

    cv2.putText(frame, f'DIST: {dist:.3f}', (350, 150), font, 
                    fontScale, color, thickness, cv2.LINE_AA)
    cv2.imshow("Realtime", cv2.resize(frame, (int(cam.width*0.5), int(cam.height*0.5)), interpolation = cv2.INTER_AREA))
    


cam.cap.release()
video.release()
videoWriter.release()
cv2.destroyAllWindows()
shutil.rmtree("./tmp")