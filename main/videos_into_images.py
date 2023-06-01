import cv2
import mediapipe
 
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands
 
capture = cv2.VideoCapture('C:/Users/N/Desktop/video.avi')
 
frameNr = 0
 
with handsModule.Hands() as hands:
 
    while (True):
 
        success, frame = capture.read()
 
        if not success:
            break
 
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
 
        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                drawingModule.draw_landmarks(frame, handLandmarks, handsModule.HAND_CONNECTIONS)
 
        cv2.imwrite(f'C:/Users/N/Desktop/output/frame_{frameNr}.jpg', frame)
 
        frameNr = frameNr+1
 
capture.release()