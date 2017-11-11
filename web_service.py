import time

import requests
import uuid


class WebService:
    # endPoint = 'http://vigilemos.com/'
    # sendScript = 'uploadFile'

    endPoint = 'http://192.168.0.21/Github/vigilemos/'
    sendScript = 'uploadFile'

    videoName = 'output'

    @staticmethod
    def get_milli_seconds():
        return int(round(time.time() * 1000))

    def get_url_to_send(self):
        return self.endPoint + self.sendScript

    @staticmethod
    def get_mac():
        mac_num = hex(uuid.getnode()).replace('0x', '').upper()
        mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
        return mac

    def send(self, file):
        files = {'upload_file': open(file, 'rb')}

        data = {'name': WebService.get_mac(), 'time': WebService.get_milli_seconds()}

        try:
            r = requests.post(self.get_url_to_send(), files=files, data=data)

            print(r.text)

            if not r.status_code // 100 == 2:
                return "Error: Unexpected response {}".format(r)
            return r.status_code
        except requests.exceptions.RequestException as e:
            return "Error: {}".format(e)
