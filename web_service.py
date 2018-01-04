import time
import uuid

import requests


class WebService:
    # endPoint = 'http://seguridadcolectiva.mx/'
    # sendScript = 'uploadFile'

    endPoint = 'http://localhost/Github/seguridadcolectiva/'
    sendScript = 'uploadFile'
    statusCameraRoute = 'subscriber/cameras/getStatus'

    def set_route(self, route):
        return self.endPoint + route

    def send(self, file):
        files = {'upload_file': open(file, 'rb')}

        data = {'name': WebService.get_mac(), 'time': WebService.get_milli_seconds()}

        try:
            r = requests.post(self.set_route(self.sendScript), files=files, data=data)

            if not r.status_code // 100 == 2:
                return "Error: Unexpected response {}".format(r)
            return r.status_code
        except requests.exceptions.RequestException as e:
            return "Error: {}".format(e)

    def get_camera_status(self):
        data = {'mac_address': WebService.get_mac()}

        try:
            r = requests.get(self.set_route(self.statusCameraRoute), params=data)

            if not r.status_code // 100 == 2:
                return "Error: Unexpected response {}".format(r)
            return r.text
        except requests.exceptions.RequestException as e:
            return "Error: {}".format(e)

    @staticmethod
    def get_mac():
        mac_num = hex(uuid.getnode()).replace('0x', '').upper()
        mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
        return mac

    @staticmethod
    def get_milli_seconds():
        return int(round(time.time() * 1000))
