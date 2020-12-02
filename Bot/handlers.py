from config import TELEGRAM_TOKEN, WEATHER_TOKEN, MOVIES_TOKEN
from flask import Response
import requests
import time
from telebot import types
import json
import DatabaseAPI.userinfoAPI as userAPI
import DatabaseAPI.questionsAPI as qAPI
import analyzer


RES = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=Markdown"


# "/start"
def get_personal_data_handler(args, chat_id, data):
    if userAPI.search_user(chat_id):
        """ not first time user """
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Welcome Back " + data.get('message').get('from').get('first_name')))
        userAPI.update_question_counter(chat_id,1)


    else:
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Hi there " + data.get('message').get('from').get('first_name')))
        first_name = data.get('message').get('from').get('first_name')
        last_name = data.get('message').get('from').get('last_name')
        user_id = chat_id
        user_place = 10
        userAPI.add_user(user_id, first_name + " " +  last_name, "Jerusalem", 0, user_place)
        hobbies_handler(args, chat_id, data)

        

def hobbies_handler(args, chat_id, data):
    
    if data['message']['text'] == 'End':
            requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Nice, done adding your hobbies\nif you want to start your session you should try to send /session "))
            user_place = 1
            userAPI.update_question_counter(chat_id, user_place)
    else:
        if not data['message']['text'] == '/sign_up':
            add_hobbies_handler(args, chat_id, data)
        hobbies = set(['Video Games', 'Movies', 'Sports', 'Cooking', "End"])
        user_hobbies = userAPI.fetch_activity(chat_id)

        user_hobbies = set([value['activity'] for value in user_hobbies])
        print(hobbies)
        print(user_hobbies)
        hobbies = list(hobbies - user_hobbies)
        print(hobbies)
        reply_markup = reply_markup_maker(hobbies)
        #requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "You can type /hobbies <hobby1,...> \nnow we support" + "\nVideo games\nMovies\nSports\nCooking"))
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

   


def suggest_activity(args, chat_id, data):
    requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "It was nice chatting with you today at our session"))
    time.sleep(1)
    requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Here are some suggestions for activites to do that can help you to be in a better mood"))
    time.sleep(1)
    activity=userAPI.fetch_one_activity(chat_id).get("activity")
    print(activity)
    if activity=='Sports':
        suggest_sport(activity,chat_id)
    elif activity=='Movies':
        suggest_movies(activity,chat_id)
    elif activity=='Cooking':
        suggest_recipe(activity,args,chat_id,data)
    elif activity=='--':
        suggest_sport(activity, chat_id)

    userAPI.update_question_counter(chat_id, 1)
    
     

def suggest_sport(activity,chat_id):
    requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "We suggest you go out and do some " + activity))
    weather = "https://api.weatherbit.io/v2.0/current?city=Jerusalem&key={}"
    temp = requests.get(weather.format(WEATHER_TOKEN))
    weather_msg="The weather in your city is currently " + str(temp.json()["data"][0]["temp"]) + " Degrees "+temp.json()["data"][0]["weather"]["description"]
    requests.get(RES.format(TELEGRAM_TOKEN, chat_id,weather_msg))

def suggest_movies(activity,chat_id):
    requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "We suggest you watch some " + activity))
    movies = "https://api.themoviedb.org/3/discover/movie?api_key={}&language=en-US&sort_by=revenue.desc&include_adult=false&include_video=false&page=1&with_genres=35&primary_release_date.gte=2015-01-01&primary_release_date.lte=2015-12-31&with_original_language=en"
    comedy = requests.get(movies.format(MOVIES_TOKEN))
    movies_list = ""
    for i in range(10):    
        movies_list += "\t" + (comedy.json()["results"][i]["title"])+" \n\n"
    movies_msg="Here are the top comedy movies that will definitely to cheer you up! \n" + movies_list
    requests.get(RES.format(TELEGRAM_TOKEN, chat_id, movies_msg))  

def suggest_recipe(activity,args, chat_id, data):
    
    requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Since you love" + activity+ " We can suggest a few of our top recipes"))
    requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "insert the ingredients you have in one line splitted by commas"))
    userAPI.update_question_counter(chat_id,-1)
    return

    
def getIngredient(args,chat_id,data):
    ingredients=data['message']['text']    
    api_url = "http://www.recipepuppy.com/api/?i={}"
    recipes = requests.get(api_url.format(ingredients)).json()["results"]
    res_str = ""

    if len(recipes) == 0:
        return "No match"

    for r in recipes:
        res_str += "Title: " + r["title"] + "\n\tLink: " + r["href"] + "\n\tIngredients: " + r["ingredients"] + "\n\n"
        
    requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Here are our top recipes based on your ingredients: \n" + res_str ))   
    userAPI.update_question_counter(chat_id,8) # 8 = Goodbye messge feature



     




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

