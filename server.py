from flask import Flask, Response, request
from config import *
import requests
from Bot.Bot import *
import json



app = Flask(__name__)

@app.route('/message', methods=["POST"])
def message_handler():

    args = request.get_json()['message']['text'].split()
    chat_id = request.get_json()['message']['chat']['id']

    bot.action(args,chat_id,request.get_json())
    
    return Response("Server is up and running smoothly")
    """
    args = request.get_json().get('message',{}).get('text',"").split()
    chat_id = request.get_json().get('message',{}).get('chat',{}).get('id')
    print(request.get_json())
    reply_markup = json.dumps({'keyboard': [,[{'text': "Send Your Location", 'request_location': True}] ]})
    requests.get((RES+ "&reply_markup={}").format(TELEGRAM_TOKEN, chat_id, "Location\n",reply_markup))

    # print(chat_id)
    # bot.action(args,chat_id,request.get_json())
    return Response("Server is up and running smoothly")
    """



if __name__ == '__main__':
    requests.get(TELEGRAM_INIT_URL)
    bot = get_bot()
    app.run(port=5002)
