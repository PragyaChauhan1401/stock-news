import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API = "ur stock api"
NEWS_API = "ur api"
TWILIO_SID = "ur sid"
TWILIO_AUTH_TOKEN = "ur auth token"

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()['Time Series (Daily)']
data_list = [value for(key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price=yesterday_data['4. close']

#Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_price = day_before_yesterday_data['4. close']
print(day_before_yesterday_price)

#Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = float(yesterday_closing_price) - float(day_before_yesterday_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"



#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round((abs(difference)/float(yesterday_closing_price))*100)
print(diff_percent)
#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

if diff_percent > 5:
    new_params = {
        "apiKey": NEWS_API,
        "qInTitle": COMPANY_NAME
    }
    responses = requests.get(NEWS_ENDPOINT, params=new_params)
    news_data = responses.json()["articles"]
    three_articles = news_data[:3]




    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_article = [f"{STOCK_NAME}:{up_down}{diff_percent}%\nHeadlines: {article['title']}. \nBrif: {article['description']}" for article in three_articles]

#Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_article:
        message = client.messages.create(
                        body=article,
                        from_="+14154085538",
                        to="your phone number"

    )
