import json
import requests
import pprint
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-s",
    action='store_true',
    help="post to slack")

parser.add_argument(
    "-wp",
    action='store_true',
    help="display only dishes with price")

args = parser.parse_args()


class Slack:

    def __init__(self):
        if args.s:
            self.hook_link = get_data_from_token("slack-web-hook-link")

    def post(self, menus):
        for menu in menus:
            post_data = {"text": menu}
            if args.s:
                data = json.dumps(post_data, ensure_ascii=False).encode('utf8')
                requests.post(self.hook_link, data=data)
            else:
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(json.dumps(post_data))


class Zomato:

    def __init__(self):
        self.token = get_data_from_token("zomato-token")

    def get_daily_dishes(self, res_id, name):
        payload = {'res_id': res_id}
        headers = {'user_key': self.token}
        r = requests.get(
            "https://developers.zomato.com/api/v2.1/dailymenu",
            params=payload,
            headers=headers)
        if r.status_code == requests.codes.ok:
            dishes = r.json()["daily_menus"][0]["daily_menu"]["dishes"]
            if args.wp:
                dishes = list(filter(
                    lambda x: len(x["dish"]["price"]) > 0,
                    dishes))
            return self.format_data(dishes, name)
        else:
            return self.no_daily_menu(name)

    def format_data(self, data, restaurant_name):
        dishes = "*" + restaurant_name + "*" + "\n"
        for dish in data:
            dishes += dish["dish"]["name"] + "\n"
        return dishes

    def no_daily_menu(self, restaurant_name):
        dishes = "*" + restaurant_name + "*" + "\n"
        dishes += "no daily menu"
        return dishes

    def read_restaurants(self):
        with open('restaurants.json', encoding="utf-8") as restaurants_file:
            restaurants = json.load(restaurants_file)
        return restaurants


def get_data_from_token(id):
    with open('config.json', encoding="utf-8") as tokens_file:
        tokens_json = json.load(tokens_file)
        token = tokens_json[id]
    return token


zom = Zomato()

menus = list()

for restaurant in zom.read_restaurants():
    rest_id = restaurant["id"]
    rest_name = restaurant["name"]
    menus.append(zom.get_daily_dishes(rest_id, rest_name))

slack = Slack()
slack.post(menus)
