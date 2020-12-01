from config import TELEGRAM_TOKEN
from flask import Response
import requests
import time
from telebot import types
import json
import DatabaseAPI.userinfoAPI as userAPI
import DatabaseAPI.questionsAPI as qAPI
import analyzer
RES = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=Markdown"



# "/sign_up"

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

# "/start"
def get_personal_data_handler(args, chat_id, data):
    if userAPI.search_user(chat_id):
        """ not first time user """
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Welecome Back " + data.get('message').get('from').get('first_name')))

    #/sign_up
    else:
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Hi there " + data.get('message').get('from').get('first_name')))
        first_name = data.get('message').get('from').get('first_name')
        last_name = data.get('message').get('from').get('last_name')
        user_id = chat_id
        user_place = 1
        userAPI.add_user(user_id, first_name + " " +  last_name, "Jerusalem", 0, user_place)
        hobbies_handler(args, chat_id, data)
        

def hobbies_handler(args, chat_id, data):
    hobbies = ['Video games', 'Movies', 'Sports', 'Cooking']
    reply_markup = reply_markup_maker(hobbies)
    requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "You can type /hobbies <hobby1,...> \nnow we support" + "\nVideo games\nMovies\nSports\nCooking"))
    requests.get((RES+ "&reply_markup={}").format(TELEGRAM_TOKEN, chat_id, "Please reply with your hobbies\n",reply_markup))

def add_hobbies_handler(args, chat_id, data):
    print("IN HOBBIES HANDLER")
    userAPI.add_activity(chat_id,data['message']['text'])

# /session 
def start_session(args, chat_id, data):
    user_question_place = int(userAPI.fetch_Qcounter(chat_id).get('quest_counter'))
    if user_question_place == 1: ## the first_question
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "welecome to our session"))
        time.sleep(0.5)
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "this session is secret so dont worry no one will know anything about it"))
        time.sleep(0.5)

        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Lets Start"))
    
    else:
        """Analyze what the user typed"""
        pre_health = userAPI.fetch_health_status(chat_id)
        curr_health = analyzer.analyze_text(data['message']['text'])

        status = analyzer.compare_mood(pre_health, curr_health)
        

        userAPI.update_health_status(chat_id, curr_health)
        



    question = qAPI.get_question_by_categoryID_randomly(user_question_place).get('question')

    requests.get(RES.format(TELEGRAM_TOKEN, chat_id, question))
    user_question_place +=1
    userAPI.update_question_counter(chat_id, user_question_place)

def reply_markup_maker(data):
    keyboard = []
    for i in range(0,len(data),2):
        key =[]
        key.append( data[i].title())
        try:
            key.append(data[i+1].title())
        except:
            pass
        keyboard.append(key)
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

