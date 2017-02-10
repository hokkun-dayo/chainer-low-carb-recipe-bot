# coding: utf-8
import json

import re

import io
from PIL import Image

from bot_core.services.bot_utility import send_message_utility
from bot_core.services.edamam import client


class TextMessageResponseProcessor:
    def __init__(self):
        self.regex = re.compile(r"search: ([a-zA-Z ]+)")

    def process(self, received_text):
        submission_data = []

        res = self.regex.match(received_text)
        if res:
            query = res.group(1)
            print("query: {}".format(query))
            recipe_list = client.search(query, "low-carb")
            column_list = list(map(TextMessageResponseProcessor.make_result_column, recipe_list[:5]))
            submission_data.append(send_message_utility.get_carousel_message(column_list, "recipes"))

        return submission_data

    @staticmethod
    def make_result_column(recipe):
        text = "100gあたりのカロリー: {:.2f}kcal".format(recipe.calories / recipe.total_weight * 100)
        actions = [{"type": "uri", "label": "このレシピを見る", "uri": recipe.url}]
        return send_message_utility.get_carousel_column(recipe.image_url,
                                                        recipe.title,
                                                        text,
                                                        actions=actions)


class ImageMessageResponseProcessor:
    def __init__(self, sender, recognizer):
        self.sender = sender
        self.recognizer = recognizer

    def process(self, message):
        image_id = message["id"]
        content = self.sender.content(image_id)

        image = Image.open(io.BytesIO(content))
        resized = image.resize((256, 256))
        recog_result = self.recognizer.recognize(resized)
        recipe_list = client.search(recog_result, "low-carb")
        column_list = list(map(TextMessageResponseProcessor.make_result_column, recipe_list[:5]))

        return [send_message_utility.get_text_message("その写真は{}ですね？".format(recog_result)),
                send_message_utility.get_text_message("{}の糖質制限レシピをお教えしましょう！".format(recog_result)),
                send_message_utility.get_carousel_message(column_list, "recipes")]
