from flask import Flask, Response, request
from config import *
import requests
from Bot.Bot import *
from analyzer import analyze_text
import json

app = Flask(__name__, static_url_path='', static_folder='dist')


@app.route('/message', methods=["POST"])
def message_handler():
    bot = Bot()
    chat_id = request.get_json()['message']['chat']['id']
    analyzer = analyze_text(request.get_json()['message']['text'])
    bot.send_message(chat_id=chat_id,message=analyzer)
    return Response("success")


if __name__ == '__main__':
    requests.get(TELEGRAM_INIT_URL)
    app.run(port=5003)
