import cv2
import pyvirtualcam

class Camera:

    def __init__(self, camera_id = 1, show_preview = False):
        self.cam = cv2.VideoCapture(camera_id)
        self.virtual_cam = pyvirtualcam.Camera(width=int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)), height=int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)), fps=30)

        if self.cam.isOpened():
            rval, self.frame = self.cam.read()
        else:
            rval = False
        
        while rval:
            if show_preview: cv2.imshow("window", self.frame)
            rval, self.frame = self.cam.read()

            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                break
            else:

                cv2.line(img=self.frame, pt1=(10,10), pt2=(100,100), color=(255,0,0), thickness=5, lineType=8, shift=0)
                self.virtual_cam.send(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))
                self.virtual_cam.sleep_until_next_frame()
        
        self.cam.release()
        cv2.destroyWindow("window")

    
    def get_frame(self):
        return self.frame


    