import cv2
import math
import numpy as np

class ArucoDetection:

    def __init__(self):
        self.image = None
        self.ids = []
        self.angles = []
        self.contours = []

        self.id_center_dict = {
            0: [],
            1: [],
            2: [], 
            3: [], 
            4: [],
            5: [],
            6: [],
            7: [],
            8: [], 
            9: [], 
        }

        self.id_distance_dict = {
            0: [],
            1: [],
            2: [], 
            3: [], 
            4: [],
            5: [],
            6: [],
            7: [],
            8: [], 
            9: [], 
        }

    def set_image_to_process(self, image):
        """
        Sets image to process
        """
        self.image = image

    def getOrientation(self, id):
        """
        Compute angle of aruco with given ID
        """
        img_center = self.image.shape[1]//2, self.image.shape[0]//2 # (x, y)
        center = self.id_center_dict[id[0]]
        return math.degrees(math.atan2(-center[1]+img_center[1], center[0]-img_center[0])) # -y instead of y
    
    def detect_aruco(self):
        """
            This method detect ArUco code from all types.
            It detect its Value, Boundaries, Center point and type.
        """

        if self.image is not None:

            self.contours = []
            self.corners = []
            self.ids = []
            self.id_center_dict = {
                0: [],
                1: [],
                2: [], 
                3: [], 
                4: [],
                5: [],
                6: [],
                7: [],
                8: [], 
                9: [], 
            }

            arucoParams = cv2.aruco.DetectorParameters()
            arucoDict = cv2.aruco.ArucoDetector(cv2.aruco.getPredefinedDictionary(ARUCO_DICT["DICT_4X4_100"]), arucoParams)
            contours, ids, _ = arucoDict.detectMarkers(self.image)
            if ids is not None:
                for c, id in zip(contours, ids):
                    self.ids.append(id)
                    self.contours.append(c[0].astype(int))

                    centroid = self.contours[-1].mean(axis=0)
                    centerX = int(np.round(centroid[0]))
                    centerY = int(np.round(centroid[1]))
                    self.id_center_dict[id[0]] = centerX, centerY

    def get_detection(self):
        self.angles = []
        self.id_distance_dict = {
            0: [],
            1: [],
            2: [], 
            3: [], 
            4: [],
            5: [],
            6: [],
            7: [],
            8: [], 
            9: [], 
        }

        for id, contour in zip(self.ids, self.contours):
            angle = self.getOrientation(id)
            self.angles.append(angle)
                                                                                 #         object_height (in mm) * focal_length
            distance = ARUCO_HEIGHT*FOCAL_LENGTH / (contour[2][1]-contour[0][1]) # dist =  ------------------------------------- 
            self.id_distance_dict[id[0]] = abs(distance)                         #              object_height (in pixels)

        return self.ids, self.contours, self.id_center_dict, self.angles, self.id_distance_dict
    
    def draw_detection(self):
        cv2.drawContours(self.image, self.contours, -1, (0, 255, 0), 3)
        return self.image


CAMERA_MATRIX = np.array([[921.170702, 0.000000, 459.904354],
                          [0.000000, 919.018377, 351.238301],
                          [0.000000, 0.000000, 1.000000]])
DISTORTION = np.array([-0.033458, 0.105152, 0.001256, -0.006647, 0.000000])

FOCAL_LENGTH = (CAMERA_MATRIX[0][0] + CAMERA_MATRIX[1][1]) / 2

ARUCO_HEIGHT = 100 # approximately 1/3 of A4's height (in mm) 

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