import os
import requests
import smtplib

my_email = "pythonemailtest106"
password = os.environ.get("PASSWORD")

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_api_key = os.environ.get("AV_API_KEY")
news_api_key = os.environ.get("NEWS_API_KEY")

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_api_key
}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]

stock_list = [value for (key, value) in stock_data.items()]
yesterday_data = stock_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = stock_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
diff_percent = (difference / float(yesterday_closing_price)) * 100

if diff_percent > .01:
    news_params = {
        "q": COMPANY_NAME,
        "apikey": news_api_key
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]

    formatted_articles = [f"Headline: {article['title']}: {up_down}{diff_percent}. \nBrief: {article['description']}"
                          for article in three_articles]

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(my_email, password)
        for article in formatted_articles:
            connection.sendmail(from_addr=my_email,
                                to_addrs="tonystark53150@gmail.com",
                                msg=f"Subject: Tesla Stock Info \n\n{formatted_articles}".encode('utf-8'))

"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
