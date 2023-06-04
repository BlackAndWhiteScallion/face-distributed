import cv2

capture = cv2.VideoCapture('/home/student/Downloads/face-distributed-main/main/500_00277_preview.mp4')
 
frameNr = 0
 
while (True):
 
        success, frame = capture.read()
 
        if not success:
            break
 
        cv2.imwrite(f'/home/student/Downloads/face-distributed-main/main/output/{frameNr}.jpg', frame)
 
        frameNr = frameNr+1
 
capture.release()
