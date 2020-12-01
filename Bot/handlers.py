from config import TELEGRAM_TOKEN
from flask import Response
import requests
from telebot import types
import json

RES = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=Markdown"



# "/sign_up"
def get_personal_data_handler(args, chat_id, data):
    requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Hi there " + data.get('message').get('from').get('first_name')))
    first_name = data.get('message').get('from').get('first_name')
    last_name = data.get('message').get('from').get('last_name')
    user_id = chat_id
    

    user_place = 1

    hobbies = ['video games', 'Movies', 'Sports', 'Cooking']
    reply_markup = reply_markup_maker(hobbies)

    
    requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "You can type /hobbies <hobby1,...> \nnow we support" + "\nVideo games\nMovies\nSports\nCooking"))
    requests.get((RES+ "&reply_markup={}").format(TELEGRAM_TOKEN, chat_id, "Please reply with your hobbies\n",reply_markup))
    #hobbies = get_hobbies()


# /session 
def starrt_session(args, chat_id, data):
    user_place = get_place()

    if user_place == 1: ## the first_question
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "welecome to our session")
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "this session is secret so dont worry no one will know anything about it")
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Lets Start")
    
    else:
        """Analyze_what the user typed"""

    question = get_rand_question_based_on_cata(user_place)
    requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "First_Question<question>")
    user_place +=1
    update_place_in_dataBase(chat_id)

    pass


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


