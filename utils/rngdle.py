import requests
from datetime import datetime


class UserRolls:
    def __init__(self, number, date, score):
        self.number = number
        self.date = date
        self.score = score


def to_user_rolls(rolls: list):
    user_rolls = []
    for roll in rolls:
        number = roll["number"]
        score = roll["totalScore"]
        time = to_timestamp(roll["rolledAt"])
        user_roll = UserRolls(number, time, score)
        user_rolls.append(user_roll)
    return user_rolls


def to_timestamp(date):
    dt = datetime.fromisoformat(date.replace("Z", "+00:00"))
    timestamp = int(dt.timestamp() * 1000)
    return timestamp


class RNGdle:
    def __init__(self):
        self.api_url = (
            "https://www.rngdle.com/api/users/{}/rolls?limit=100&offset={}"
        )

    def get_user_rolls(
        self, username, previous_roll: list[UserRolls] = [], offset=0
    ) -> list[UserRolls] | None:
        url = self.api_url.format(username, offset)
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            user_roll = to_user_rolls(result["rolls"])
            previous_roll += user_roll
            if result["hasMore"]:
                self.get_user_rolls(username, previous_roll, offset + 100)
            return previous_roll
        else:
            return None
