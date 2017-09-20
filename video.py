import os

import cv2

from web_service import WebService


class Video:
    ext = '.avi'
    videoName = 'output'
    path = ''

    def __init__(self):
        self.videoFile = self.videoName + self.ext
        self.deleteExistingFile()
        self.setVideoWriterObject()

    def saveVideo(self, frame):
        self.out.write(frame)

    @staticmethod
    def send_video():
        web_service = WebService()
        web_service.send(Video.get_video_name())
        Video.deleteVideoFile()

    def setCodec(self):
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

    def setVideoWriterObject(self):
        self.setCodec()
        self.out = cv2.VideoWriter(self.videoFile, self.fourcc, 20.0, (640, 480))

    @staticmethod
    def get_video_name():
        videoName = 'output'
        extension = '.avi'
        return videoName + extension

    def deleteExistingFile(self):
        if os.path.isfile(self.videoFile):
            os.remove(self.videoFile)

    @staticmethod
    def deleteVideoFile():
        if os.path.isfile(Video.get_video_name()):
            os.remove(Video.get_video_name())

    def release(self):
        self.out.release()

    def __del__(self):
        self.out.release()
