
from config import TELEGRAM_TOKEN
import requests
from flask import request
from Bot.handlers import *

class Bot:
    RES = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
    def __init__(self):
        self.handlers = {}

    def send_message(self,chat_id,message):
        requests.get(Bot.RES.format(TELEGRAM_TOKEN, chat_id, message))

    
    def add_handler(self, handler_name,handler):
        self.handlers[handler_name] = handler
        
    def action(self,args,chat_id):
        pass


def get_bot():
    bot = Bot()
    bot.add_handler("/prime", prime_handler)
    return bot