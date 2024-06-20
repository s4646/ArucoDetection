import threading
from typing import List
import cv2
import argparse
import sys
from math import atan2, cos, sin, sqrt, pi
import numpy as np
import safethread
import imutils
import time

class ArucoDetection:

    def __init__(self, aruco_dict):
        
        self.img = None
        self.ARUCO_DICT = aruco_dict
        self.corners = []
        self.ids = []
        self.contours = []

        self.id_2_area = {
            "0": 100000,
            "1": 100000,
            "2": 100000, 
            "3": 100000, 
            "4": 100000,
            "5": 100000,
            "6": 100000,
            "7": 100000,
            "8": 100000, 
            "9": 100000, 
        }

        self.id_2_centerPoint = {
            "0": [],
            "1": [],
            "2": [], 
            "3": [], 
            "4": [],
            "5": [],
            "6": [],
            "7": [],
            "8": [], 
            "9": [], 
        }

        self.ticker = threading.Event()
        # processing frequency (to spare CPU time)
        self.cycle_counter = 1
        self.cycle_activation = 10


        # self.detection = safethread.SafeThread(target=self.detect_aruco).start()
        # self.orientation = safethread.SafeThread(target=self.getOrientation_detection).start()


    def set_image_to_process(self, img):
        """Image to process

        Args:
            img (nxmx3): RGB image
        """
        self.img = img

    def getOrientation(self, pts):
        ## [pca]
        # Construct a buffer used by the pca analysis
        sz = len(pts)
        data_pts = np.empty((sz, 2), dtype=np.float64)
        for i in range(data_pts.shape[0]):
            data_pts[i,0] = pts[i,0,0]
            data_pts[i,1] = pts[i,0,1]
        
        # Perform PCA analysis
        mean = np.empty((0))
        mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_pts, mean)
        
        angle = atan2(eigenvectors[0,1], eigenvectors[0,0]) # orientation in radians
        
        return -int(np.rad2deg(angle))

    def getOrientation_detection(self):
        """
            This method finds the contours in the image
        """
        # time base
        self.ticker.wait(0.005)

        if self.img is not None:
            image = self.img.copy()
        
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
            # Convert image to binary
            _, bw = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            
            # Find all the contours in the thresholded image
            contours, _ = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

            self.contours = contours
        
        self.cycle_counter += 1
    
    def detect_aruco(self):
        """
            This method detect ArUco code from all types.
            It detect its Value, Boundaries, Center point and type.
            it return an image with the draws.
        """
        # time base
        self.ticker.wait(0.005)

        if self.img is not None:
            img = self.img.copy()

            image = imutils.resize(img, width=720)
            # load the ArUCo dictionary, grab the ArUCo parameters, and detect
            # the markers
            center = (720/2, 540/2)
            # print(center)

            corners_list = []
            ids_list = []
            self.id_2_centerPoint = {
                "0": [],
                "1": [],
                "2": [], 
                "3": [], 
                "4": [],
                "5": [],
                "6": [],
                "7": [],
                "8": [], 
                "9": [], 
            }

            # for dict in self.ARUCO_DICT:
            # arucoDict = cv2.aruco.Dictionary_get(self.ARUCO_DICT[self.args.type])
            # arucoDict = cv2.aruco.Dictionary_get(self.ARUCO_DICT["DICT_4X4_100"])
            arucoParams = cv2.aruco.DetectorParameters()
            arucoDict = cv2.aruco.ArucoDetector(cv2.aruco.getPredefinedDictionary(self.ARUCO_DICT["DICT_4X4_100"]), arucoParams)
            (corners, ids, rejected) = arucoDict.detectMarkers(image)
            if ids is not None:
                for c, i in zip(corners, ids):
                    ids_list.append(i)
                    corners_list.append(c)
                    c = c[0]
                    centerY = int((c[0][1] + c[1][1]) / 2)
                    centerX = int((c[0][0] + c[1][0]) / 2)
                    # print(centerX, centerY)
                    self.id_2_centerPoint[str(i[0])] = (centerX, centerY)
                    # print("Code: ", i , " Coords: ", c)
                    
            self.ids = ids_list
            self.corners = corners_list
        
        self.cycle_counter +=1


    def draw_detection(self):
        """
            This method draw the latest detections on the given image.
        """
        # contours = self.contours
        angles = []
        areas = []
        self.id_2_area = {
            "0": 100000,
            "1": 100000,
            "2": 100000, 
            "3": 100000, 
            "4": 100000,
            "5": 100000,
            "6": 100000,
            "7": 100000,
            "8": 100000, 
            "9": 100000, 
        }

        for i, (id, c) in enumerate(zip(self.ids, self.corners)):
        
            # Calculate the area of each contour
            area = cv2.contourArea(c)
            areas.append(area)
            
            # Find the orientation of each shape
            angle = self.getOrientation(c)
            angles.append(angle)

            self.id_2_area[str(id[0])] = area

        

        return self.ids, self.corners, angles, self.id_2_area, self.id_2_centerPoint

ARUCO_DICT = {
            "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
            "DICT_4X4_100": cv2.aruco.DICT_4X4_100,     # the one we use!
            "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
            "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
            "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
            "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
            "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
            "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
            "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
            "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
            "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
            "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
            "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
            "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
            "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
            "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
            "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
            "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
            "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
            "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
            "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
        }