# coding: utf-8
import json

import requests

API_ENDPOINT = "https://api.edamam.com/search"
APP_ID = "3fb80aec"
APP_KEY = json.load(open("bot_core/services/edamam/edamam_setting.json"))["api_key"]


def search(query, diet):
    params = {"app_id": APP_ID, "app_key": APP_KEY, "q": query, "diet": diet, "to": 5}
    res = requests.get(API_ENDPOINT, params=params)
    res_json = res.json()
    hits = res_json["hits"]
    ret = []
    for hit in hits:
        recipe = hit["recipe"]
        single_ret = Recipe(recipe["url"], recipe["image"], recipe["label"],
                            recipe["calories"], recipe["totalWeight"])
        ret.append(single_ret)

    return ret


class Recipe:
    def __init__(self, url, image_url, title, calories, total_weight):
        self.calories = calories
        self.total_weight = total_weight
        self.title = title
        self.url = url
        self.image_url = image_url
