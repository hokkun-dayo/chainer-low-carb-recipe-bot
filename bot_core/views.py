# coding: utf-8

import base64
import hashlib
import hmac
import json

from rest_framework import views
from rest_framework.response import Response

from bot_core.tasks import reply_message


class MessageTaskSet(views.APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.line_setting = json.load(open("bot_core/line_setting.json"))
        self.channel_secret = self.line_setting["channel_secret"].encode('utf-8')

    def get(self, request):
        return Response("Hello, GET request!")

    def post(self, request):
        body = request.body.decode("utf-8").encode('utf-8')
        hash_string = hmac.new(self.channel_secret,
                               body,
                               hashlib.sha256).digest()
        signature = base64.b64encode(hash_string).decode('utf-8')
        try:
            if signature != request.META["HTTP_X_LINE_SIGNATURE"]:
                print("signature is not corrected c:{}, h:{}".format(signature,
                                                                     request.META["HTTP_X_LINE_SIGNATURE"]))
                return Response("signature is not corrected")
        except Exception:
            return Response("cant get signature header")

        # 非同期にreplyをします。
        reply_message.delay(request.data["events"][0])

        return Response("")
