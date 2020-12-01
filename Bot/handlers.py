from config import TELEGRAM_TOKEN
from flask import Response
import requests
from telebot import types
import json
import DatabaseAPI.userinfoAPI as userAPI
import DatabaseAPI.questionsAPI as qAPI
RES = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=Markdown"




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
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Welecome Back" + data.get('message').get('from').get('first_name')))


    else:
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Hi there " + data.get('message').get('from').get('first_name')))
        first_name = data.get('message').get('from').get('first_name')
        last_name = data.get('message').get('from').get('last_name')
        user_id = chat_id
        user_place = 1
        userAPI.add_user(user_id, first_name + " " +  last_name, "Jerusalem", None, user_place)
        hobbies_handler(args, chat_id, data)
        
    #hobbies = get_hobbies()

def hobbies_handler(args, chat_id, data):
    hobbies = ['Video games', 'Movies', 'Sports', 'Cooking']
    reply_markup = reply_markup_maker(hobbies)
    requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "You can type /hobbies <hobby1,...> \nnow we support" + "\nVideo games\nMovies\nSports\nCooking"))
    requests.get((RES+ "&reply_markup={}").format(TELEGRAM_TOKEN, chat_id, "Please reply with your hobbies\n",reply_markup))

def add_hobbies_handler(args, chat_id, data):
    userAPI.add_activity(chat_id,data['message']['text'])

# /session 
def start_session(args, chat_id, data):
    user_question_place = get_place(chat_id)

    if user_question_place == 1: ## the first_question
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "welecome to our session"))
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "this session is secret so dont worry no one will know anything about it"))
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Lets Start"))
    
    else:
        """Analyze_what the user typed"""

    question = get_rand_question_based_on_cata(user_question_place)
    requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "First_Question<question>"))
    user_question_place +=1
    update_place_in_dataBase(chat_id)


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
    print(reply_markup)
    return json.dumps(reply_markup)


