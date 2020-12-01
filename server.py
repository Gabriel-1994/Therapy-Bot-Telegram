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
    

    args = request.get_json()['message']['text'].split()
    chat_id = request.get_json()['message']['chat']['id']
    print(chat_id)
    bot.action(args,chat_id,request.get_json())
    return Response("Server is up and running smoothly")



if __name__ == '__main__':
    requests.get(TELEGRAM_INIT_URL)
    app.run(port=5003)
