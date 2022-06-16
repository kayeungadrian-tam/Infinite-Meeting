import cv2
import os
import math
from time import sleep
import time
import shutil
import sys

from v_cam import VirtualCamera
from detector import Detector 

class Webcam():
    def __init__(self, width=1280, height=720, cam_id=0):
        self.cap = cv2.VideoCapture(cam_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.width = width
        self.height = height

    def test(self):
        pass


def init_video(video_path):
    try:
        shutil.rmtree("./tmp")
    except:
        pass
    tmp_dir = "tmp"
    if not os.path.isdir(tmp_dir):
        os.mkdir("./tmp")
    if not os.path.exists(video_path):
        with open(video_path, 'w') as fp: pass

def main():
    record, play = False, False
    v_path = 'tmp/tmp_video.avi'
    frame_rate = 60
    prev = 0
    font = cv2.FONT_HERSHEY_SIMPLEX  
    fontScale = 1   
    thickness = 2
    dist = -1

    cam = Webcam()
    detector = Detector()
    v_cam = VirtualCamera(width=cam.width, height=cam.height, fps=30)

    init_video(video_path=v_path)
    fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

    video = cv2.VideoCapture(v_path)
    ret, frame = cam.cap.read()

    prev = 0

    while cam.cap.isOpened():
        saved_size = os.path.getsize(v_path)
        if saved_size != 0:
            saved = True
            saved_color = (0, 255, 0)
        else:
            saved = False
            saved_color = (0, 0, 255)

        time_elapsed = time.time() - prev
        key =  cv2.waitKey(15)

        title = "Real_frame"

        if key == 27:
            break

        color = (0, 255, 0) 
        ret, frame = cam.cap.read()
        frame = cv2.flip(frame, 1)
        frame_copy = frame.copy()
        
        if key == ord('r'):
            x_ref, y_ref, z_ref = x, y, z
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
            x_ref, y_ref, z_ref = x, y, z

        
        if key ==32:
            time.sleep(3)
            play = False
            try:
                ret_video, frame_video = video.read()
                cv2.imwrite("tmp/tmp_start.png", frame_video)
            except:
                pass


        frame.flags.writeable = False
        results = detector.detect(frame)
        frame.flags.writeable = True

        try:
            x, y, z = detector.calculate_xy(results)
            # detector.plot(results)
        except:
            pass

        if record:
            title = "Recording"
            contrast = cv2.bitwise_not(start)
            frame = cv2.addWeighted(frame, 0.5, contrast, 0.5, 1)
            color = (0, 0, 255)
            videoWriter.write(frame_copy)
            dist = math.sqrt( (x - x_ref)**2 + (y - y_ref)**2 )

        if play:        
            title = "Playing"
            color = (255, 0 ,0)
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
                if os.path.exists("tmp/tmp_start.png"):
                    video_start = cv2.imread("tmp/tmp_start.png")
                frame = cv2.addWeighted(frame_copy, 0.5, cv2.bitwise_not(video_start), 0.5, 1)
                dist = math.sqrt( (x - x_ref)**2 + (y - y_ref)**2 )
            except:
                pass

        cv2.rectangle(frame, (0,0), (cam.width, 50), (122, 122, 122), -1)
        cv2.rectangle(frame, (0, cam.height), (cam.width, cam.height-50), (122, 122, 122), -1)
        cv2.putText(frame, " Record: 'r' | Switch mode: 'p' | Quit: 'ESC' |  Pause: 'Spacebar'", (50, cam.height-15), font, fontScale, (255, 255, 255), thickness, cv2.LINE_AA)
        cv2.putText(frame, f'Diff: ', (350, 30), font, 
                        fontScale, (255, 255, 255), thickness, cv2.LINE_AA)
        cv2.putText(frame, f'{dist:.3f}', (450, 30), font, 
                        fontScale, (216, 191, 216), thickness, cv2.LINE_AA)                
        cv2.putText(frame, 'Status: ', (5, 30), font, 
                        fontScale, (255, 255, 255), thickness, cv2.LINE_AA)
        cv2.putText(frame, f'{title}', (150, 30), font, 
                        fontScale, color, thickness, cv2.LINE_AA)
        cv2.putText(frame, f'Saved video: ', (650, 30), font, 
                            fontScale, (255, 255, 255), thickness, cv2.LINE_AA)
        cv2.putText(frame, f'{saved}', (900, 30), font, 
                            fontScale, saved_color, thickness, cv2.LINE_AA)

        cv2.imshow("Realtime", cv2.resize(frame, (int(cam.width*0.5), int(cam.height*0.5)), interpolation = cv2.INTER_AREA))
        

    cam.cap.release()
    video.release()
    if saved:
        videoWriter.release()
    shutil.rmtree("./tmp")
    cv2.destroyAllWindows()


main()