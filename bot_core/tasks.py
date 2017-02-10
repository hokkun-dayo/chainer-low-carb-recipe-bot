from __future__ import absolute_import, unicode_literals

import json

from celery import shared_task

from bot_core.services.line.sender import LineSender
from bot_core.services.handler.message_response_processor \
    import TextMessageResponseProcessor, ImageMessageResponseProcessor
from bot_core.services.recognition.food_recognizer import Recognizer

line_setting = json.load(open("bot_core/line_setting.json"))
sender = LineSender(line_setting)
recognizer = Recognizer("bot_core/services/recognition/mean.npy",
                        "bot_core/services/recognition/model",
                        "bot_core/services/recognition/labels.txt")
text_message_processor = TextMessageResponseProcessor()
image_message_processor = ImageMessageResponseProcessor(sender, recognizer)


@shared_task
def reply_message(data):
    event_type = data["type"]
    submission_data = []

    if event_type == "message":
        message = data["message"]
        message_type = message["type"]

        if message_type == "text":
            received_text = message["text"]
            # process submission text
            submission_data = text_message_processor.process(received_text)
        elif message_type == "image":
            submission_data = image_message_processor.process(message)
    else:
        print("Not supported event type.")
        raise RuntimeError()

    if len(submission_data) == 0:
        print("No messages.")
        raise RuntimeError()

    request_body = {"replyToken": data["replyToken"], "messages": submission_data}
    print(request_body)
    sender.reply(request_body)
