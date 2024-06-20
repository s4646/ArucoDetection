from djitellopy import tello
from threading import Thread
import cv2
import queue
from Aruco_detection import ArucoDetection
from Aruco_detection import ARUCO_DICT
from pynput import keyboard
from pynput.keyboard import Key, KeyCode

class Drone():

    def __init__(self):
        
        self.me = tello.Tello()
        self.me.connect()
        self.me.streamon()
        
        self.cap: cv2.VideoCapture = cv2.VideoCapture(self.me.get_udp_video_address())
        self.q = queue.Queue()

        print("Battery percentage:", self.me.get_battery())
        self.video_thread = Thread(target=self.video)
        self.stream_thread = Thread(target=self.stream)
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.aruco = ArucoDetection(ARUCO_DICT)

        if self.me.get_battery() < 10:
            raise RuntimeError("Tello rejected attemp to takeoff due to low Battery")
        
        self.stream_thread.start()
        self.video_thread.start()
        self.listener.start()

        
        self.ids = []
        self.corners = []
        self.angles = []
        self.area = {}
        self.centerPoints = {}
        self.centerpoint = (360, 220) # (360, 270)

    def video(self):
        while True:
            try:
                image = self.q.get()
            except queue.Empty:
                continue
            self.aruco.set_image_to_process(image.copy())
            self.ids, self.corners, self.angles, self.area, self.centerPoints = self.aruco.draw_detection(image.copy())
            cv2.imshow("results", image)
            cv2.waitKey(1)
    
    def stream(self):
        while True:
            ret, frame = self.cap.read()
            if not self.q.empty():
                try:
                    self.q.get_nowait()
                except queue.Empty:
                    pass
            self.q.put(frame)
    
    def on_press(self, key):
        if key == KeyCode.from_char('e'):
            self.me.emergency()
        elif key == KeyCode.from_char('l'):
            self.me.land()
        elif key == KeyCode.from_char('b'):
            self.me.get_battery()

    
    def on_release(self,key):
        pass