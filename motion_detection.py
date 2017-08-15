import datetime
import time
import cv2
import json
import requests
from video import Video

def initConfig():
    with open('conf.json') as json_data:
        conf = json.load(json_data)
    return conf


def getVideoName(numRecordedVideos=0):
    videoName = 'output'
    extVideo = '.avi'
    numRecordedVideos = numRecordedVideos
    return videoName + str(numRecordedVideos) + extVideo

def sendVideo(file):
    url = 'http://192.168.0.21/test.php'
    files = {'file': open(file, 'rb')}
    r = requests.post(url, files=files)

conf = initConfig()

camera = cv2.VideoCapture(0)
time.sleep(conf["camera_warmup_time"])

firstFrame = None

numRecordedVideos = 0
video = Video("", getVideoName(numRecordedVideos))
framesRecorded = 0

while True:
    (grabbed, frame) = camera.read()
    text = "Unoccupied"
    movement = False

    if not grabbed:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if firstFrame is None:
        firstFrame = gray.copy().astype("float")
        continue

    cv2.accumulateWeighted(gray, firstFrame, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(firstFrame))
    thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if (cv2.contourArea(c) < conf["min_area"]):
            continue

        # compute the bounding box for the contour, draw it on the frame, and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"
        movement = True

    # draw the text and timestamp on the frame
    cv2.putText(frame, "Room Status:{}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    cv2.imshow("Security Feed", frame)

    if (movement == True):
        video.saveVideo(frame)
        framesRecorded += 1

    if (framesRecorded == 16):
        del video
        sendVideo(getVideoName(numRecordedVideos))
        numRecordedVideos += 1
        video = Video("", getVideoName(numRecordedVideos))
        framesRecorded = 0

    key = cv2.waitKey(1) & 0xFF

    if (key == ord("q")):
        break

camera.release()
cv2.destroyAllWindows()