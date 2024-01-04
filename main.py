import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "QSBMD0B4K958SQ3F"

NEWS_API_KEY = "bfd0af710f584fcf8708b5300a4f1f6e"

TWILIO_SID = "AC81080a36cd0a332a949aaa96c192afa2"
TWILIO_TOKEN = "0158d3510a780809bcf334b4565e75d4"
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)

data = response.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)


day_before_yesterday_data = data_list[1]
day_before_closing_price = day_before_yesterday_data["4. close"]
print(day_before_closing_price)

difference = abs(float(yesterday_closing_price) - float(day_before_closing_price))

print(difference)

diff_percent = (difference/float(yesterday_closing_price)) * 100
print(diff_percent)

if diff_percent > 2:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]

    formatted_articles_list = [f"Headline: {article['title']}. \n Brief: {article['description']}" for article in three_articles]
    for formatted_article in formatted_articles_list:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        message = client.messages.create(
            body=formatted_article,
            from_="+19285506360",
            to="+16475182082"
        )