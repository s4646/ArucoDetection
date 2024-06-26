import os
import cv2
from Aruco_detection import ArucoDetection

def get_data(id, corners, angle, distance):
    data = f"{id},"
    
    for i in range(len(corners)):
        data += f"{int(corners[i][0])}:{int(corners[i][1])},"
    
    data += f"{distance},{angle}\n"
    
    return data

def main():

    vidcap = cv2.VideoCapture('challengeB.mp4')
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    detector = ArucoDetection()
    success = True
    count = 0
    f = open('output.csv', 'w')
    f.write("FrameID,QR_ID,QR_leftup,QR_rightup,QR_rightdown,QR_leftdown,Distance,Yaw\n")
    while success:
        success, image = vidcap.read()
        if success and count == 0:
            result = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(vidcap.get(3)), int(vidcap.get(4))))
        detector.set_image_to_process(image)
        detector.detect_aruco()
        ids, corners, centers, angles, distances = detector.get_detection()

        print("frame %d" % count)
        if len(ids) > 0:
            for i, id in enumerate(ids):
                data = get_data(id[0], corners[i], angles[i], distances[id[0]])
                f.write(f"{count},"+data)
        else:
            f.write(f"{count},-1,-1:-1,-1:-1,-1:-1,-1:-1,-1,0\n")  
        
        if success:
            image = detector.draw_detection()
            result.write(image)
            # cv2.imwrite("frames/frame%d.jpg" % count, image)
        count += 1
    
    f.close()
    result.release()
    vidcap.release()


if __name__ == '__main__':
    main()