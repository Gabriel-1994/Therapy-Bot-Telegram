import paralleldots
from config import paralleldots_TOKEN


def analyze_text(text):
    paralleldots.set_api_key(paralleldots_TOKEN)
    paralleldots.get_api_key()
    emotions = paralleldots.emotion(text)["emotion"]
    pos = (emotions["Happy"] + emotions["Excited"]) / 2
    neg = (emotions["Angry"] + emotions["Bored"] + emotions["Fear"] + emotions["Sad"]) / 4
    return pos, neg


def analyze_text_w(text):
    paralleldots.set_api_key(paralleldots_TOKEN)
    paralleldots.get_api_key()
    emotions = paralleldots.emotion(text)["emotion"]
    pos = (emotions["Happy"] + emotions["Excited"]) / 2
    neg = (emotions["Angry"] + emotions["Bored"] + emotions["Fear"] + emotions["Sad"]) / 4
    print(pos, " ", neg)


analyze_text_w("hello love")
