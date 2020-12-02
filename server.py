from flask import Flask, Response, request
from config import *
import requests
from Bot.Bot import *
from analyzer import analyze_text
from recipe import get_recipes
import json


app = Flask(__name__)


@app.route('/message', methods=["POST"])
def message_handler():
    #chat_id = request.get_json()['message']['chat']['id']

    #print(request.get_json())    
    #bot.send_message(chat_id, "Hi, What's your location? Preferably the name of the city and country. Thank you")
    """   -----   weather
    txt = request.get_json()['message'].get("text")

    weather = "https://api.weatherbit.io/v2.0/current?city={}&key={}"
    temp = requests.get(weather.format(txt, WEATHER_TOKEN))
    bot.send_message(chat_id, "The weather in your city is currently " + str(temp.json()["data"][0]["temp"]) + " Degrees")
    """
    """
    chat_id = request.get_json()['message']['chat']['id']
    joke = requests.get("https://official-joke-api.appspot.com/jokes/general/random")    
    bot.send_message(chat_id, joke.json()[0].get("setup"))

    bot.send_message(chat_id, joke.json()[0].get("punchline"))
    """

    """
    movies = "https://api.themoviedb.org/3/discover/movie?api_key={}&language=en-US&sort_by=revenue.desc&include_adult=false&include_video=false&page=1&with_genres=35&primary_release_date.gte=2015-01-01&primary_release_date.lte=2015-12-31&with_original_language=en"
    comedy = requests.get(movies.format(MOVIES_TOKEN))
    movies_list = []
    for i in range(10):    
        movies_list.append(comedy.json()["results"][i]["title"])

    bot.send_message(chat_id, movies_list)            
    """
    
    """
    args = request.get_json()['message']['text'].split()
    chat_id = request.get_json()['message']['chat']['id']
    print(chat_id)    
    bot.action(args,chat_id,request.get_json())
    """

    chat_id = request.get_json()['message']['chat']['id']
    gif = "https://thumbs.gfycat.com/AmazingGiftedGnu-mobile.mp4"
    bot.send_message(chat_id, gif)

    example_dict ={"mark":13, "steve":3, "bill":6, "linus":11} 
  
    print(list(sorted(example_dict.values()))[-2]) 


    return Response("Server is up and running smoothly")



if __name__ == '__main__':
    bot = get_bot()
    requests.get(TELEGRAM_INIT_URL)
    app.run(port=5002)
