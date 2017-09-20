import time

import requests


class WebService:
    # endPoint = 'http://vigilemos.com/'
    # sendScript = 'test_upload.php'

    endPoint = 'http://192.168.0.21/Github/vigilemos/'
    sendScript = 'uploadFile'

    videoName = 'output'

    @staticmethod
    def get_milli_seconds():
        return int(round(time.time() * 1000))

    def get_url_to_send(self):
        return self.endPoint + self.sendScript

    def send(self, file):
        files = {'upload_file': open(file, 'rb')}

        data = {'name': self.videoName, 'time': WebService.get_milli_seconds()}

        try:
            r = requests.post(self.get_url_to_send(), files=files, data=data)

            if not r.status_code // 100 == 2:
                return "Error: Unexpected response {}".format(r)
            return r.status_code
        except requests.exceptions.RequestException as e:
            return "Error: {}".format(e)
