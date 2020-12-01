from flask import Flask, Response, request
from config import *
import requests
from Bot.Bot import *
import json



app = Flask(__name__, static_url_path='', static_folder='dist')

@app.route('/message', methods=["POST"])
def message_handler():
    chat_id = request.get_json()['message']['chat']['id']

    #print(request.get_json())    
    #bot.send_message(chat_id, "Hi, What's your location? Preferably the name of the city and country. Thank you")
    
    txt = request.get_json()['message'].get("text")

    weather = "https://api.weatherbit.io/v2.0/current?city={}&key={}"
    temp = requests.get(weather.format(txt, WEATHER_TOKEN))
    bot.send_message(chat_id, "The weather in your city is currently " + str(temp.json()["data"][0]["temp"]) + " Degrees")
    


    



    return Response("Server is up and running smoothly")



if __name__ == '__main__':
    requests.get(TELEGRAM_INIT_URL)
    bot = get_bot()
    app.run(port=5002)
