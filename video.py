import os

import cv2
from ffmpy import FFmpeg

from web_service import WebService


class Video:
    conf = None
    path = ''
    codec = None
    out = None

    def __init__(self, conf):
        self.conf = conf
        self.delete_files()
        self.set_video_writer_object()

    def save_video(self, frame):
        self.out.write(frame)

    def send_video(self):
        web_service = WebService()
        self.convert_avi_to_mp4()
        web_service.send(self.conf['video_converted'])
        self.delete_files()

    def set_codec(self):
        self.codec = cv2.VideoWriter_fourcc(*'XVID')

    def set_video_writer_object(self):
        self.set_codec()
        self.out = cv2.VideoWriter(self.conf['video'], self.codec, 20.0, (640, 480))

    def convert_avi_to_mp4(self):
        ff = FFmpeg(inputs={self.conf['video']: None}, outputs={self.conf['video_converted']: None})
        ff.run()
        return True

    def delete_files(self):
        if os.path.isfile(self.conf['video']):
            os.remove(self.conf['video'])
        if os.path.isfile(self.conf['video_converted']):
            os.remove(self.conf['video_converted'])

    def release(self):
        self.out.release()

    def __del__(self):
        self.out.release()
