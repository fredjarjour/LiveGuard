import cv2
import pyvirtualcam
import mediapipe as mp
import numpy as np
import pandas as pd

class Camera:

    def __init__(self, camera_id = 1, show_preview = False):
        self.cam = cv2.VideoCapture(camera_id)
        self.virtual_cam = pyvirtualcam.Camera(width=int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)), height=int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)), fps=60)

        self.model = pd.read_pickle(r'model.pkl')

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands() #ctrl click Hands to see fct manuel #by default False
        self.mpDraw = mp.solutions.drawing_utils
        self.mp_holistic = mp.solutions.holistic

        if self.cam.isOpened():
            rval, self.frame = self.cam.read()
        else:
            rval = False
        
        while rval:
            rval, self.frame = self.cam.read()

            width, height = self.frame.shape[1], self.frame.shape[0]
            imgRGB = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(imgRGB)

            if results.multi_hand_landmarks: #detect if there's a hand
                
                originX = results.multi_hand_landmarks[0].landmark[0].x
                originY = results.multi_hand_landmarks[0].landmark[0].y
                originZ = results.multi_hand_landmarks[0].landmark[0].z

                for handLms in results.multi_hand_landmarks: #for a single hand
                    xCoords = []
                    yCoords = []
                    X_test = []

                    for id, lm in enumerate(handLms.landmark):
                        xCoords.append(lm.x)
                        yCoords.append(lm.y)

                        lm.x -= originX
                        lm.y -= originY
                        lm.z -= originZ
                        X_test.extend([lm.x, lm.y, lm.z])
                    
                    prediction = self.model.predict([X_test])
                    
                    print(prediction)
                    # mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS) #puts the dots + connections on the hand 21 landmarks
                    if prediction > 0.8:
                        border = 20
                        rectW = int((max(xCoords) - min(xCoords))*width) + border * 2
                        rectH = int((max(yCoords) - min(yCoords))*height) + border * 2
                        offsetX = int(min(xCoords)*width) - border
                        offsetY = int(min(yCoords)*height) - border   

                        try:
                            cropped = self.frame[offsetY:offsetY + rectH, offsetX:offsetX + rectW]
                            temp = cv2.resize(cropped, (rectW // 20, rectW // 20), interpolation = cv2.INTER_LINEAR)
                            temp2 = cv2.resize(temp, (rectW, rectH), interpolation = cv2.INTER_NEAREST)
                            self.frame[offsetY:offsetY + rectH, offsetX:offsetX + rectW] = temp2
                        except Exception:
                            pass

            cv2.imshow("LiveGuard", self.frame)

            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                break
            else:
                self.virtual_cam.send(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))
                self.virtual_cam.sleep_until_next_frame()
        
        self.cam.release()
        cv2.destroyAllWindows()

    
    def get_frame(self):
        return self.frame


    