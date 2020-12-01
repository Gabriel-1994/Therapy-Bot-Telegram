
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

def is_prime(num):
    if num > 1:
        for i in range(2, num//2):
            if (num % i) == 0:
                print(num, "is not a prime number")
                return False
        else:
            return True
    else:
        return False