import os
import requests
from flask_login import current_user

URI: str = os.environ["API_URI"]


def authorization(token: str) -> dict:
    return {"Authorization": "Bearer " + token}


class ClientApi:
    path = "users"

    @classmethod
    def get_profiles(cls) -> list:
        response = requests.get(URI + cls.path)

        return response.json()

    @classmethod
    def get_profile_by_username(cls, username: str) -> dict | str:
        response = requests.get(URI + cls.path + f"/{username}")

        return response.json() or response.json().get("detail")

    @classmethod
    def get_account_data(cls) -> dict:
        response = requests.get(
            URI + cls.path + "/account/",
            headers=authorization(current_user.refresh),
        )

        return response.json()

    @classmethod
    def delete(cls) -> str:
        response = requests.delete(
            URI + cls.path, headers=authorization(current_user.refresh)
        )

        return response.json().get("detail")

    # up account
    # up profile
    # post birthday
    # up birthday
    # up avatar
