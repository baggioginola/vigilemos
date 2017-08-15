import cv2
import os


class Video:
    def __init__(self, path="", file="numVideo.avi"):
        self.videoFile = path + file
        self.deleteExistingFile()
        self.setVideoWriterObject()

    def saveVideo(self, frame):
        self.out.write(frame)

    def setCodec(self):
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

    def setVideoWriterObject(self):
        self.setCodec()
        self.out = cv2.VideoWriter(self.videoFile, self.fourcc, 20.0, (640, 480))

    def deleteExistingFile(self):
        if os.path.isfile(self.videoFile):
            os.remove(self.videoFile)

    def __del__(self):
        self.out.release()

