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
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Welcome Back " + data.get('message').get('from').get('first_name') + " Nice to see you again"))
        userAPI.update_question_counter(chat_id,1)


    else:
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Hi " + data.get('message').get('from').get('first_name')+" Welcome to MOODIFIER! \nMy goal is to always lighten your mood and give you a safe space to talk about your problems. " ))
        time.sleep(1.5)
        first_name = data.get('message').get('from').get('first_name')
        last_name = data.get('message').get('from').get('last_name')
        user_id = chat_id
        user_place = 12
        userAPI.add_user(user_id, first_name + " " +  last_name, "", 0, user_place)
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Where do you live"))



def get_location_handler(args, chat_id, data):
    location = data['message']['text']
    print(location)
    user_place = 10
    userAPI.update_question_counter(chat_id,user_place)
    userAPI.update_location(chat_id,location)
    requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Your location is saved, lets start with your hobbies"))
    hobbies_handler(args, chat_id, data)


def hobbies_handler(args, chat_id, data):
    
    if data['message']['text'] == 'End':
            time.sleep(1.0)
            requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Great, Now we can start our /session "))
            time.sleep(1.5)
            user_place = 1
            userAPI.update_question_counter(chat_id, user_place)
    else:
        if not data['message']['text'] == '/sign_up':
            add_hobbies_handler(args, chat_id, data)
        hobbies = set(['Video Games', 'Movies', 'Sports', 'Cooking', "End"])
        user_hobbies = userAPI.fetch_activity(chat_id)

        user_hobbies = set([value['activity'] for value in user_hobbies])
        hobbies = list(hobbies - user_hobbies)
        reply_markup = reply_markup_maker(hobbies)
        #requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "You can type /hobbies <hobby1,...> \nnow we support" + "\nVideo games\nMovies\nSports\nCooking"))
        requests.get((RES+ "&reply_markup={}").format(TELEGRAM_TOKEN, chat_id, "Let's start by telling me what your favorite hobbies are: \n",reply_markup))

def add_hobbies_handler(args, chat_id, data):
    print("IN HOBBIES HANDLER")
    userAPI.add_activity(chat_id,data['message']['text'])

# /session 
def start_session(args, chat_id, data):
    user_question_place = int(userAPI.fetch_Qcounter(chat_id).get('quest_counter'))
    #if user_question_place == 1: ## the first_question
    if user_question_place == 1:
        question = qAPI.get_question_by_categoryID_randomly(user_question_place).get('question')
    
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, question))
        user_question_place +=1
        userAPI.update_question_counter(chat_id, user_question_place)
        return
    elif user_question_place == 2:
        
        #pre_health = userAPI.fetch_health_status(chat_id)
        curr_health = analyzer.analyze_text(data['message']['text'])
        #status = analyzer.compare_mood(pre_health, curr_health)
        userAPI.update_health_status(chat_id, curr_health)
        status1 = analyzer.get_highest_two_emotions(data['message']['text'])
        if status1 == "Happy" or status1 == "Excited":
            happy_gif = "https://i.gifer.com/1fQT.mp4"
            requests.get(RES.format(TELEGRAM_TOKEN, chat_id, happy_gif))
            time.sleep(1.5)                
            requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "I'm very happy to hear that you are " + status1))
            user_question_place = 7
            userAPI.update_question_counter(chat_id, user_question_place)
            suggest_activity(args, chat_id, data)
            return


        #shocked gif 
        gif = "https://thumbs.gfycat.com/AmazingGiftedGnu-mobile.mp4"
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, gif))
        
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "I'm very sorry to hear that! \nI am sensing that you are: " + status1))
        #second question
        question = qAPI.get_question_by_categoryID_randomly(user_question_place).get('question')
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, question))
        user_question_place +=1
        userAPI.update_question_counter(chat_id, user_question_place)
        return
    elif user_question_place == 3:
        #motivation
        question = qAPI.get_question_by_categoryID_randomly(user_question_place).get('question')
        user_question_place +=1
        userAPI.update_question_counter(chat_id, user_question_place)
        
        #fetching health status
        pre_health = userAPI.fetch_health_status(chat_id)
        curr_health = analyzer.analyze_text(data['message']['text'])
        status = analyzer.compare_mood(pre_health, curr_health)
        userAPI.update_health_status(chat_id, curr_health)

        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Aha, I see... That sucks!"))

        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Just remeber that " + question))
        time.sleep(1.0)

        #third question
        question = qAPI.get_question_by_categoryID_randomly(user_question_place).get('question')
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, question))
        return
    elif user_question_place == 4 :
        pre_health = userAPI.fetch_health_status(chat_id)
        print(pre_health)
        curr_health = analyzer.analyze_text(data['message']['text'])
        print(curr_health)
        status = analyzer.compare_mood(pre_health, curr_health)
        print(status)
        userAPI.update_health_status(chat_id, curr_health)

        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Wow! What a great idea!\nTo lighten the mood, here is a joke that always cracked me up (But remember I am a bot lol!)"))
        joke = requests.get("https://official-joke-api.appspot.com/jokes/general/random")
        time.sleep(0.5)    
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, joke.json()[0].get("setup")))
        time.sleep(5.0)    
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, joke.json()[0].get("punchline")))
        time.sleep(5.0)
        userAPI.update_question_counter(chat_id, 7)
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "I am very happy because I can sense that the mood is much better than start of our session!"))
        suggest_activity(args, chat_id, data)
        

   


def suggest_activity(args, chat_id, data):
    requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "I Would like to also suggest some activities that can put you even in a better mood (Although none of them can ever replace me)"))
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

    userAPI.update_question_counter(chat_id, 8)
    
     

def suggest_sport(activity,chat_id):
    requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "We suggest you go out and do some " + activity))
    weather = "https://api.weatherbit.io/v2.0/current?city=Jerusalem&key={}"
    temp = requests.get(weather.format(WEATHER_TOKEN))
    weather_msg="The weather in your city is currently " + str(temp.json()["data"][0]["temp"]) + " Degrees with "+temp.json()["data"][0]["weather"]["description"]
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
    curr_health = userAPI.fetch_health_status(chat_id)
    requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Since you love" + activity+ " We can suggest a few of our top recipes"))
    if curr_health < 0.5:
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "I sense that you are still sad Here are some recipes that can cheer you up!"))
        response=sendRecipe("sweets")
        
    else:
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "I sense that you are happy I encourgae you to have a healthy meal! Here are some recipes"))
        response=sendRecipe("healthy")

    requests.get(RES.format(TELEGRAM_TOKEN, chat_id,response))
    userAPI.update_question_counter(chat_id,8)

def sendRecipe(query):   
    api_url = "http://www.recipepuppy.com/api/?q={}"
    recipes = requests.get(api_url.format(query)).json()["results"]
    res_str = ""

    if len(recipes) == 0:
        return "No match"

    for r in recipes:
        res_str += "Title: " + r["title"] + "\n\tLink: " + r["href"] + "\n\tIngredients: " + r["ingredients"] + "\n\n"
    
    return res_str


     




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

