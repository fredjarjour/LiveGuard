import cv2
from cv2 import CV_32F
import mediapipe as mp
import pandas as pd
import keyboard
import pickle
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, accuracy_score
from sklearn.preprocessing import LabelEncoder, StandardScaler

record = False

cam = cv2.VideoCapture(1)

mpHands = mp.solutions.hands
hands = mpHands.Hands() #ctrl click Hands to see fct manuel #by default False
mpDraw = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

dfColumns = ['Label']
for i in range(21):
    dfColumns.append(f'X{i}')
    dfColumns.append(f'Y{i}')
    dfColumns.append(f'Z{i}')
print(len(dfColumns))
df = pd.DataFrame(columns=dfColumns)

digit = 0

if cam.isOpened():
    rval, frame = cam.read()
else:
    rval = False

while rval:

    rval, frame = cam.read()

    width, height = frame.shape[1], frame.shape[0]
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks: #detect if there's a hand

        originX = results.multi_hand_landmarks[0].landmark[0].x
        originY = results.multi_hand_landmarks[0].landmark[0].y
        originZ = results.multi_hand_landmarks[0].landmark[0].z

        for handLms in results.multi_hand_landmarks: #for a single hand

            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS) #puts the dots + connections on the hand 21 landmarks
            cv2.imshow("window", frame)

            if record:
                new_landmarks = [digit]
                for id, lm in enumerate(handLms.landmark):
                    lm.x -= originX
                    lm.y -= originY
                    lm.z -= originZ

                    new_landmarks.append(lm.x)
                    new_landmarks.append(lm.y)
                    new_landmarks.append(lm.z)
                
                row = pd.DataFrame([new_landmarks], columns=dfColumns)
                df = pd.concat([df, row], ignore_index=True)


    if keyboard.is_pressed('r'):
        record = not record
        print(f"Recording: {record}")

    if keyboard.is_pressed('t'):
        print("Training")
        X = df.iloc[:,1:]
        X = X.values
        y = df.iloc[:,0]
        y.to_numpy()

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

        gb = GradientBoostingRegressor()
        model = GradientBoostingRegressor(n_estimators=600, min_samples_split= 8, min_samples_leaf= 1, max_features= 'sqrt', max_depth=4, learning_rate=0.01)
        model.fit(X_train, y_train)

        file = open("model.pkl", "wb") 
        pickle.dump(model, file)


    if keyboard.is_pressed('s'):
        df.to_csv('data.csv')
        print("Saved")

    if keyboard.is_pressed('l'):
        df = pd.read_csv('data.csv')
        print("Loaded")

    if keyboard.is_pressed('0'):
        print("set to 0")
        digit = 0

    if keyboard.is_pressed('1'):
        digit = 1
        print("set to 1")

    cv2.imshow("window", frame)

    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cam.release()
cv2.destroyWindow("window")
