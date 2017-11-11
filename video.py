import os

import cv2
from ffmpy import FFmpeg

from web_service import WebService


class Video:
    ext = '.avi'
    videoName = 'output'
    path = ''

    def __init__(self):
        Video.delete_video_file()
        self.videoFile = self.videoName + self.ext
        self.set_video_writer_object()

    def saveVideo(self, frame):
        self.out.write(frame)

    @staticmethod
    def send_video():
        web_service = WebService()
        Video.convert_avi_to_mp4()
        web_service.send(Video.get_mp4_video())
        Video.delete_video_file()

    def set_codec(self):
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

    def set_video_writer_object(self):
        self.set_codec()
        self.out = cv2.VideoWriter(self.videoFile, self.fourcc, 20.0, (640, 480))

    @staticmethod
    def get_avi_video():
        video_name = 'output'
        extension = '.avi'
        return video_name + extension

    @staticmethod
    def get_mp4_video():
        video_name = 'output'
        extension = '.mp4'
        return video_name + extension

    @staticmethod
    def convert_avi_to_mp4():
        ff = FFmpeg(inputs={Video.get_avi_video(): None}, outputs={Video.get_mp4_video(): None})
        ff.run()
        return True

    @staticmethod
    def delete_video_file():
        if os.path.isfile(Video.get_avi_video()):
            os.remove(Video.get_avi_video())
        if os.path.isfile(Video.get_mp4_video()):
            os.remove(Video.get_mp4_video())

    def release(self):
        self.out.release()

    def __del__(self):
        self.out.release()
