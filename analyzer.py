import paralleldots
from config import paralleldots_TOKEN


def analyze_text(text):
    paralleldots.set_api_key(paralleldots_TOKEN)
    paralleldots.get_api_key()
    return paralleldots.emotion(text)["emotion"]
