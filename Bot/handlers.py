
from config import TELEGRAM_TOKEN
from flask import Response
import requests

RES = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
def prime_handler(args, chat_id):
    try:
        number = int(args[1])
    except:
        requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "Please Enter Numbers"))
        return Response("Server is up and running smoothly")        

    if is_prime(number):
        res = requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "is Prime"))
    else:
        res = requests.get(RES.format(TELEGRAM_TOKEN, chat_id, "is not prime"))

    return Response("Server is up and running smoothly")

