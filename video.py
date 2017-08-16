import cv2
import os

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
        web_service.send(Video.get_video_name(num_recorded_videos))

    def setCodec(self):
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

    def setVideoWriterObject(self):
        self.setCodec()
        self.out = cv2.VideoWriter(self.videoFile, self.fourcc, 20.0, (640, 480))

    @staticmethod
    def get_video_name(num_recorded_videos):
        return 'output' + str(num_recorded_videos) + '.avi'

    def deleteExistingFile(self):
        if os.path.isfile(self.videoFile):
            os.remove(self.videoFile)

    def __del__(self):
        self.out.release()
