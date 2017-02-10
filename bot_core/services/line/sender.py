import json
from abc import abstractmethod

import requests


class LineSender:
    def __init__(self, settings):
        self.settings = settings

    def reply(self, data):
        url = self.settings["url_prefix"] + "/message/reply"

        # ヘッダの追加
        headers = self.settings["header"]

        json_data = json.dumps(data)
        print(json_data)
        response = requests.post(url, data=json_data, headers=headers)
        print(response.json())
        print("send finished.")

    def content(self, id):
        url = self.settings["url_prefix"] + "/message/{}/content".format(id)

        headers = self.settings["header"]
        response = requests.get(url, headers=headers)
        print(response.status_code)
        print(response.content)
        return response.content
