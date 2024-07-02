

# ArucoDetection
## Authors: 
Sahar Tuvyahu\
Yehonatan Baruchson\
Guy Gur-Arieh\
Harel Giladi


## Abstract:
This project focuses on detecting QR codes within a given video. The task involves identifying QR codes in each frame of the video and extracting the following parameters:

* QR ID (a number between 0 and 1023)
* QR 2D Information: The four corner points (in frame coordinates)\
* QR 3D Information: Distance to the camera, yaw angle with respect to the camera's "lookAt" point

The output is required in two formats: 

* CSV: Containing frame ID, QR ID, QR 2D coordinates, and QR 3D information
* Annotated Video: Each detected QR code marked with a green rectangular frame and its ID

## Requirements
### Hardware
* Computer with capabilities to run real-time video processing
### Software
* Python 3.x
* OpenCV
* Numpy
* Pandas
### Input
* Video file: TelloAIv0.0_video.mp4
### Output
* CSV file with QR detection data
* Annotated video with detected QR codes
## Getting Started
### Prerequisites
* Install Python 3.x from python.org.
Install the required Python packages using pip:
![image](https://github.com/s4646/ArucoDetection/assets/93948749/f8fca3da-d0ae-4740-b7e2-db8ef1a811ff)

### Camera Specifications
* Resolution: 720p (1280x720, 30 fps)
* Field of View (FoV): 82.6 degrees
* Calibration parameters are available here.
 
## Instructions
### Clone the Repository:
![image](https://github.com/s4646/ArucoDetection/assets/93948749/ca8e0d73-f88f-4a0d-94b0-b29edc3ffe29)

### Run the Script:

![image](https://github.com/s4646/ArucoDetection/assets/93948749/99abf781-4857-4c37-ad03-7193b79dba96)

## Code Explanation
### Aruco_detection.py
This script includes functions for detecting QR codes and calculating their 2D and 3D coordinates. Key functionalities include:
* Loading camera calibration parameters.
* Detecting QR codes using OpenCV’s QRCodeDetector.
* Extracting 2D corner coordinates and calculating 3D information (distance, yaw).
### Drone.py
Manages the connection and video stream from the Tello drone. It provides functions to:
* Connect to the drone.
* Capture video frames in real-time.
* Handle video feed disconnections and reconnections.
### main.py
The main script that orchestrates the overall detection process. It:
* Initializes the drone connection and video capture.
* Processes each video frame to detect QR codes.
*  Records detection data to a CSV file.
*  Annotates and saves the video with detected QR codes.
### safethread.py
Provides threading utilities to handle video capture and processing concurrently, ensuring real-time performance.
### test.py
Includes unit tests to validate the functionality of QR detection and 3D calculations.
## Output Formats
### CSV:
![image](https://github.com/s4646/ArucoDetection/assets/93948749/f21a2bec-2578-48f3-b025-d078cb401774)






* Annotated Video: Each detected QR code is marked with a green rectangular frame displaying its ID.
## Example Output
### CSV
![image](https://github.com/s4646/ArucoDetection/assets/93948749/2ae91251-8eb7-49ab-b676-304f0d2b4bb0)

### Annotated Video
* Each frame with detected QR codes marked and ID displayed.
 
## Performance
The code is designed to process each frame in less than 30 ms to ensure real-time performance.
## Testing
* Use the provided video file TelloAIv0.0_video.mp4 for testing.
* Verify the CSV output and the annotated video for accuracy.
## Acknowledgements
* Class examples from 9/6/2024
* Tello camera specifications and calibration parameters

