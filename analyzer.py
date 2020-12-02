import paralleldots
from config import paralleldots_TOKEN


def analyze_text(text):
    paralleldots.set_api_key(paralleldots_TOKEN)
    paralleldots.get_api_key()
    emotions = paralleldots.emotion(text)["emotion"]
    pos = (emotions["Happy"] + emotions["Excited"]) 
    return pos

def get_highest_two_emotions(text):
    paralleldots.set_api_key(paralleldots_TOKEN)
    paralleldots.get_api_key()
    emotions = paralleldots.emotion(text)["emotion"]
    my_list=[k for k, v in emotions.items() if v == max(emotions.values())]
    if my_list[0] == "Fear":
        return "Sad"
    return my_list[0]

    


def compare_mood(prev, now):
    
    pre_neg = 1 - prev # 1 , 0
    now_neg = 1 - now  # 0.7, 0.3
    if prev < now and pre_neg > now_neg:
        return "better"
    elif prev < now and pre_neg > now_neg:
        return "much better"
    else:
        return "Sad"


def analyze_text_w(text):
    paralleldots.set_api_key(paralleldots_TOKEN)
    paralleldots.get_api_key()
    emotions = paralleldots.emotion(text)["emotion"]
    pos = (emotions["Happy"] + emotions["Excited"]) / 2
    neg = (emotions["Angry"] + emotions["Bored"] + emotions["Fear"] + emotions["Sad"]) / 4
    print(pos, " ", neg)



