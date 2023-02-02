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

    @classmethod
    def upload_avatar(cls, **kwargs) -> tuple[bool, str]:
        resp = requests.patch(
            cls._endpoint("/avatar"), data=kwargs, headers=_authorization()
        )
        return resp.ok, resp.json().get("detail")

    @classmethod
    def upload_background(cls, **kwargs) -> tuple[bool, str]:
        resp = requests.patch(
            cls._endpoint("/background"), data=kwargs, headers=_authorization()
        )
        return resp.ok, resp.json().get("detail")

    @classmethod
    def update_profile(cls, **kwargs) -> tuple[bool, str]:
        """Optional: username, bio"""
        resp = requests.patch(
            cls._endpoint("/profile"), json=kwargs, headers=_authorization()
        )
        return resp.ok, resp.json().get("detail")

    @classmethod
    def update_account(cls, **kwargs) -> tuple[bool, str]:
        """Optional: first name, last name, email"""
        resp = requests.patch(
            cls._endpoint("/account"), json=kwargs, headers=_authorization()
        )
        return resp.ok, resp.json().get("detail")

    @classmethod
    def put_birthday(cls, **kwargs) -> tuple[bool, str]:
        """day, month, year"""
        resp = requests.put(
            cls._endpoint("/birthday"), json=kwargs, headers=_authorization()
        )
        return resp.ok, resp.json().get("detail")
