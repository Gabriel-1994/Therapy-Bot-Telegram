import paralleldots
from config import paralleldots_TOKEN


def analyze_text(text):
    paralleldots.set_api_key(paralleldots_TOKEN)
    paralleldots.get_api_key()
    emotions = paralleldots.emotion(text)["emotion"]
    pos = (emotions["Happy"] + emotions["Excited"]) 
    return pos


def compare_mood(prev, now):
    
    pre_neg = 1 - prev
    now_neg = 1 - now
    if prev < now and pre_neg > now_neg:
        return "better"
    elif prev < now and pre_neg > now_neg:
        return "better positive"
    else:
        return "worse"


def analyze_text_w(text):
    paralleldots.set_api_key(paralleldots_TOKEN)
    paralleldots.get_api_key()
    emotions = paralleldots.emotion(text)["emotion"]
    pos = (emotions["Happy"] + emotions["Excited"]) / 2
    neg = (emotions["Angry"] + emotions["Bored"] + emotions["Fear"] + emotions["Sad"]) / 4
    print(pos, " ", neg)



