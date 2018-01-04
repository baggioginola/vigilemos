import datetime
import json
import time

import cv2
import imutils

from video import Video
from web_service import WebService


class MotionDetection:
    conf = None
    video = None
    camera = None
    rawCapture = None
    firstFrame = None
    frame = None
    numRecordedVideos = 0
    framesRecorded = 0
    web_service = None

    def __init__(self, json_file='conf.json'):
        self.init_config(json_file)

    def init_config(self, json_file):
        with open(json_file) as json_data:
            self.conf = json.load(json_data)

    def initialize_web_service(self):
        self.web_service = WebService()

    def initialize_camera(self):
        # self.camera = PiCamera()
        # self.camera.resolution = tuple(self.conf["resolution"])
        # self.camera.framerate = self.conf["fps"]
        # self.rawCapture = PiRGBArray(self.camera, size=tuple(self.conf["resolution"]))
        self.camera = cv2.VideoCapture(0)
        time.sleep(self.conf['camera_warmup_time'])

    def initialize_video(self):
        self.video = Video(self.conf)

    def process_frames(self):
        avg = None

        self.initialize_web_service()
        while True:
            (grabbed, self.frame) = self.camera.read()
            text = "No crime"
            movement = False

            gray = self.set_gray()

            if avg is None:
                avg = gray.copy().astype("float")
                continue

            thresh = self.set_thresh(gray, avg)

            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if imutils.is_cv2() else cnts[1]

            # loop over the contours
            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) < self.conf["min_area"]:
                    continue

                # compute the bounding box for the contour, draw it on the frame, and update the text
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "Crime"
                movement = True

            # draw the text and timestamp on the frame
            cv2.putText(self.frame, "Room Status:{}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255),
                        2)
            cv2.putText(self.frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, self.frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            cv2.imshow("Camera", self.frame)

            # camera_status = self.web_service.get_camera_status()

            camera_status = '1'

            if camera_status == '1':
                if movement:
                    self.video.save_video(self.frame)
                    self.framesRecorded += 1

                if self.framesRecorded == self.conf['fps']:
                    self.video.release()
                    self.video.send_video()
                    del self.video
                    self.initialize_video()
                    self.framesRecorded = 0

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                cv2.destroyAllWindows()
                self.camera.release()
                break

    def set_gray(self):
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        return gray

    def set_thresh(self, gray, avg):
        cv2.accumulateWeighted(gray, avg, 0.5)
        frame_delta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
        thresh = cv2.threshold(frame_delta, self.conf["delta_thresh"], 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        return thresh

    @staticmethod
    def set_contours(thresh):
        return cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


def main():
    motion_detection = MotionDetection()
    motion_detection.initialize_camera()
    motion_detection.initialize_video()
    motion_detection.process_frames()


if __name__ == "__main__":
    main()
