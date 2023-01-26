import os
import requests
from datetime import timedelta
from flask_login import login_user
from app.backend.models.client import Client


URI: str = os.environ["API_URI"]


class AuthApi:
    @staticmethod
    def post_login(**kwargs) -> tuple[bool, str]:
        resp = requests.post(URI + "token", data=kwargs)
        if resp.ok:

            client = Client()
            client.refresh = resp.json().get("refresh_token")

            login_user(
                client,
                remember=kwargs["remember"],
                duration=timedelta(minutes=15),
                fresh=True,
            )
        return resp.ok, resp.json().get("detail")

    @staticmethod
    def post_refresh(**kwargs) -> Client | None:
        resp = requests.post(URI + "refresh", data=kwargs)
        if resp.ok:

            client = Client()
            client.refresh = resp.json().get("refresh_token")
            return client
        return None

    @staticmethod
    def post_register(**kwargs) -> tuple[bool, str]:
        resp = requests.post(URI + "users", json=kwargs)

        return resp.ok, resp.json().get("detail")

    @staticmethod
    def post_recover_password(**kwargs) -> tuple[bool, str]:
        resp = requests.post(URI + "password", data=kwargs)

        return resp.ok, resp.json().get("detail")

    @staticmethod
    def patch_reset_password(token: str, **kwargs) -> tuple[bool, str]:
        resp = requests.patch(URI + f"password/{token}", data=kwargs)

        return resp.ok, resp.json().get("detail")
