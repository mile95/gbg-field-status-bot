# coding=utf-8

from typing import List
import tweepy
from bs4 import BeautifulSoup
import requests
import re
import datetime
import json
from os import environ

# Twitter authentication
ACCESS_TOKEN_SECRET = environ["ACCESS_TOKEN_SECRET"]
ACCESS_TOKEN = environ["ACCESS_TOKEN"]
CONSUMER_API_KEY = environ["CONSUMER_API_KEY"]
CONSUMER_API_SECRET = environ["CONSUMER_API_SECRET"]

# Göteborgs Stad
URL = "https://bok.goteborg.se/ShowNews.action;jsessionid=8B8D19B5301F646B425B26EF4E1874D6?id=285"
IGNORED_SPANS = [
    "CENTRUM",
    "NORDOST",
    "VÄSTER",
    "HISINGEN",
    "Grön markering",
    "Röd markering",
]
VALID_COLORS = ["#00ff00", "#ffffff", "ff0000"]

# Create access to Twitter API
auth = tweepy.OAuthHandler(CONSUMER_API_KEY, CONSUMER_API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
API = tweepy.API(auth)


def collect_statuses_from_webpage() -> dict:
    html_data = requests.get(URL).text
    soup = BeautifulSoup(html_data)
    fields = {}
    for span in soup.find_all("span"):
        text = span.text
        text = text.replace("\xa0", " ")
        style = span.get("style")
        if (
            re.search("[a-zA-Z]", text)
            and style
            and any(color in style for color in VALID_COLORS)
            and not any(filter_span in text for filter_span in IGNORED_SPANS)
        ):
            fields[text] = "GREEN" if "#00ff00" in style else "RED"
    return fields


def tweet_statuses(closed_fields):
    time = (datetime.datetime.utcnow() + datetime.timedelta(hours=2)).strftime(
        "%Y-%m-%d %H:%M"
    )
    tweet_text = f"Uppdatering: {time} \n\n"
    if not closed_fields:
        tweet_text += "Alla planer är spelbara! ✅"
    else:
        for field in closed_fields:
            tweet_text += f"{field} ❌ \n"
    API.update_status(tweet_text)


def get_closed_fields(statuses) -> List:
    closed = []
    for field, status in statuses.items():
        if status == "RED":
            closed.append(field)
    return closed


def lambda_handler(event, context):
    statuses = collect_statuses_from_webpage()
    closed_fields = get_closed_fields(statuses)
    tweet_statuses(closed_fields)
    return {"statusCode": 200, "body": json.dumps({"Message ": "Tweet Tweeted!"})}
