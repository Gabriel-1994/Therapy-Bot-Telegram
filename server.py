from flask import Flask, Response, request
from config import *
import requests
from Bot.Bot import *
import json



app = Flask(__name__, static_url_path='', static_folder='dist')

@app.route('/message', methods=["POST"])
def message_handler():
    args = request.get_json()['message']['text'].split()
    chat_id = request.get_json()['message']['chat']['id']

    bot.action(args,chat_id)
    print(request.get_json())
        
    return Response("Server is up and running smoothly")



if __name__ == '__main__':
    requests.get(TELEGRAM_INIT_URL)
    bot = get_bot()
    app.run(port=5003)
