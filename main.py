from camera import Camera
from threading import Thread
import mic

if __name__ == '__main__':

    # microphone = Thread(target=mic.main())
    # microphone.start()
    # print("hi")
    cam = Camera(1, True)