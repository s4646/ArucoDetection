import cv2
import math
from Aruco_detection import ARUCO_DICT
from Aruco_detection import ArucoDetection

CENTER = None

def get_data(id, corners, center):
    data = f"{id},"
    
    for i in range(len(corners[0])):
        data += f"{int(corners[0][i][0])}:{int(corners[0][i][1])},"
    
    data += f"{math.degrees(math.atan2(CENTER[1]-center[1], center[0]-CENTER[0]))}\n" # -y instead of y
    
    return data

def main():

    global CENTER
    vidcap = cv2.VideoCapture('challengeB.mp4')
    detector = ArucoDetection(ARUCO_DICT)
    success = True
    count = 0
    f = open('output.csv', 'w')
    f.write("FrameID,QR_ID,QR_leftup,QR_rightup,QR_rightdown,QR_leftdown,Yaw\n")
    while success:
        success,image = vidcap.read()
        if CENTER == None: CENTER = image.shape[1]//2, image.shape[0]//2
        detector.set_image_to_process(image)
        detector.detect_aruco()
        ids, corners, angles, areas, centers = detector.draw_detection()

        print("frame %d" % count)
        # print(f"ids: {ids}, corners:{corners}, angles: {angles}, areas: {areas}, centers: {centers}")
        if len(ids) > 0:
            for i, id in enumerate(ids):
                data = get_data(id[0], corners[i], centers[str(id[0])])
                f.write(f"{count},"+data)
        else:
            f.write(f"{count},-1,-1:-1,-1:-1,-1:-1,-1:-1,0\n")  
        
        count += 1
    f.close()


if __name__ == '__main__':
    main()