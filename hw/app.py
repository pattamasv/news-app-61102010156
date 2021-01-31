from flask import Flask
from flask import render_template
from flask import request
from urllib.parse import quote
from urllib.request import urlopen
import json
from newsapi import NewsApiClient


app = Flask(__name__)

OPEN_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&APPID={1}"
OPEN_WEATHER_KEY = 'e26f92de9d65859a0233d265a4175cd3'

OPEN_NEWS_URL = "https://newsapi.org/v2/everything?q={0}&apiKey={1}"
OPEN_KEYWORD = 'COVID-19'
OPEN_NEWS_KEY = '35447a398c0449ac804cc9d7a8e4d172'

@app.route('/')
def index():
    city = request.args.get('city')
    if not city:
        city = 'bangkok'
    weather = get_weather(city, OPEN_WEATHER_KEY)

    newsapi = NewsApiClient(api_key="35447a398c0449ac804cc9d7a8e4d172")
    topheadlines = newsapi.get_everything(q="COVID-19")

    articles = topheadlines['articles']

    desc = []
    news = []
    img = []
    url = []

    for i in range(5):
        myarticles = articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        url.append(myarticles['url'])

    mylist = zip(news, desc, img, url)

    return render_template("home.html", weather=weather, context = mylist)

def get_weather(city,API_KEY):
    query = quote(city)
    url = OPEN_WEATHER_URL.format(city, API_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):

        description = parsed['weather'][0]['description']
        temperature = parsed['main']['temp']
        pressure = parsed['main']['pressure']
        humidity = parsed['main']['humidity']
        speed = parsed['wind']['speed']
        city = parsed['name']
        country = parsed['sys']['country']
        icon = parsed['weather'][0]['icon']

        weather = {'description': description,
                   'temperature': temperature,
                   'pressure' : pressure,
                   'humidity' : humidity,
                   'speed' : speed,
                   'city': city,
                   'country': country,
                   'icon' : icon
                   }
    return weather

@app.route('/news')
def news():
    news = request.args.get('news')
    if not news:
        news = 'covid-19'
   
    newsapi = NewsApiClient(api_key="35447a398c0449ac804cc9d7a8e4d172")
    topheadlines = newsapi.get_everything(q=news)
    

    articles = topheadlines['articles']

    desc = []
    news = []
    url = []

    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        url.append(myarticles['url'])

    mylist = zip(news, desc, url)

    return render_template('news.html', context = mylist)

@app.route('/about')
def about():
    return render_template('about.html')



