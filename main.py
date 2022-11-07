import requests
import os
from twilio.rest import Client

"""Global variables"""
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEW_API_KEY = os.environ.get("NEWSAPI")
STOCK_API_KEY = os.environ.get("STOCKAPI")
TWILIO_SID = "ACe6e5382825a13db97ad1afbaf0082a9d"
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

"""Stock data analysis to determine percentage difference between the last 2 days closing stock price"""
stock_parameter = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "interval": "5min",
    "adjusted": "true",
    "apikey": STOCK_API_KEY
}

stock_response = requests.get(STOCK_ENDPOINT, stock_parameter)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]
today_close = stock_data_list[0]["4. close"]
yesterday_close = stock_data_list[1]["4. close"]
percentage = (float(today_close) / float(yesterday_close)) * 100
result = 100 - percentage


"""Stock News functionality"""
news_parameter = {
    "qInTitle": "Tesla",
    "from": "2022-11-04",
    "to": "2022-11-04",
    "sortby": "publishedAt",
    "source": "bbc-news",
    "apikey": NEW_API_KEY,
}
client = Client(TWILIO_SID, AUTH_TOKEN)
news_response = requests.get(NEWS_ENDPOINT, params=news_parameter)
news_response.raise_for_status()
new_data = news_response.json()
news_article = new_data["articles"]
news_title = [item["title"] for item in news_article[:3]]
news_description = [item["description"] for item in news_article[:3]]


"""Sending messages when stock closing price is 5% higher or lower than the previous day"""


def percentage_result():
    if result >= 5:
        return "UP;💚"
    elif result <= 5:
        return "DOWN;💚"


for n in range(3):
    percentage_result()
    message = client.messages.create(
        body=f"{percentage_result()}\nHeadline: {news_title[n]}\nBrief: {news_description[n]}",
        from_="+19206909329",
        to="+2347045905073"
    )
