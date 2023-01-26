import os
import requests
from flask_login import current_user

URI: str = os.environ["API_URI"]


def _authorization() -> dict:
    return {"Authorization": "Bearer " + current_user.refresh}


class ClientApi:
    path = "users"

    @classmethod
    def _endpoint(cls, endpoint: str = "") -> str:
        return URI + cls.path + endpoint

    @classmethod
    def get_profiles(cls) -> list:
        resp = requests.get(cls._endpoint())

        return resp.json()

    @classmethod
    def get_profile_by_username(cls, username: str) -> dict | str:
        resp = requests.get(cls._endpoint(f"/{username}"))

        return resp.json() or resp.json().get("detail")

    @classmethod
    def get_account_data(cls) -> dict:
        resp = requests.get(cls._endpoint("/account/"), headers=_authorization())

        return resp.json()

    @classmethod
    def delete(cls) -> str:
        resp = requests.delete(cls._endpoint(), headers=_authorization())

        return resp.json().get("detail")

    # up account
    # up profile
    # post birthday
    # up birthday
    # up avatar
