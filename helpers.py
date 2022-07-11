import json


def save_user(func):
    def wrapper(*args, **kwargs):
        user_data = func(*args, **kwargs)
        with open("data/userinfo.json", "w") as f:
            json.dump(user_data, f)
            return


new_user = {
    "name": "bill"
}