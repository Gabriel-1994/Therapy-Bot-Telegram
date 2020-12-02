from config import TELEGRAM_TOKEN
import requests

from Bot.handlers import *
import DatabaseAPI.userinfoAPI as userAPI

class Bot:
    RES = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"

    def __init__(self):
        self.handlers = {}

    def send_message(self, chat_id, message):
        requests.get(Bot.RES.format(TELEGRAM_TOKEN, chat_id, message))

    def add_handler(self, handler_name, handler):
        self.handlers[handler_name] = handler
    
    def action(self,args,chat_id, data):
        
        try:
            user_question_place = int(userAPI.fetch_Qcounter(chat_id).get('quest_counter'))
            if user_question_place <= 4 and user_question_place > 0:
                self.handlers.get("/session")(args, chat_id, data)
                return

            if user_question_place == 10:
                self.handlers.get("/hobbies")(args, chat_id, data)
            
            if user_question_place == 7:
                self.handlers.get("/suggest_activity")(args,chat_id,data)
        except:
            pass
        try:
            self.handlers.get(args[0])(args, chat_id, data)
            return
        except:
            return


def get_bot():
    bot = Bot()
    bot.add_handler("/sign_up", get_personal_data_handler)
    bot.add_handler("/hobbies", hobbies_handler)
    bot.add_handler("/session", start_session)
    bot.add_handler("/suggest_activity",suggest_activity)
    return bot
