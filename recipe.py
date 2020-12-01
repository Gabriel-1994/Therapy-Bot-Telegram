import requests

api_url = "http://www.recipepuppy.com/api/?i={}"


def get_recipes(ingredients):
    recipes = requests.get(api_url.format(ingredients)).json()["results"]
    res_str = ""

    if len(recipes) == 0:
        return "No match"

    for r in recipes:
        res_str += "Title: " + r["title"] + "\n\tLink: " + r["href"] + "\n\tIngredients: " + r["ingredients"] + "\n\n"
    return res_str



