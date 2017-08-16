import requests


class WebService:
    endPoint = 'http://192.168.0.21/'
    sendScript = 'test.php'

    def get_url_to_send(self):
        return self.endPoint + self.sendScript

    def send(self, file):
        files = {'file': open(file, 'rb')}
        requests.post(self.get_url_to_send(), files=files)
