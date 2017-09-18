import requests


class WebService:
    # endPoint = 'http://vigilemos.com/'
    # sendScript = 'test_upload.php'

    endPoint = 'http://192.168.0.21/'
    sendScript = 'test.php'

    def get_url_to_send(self):
        return self.endPoint + self.sendScript

    def send(self, file):
        files = {'file': open(file, 'rb')}

        try:
            r = requests.post(self.get_url_to_send(), files=files)

            if not r.status_code // 100 == 2:
                return "Error: Unexpected response {}".format(r)
            return r.status_code
        except requests.exceptions.RequestException as e:
            return "Error: {}".format(e)
