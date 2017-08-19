import datetime
import time
import cv2
import json

from video import Video


class MotionDetection:
    conf = None
    video = None
    camera = None
    firstFrame = None
    frame = None
    numRecordedVideos = 0
    framesRecorded = 0

    def __init__(self, json_file='conf.json'):
        self.init_config(json_file)

    def init_config(self, json_file):
        with open(json_file) as json_data:
            self.conf = json.load(json_data)

    def set_video_object(self):
        self.video = Video(self.numRecordedVideos)

    def set_camera_object(self):
        self.camera = cv2.VideoCapture(0)

    def initialize_camera(self):
        self.set_camera_object()
        time.sleep(self.conf['camera_warmup_time'])

    def initialize_video(self):
        self.set_video_object()

    def set_gray(self):
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        return gray

    def set_thresh(self, gray):
        cv2.accumulateWeighted(gray, self.firstFrame, 0.5)
        frame_delta = cv2.absdiff(gray, cv2.convertScaleAbs(self.firstFrame))
        thresh = cv2.threshold(frame_delta, self.conf["delta_thresh"], 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        return thresh

    @staticmethod
    def set_contours(thresh):
        return cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    def process_video(self):
        while True:
            (grabbed, self.frame) = self.camera.read()
            text = "Unoccupied"
            movement = False

            if not grabbed:
                break

            gray = self.set_gray()

            if self.firstFrame is None:
                self.firstFrame = gray.copy().astype("float")
                continue

            thresh = self.set_thresh(gray)

            (_, cnts, _) = MotionDetection.set_contours(thresh)

            # loop over the contours
            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) < self.conf["min_area"]:
                    continue

                # compute the bounding box for the contour, draw it on the frame, and update the text
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "Occupied"
                movement = True

            # draw the text and timestamp on the frame
            cv2.putText(self.frame, "Room Status:{}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255),
                        2)
            cv2.putText(self.frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, self.frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            cv2.imshow("Security Feed", self.frame)

            if movement:
                self.video.saveVideo(self.frame)
                self.framesRecorded += 1

            if self.framesRecorded == 16:
                del self.video
                Video.send_video(self.numRecordedVideos)
                self.numRecordedVideos += 1
                self.set_video_object()
                self.framesRecorded = 0

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
        self.camera.release()
        cv2.destroyAllWindows()


def main():
    motion_detection = MotionDetection()
    motion_detection.initialize_camera()
    motion_detection.initialize_video()
    motion_detection.process_video()


if __name__ == "__main__":
    main()
