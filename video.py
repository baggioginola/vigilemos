import os

import cv2

from web_service import WebService


class Video:
    ext = '.avi'
    videoName = 'output'
    path = ''

    def __init__(self, num_recorded_videos=0):
        self.videoFile = Video.get_video_name(num_recorded_videos)
        self.deleteExistingFile()
        self.setVideoWriterObject()

    def saveVideo(self, frame):
        self.out.write(frame)

    @staticmethod
    def send_video(num_recorded_videos):
        web_service = WebService()
        response = web_service.send(Video.get_video_name(num_recorded_videos))
        Video.deleteVideoFile(num_recorded_videos)

    def setCodec(self):
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

    def setVideoWriterObject(self):
        self.setCodec()
        self.out = cv2.VideoWriter(self.videoFile, self.fourcc, 20.0, (640, 480))

    @staticmethod
    def get_video_name(num_recorded_videos):
        videoName = 'output'
        extension = '.avi'
        return videoName + str(num_recorded_videos) + extension

    def deleteExistingFile(self):
        if os.path.isfile(self.videoFile):
            os.remove(self.videoFile)

    @staticmethod
    def deleteVideoFile(num_recorded_videos):
        if os.path.isfile(Video.get_video_name(num_recorded_videos)):
            os.remove(Video.get_video_name(num_recorded_videos))

    def release(self):
        self.out.release()

    def __del__(self):
        self.out.release()
