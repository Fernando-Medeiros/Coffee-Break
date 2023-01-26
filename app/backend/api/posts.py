import os
import requests
from flask_login import current_user

URI: str = os.environ["API_URI"]


def _authorization() -> dict:
    return {"Authorization": "Bearer " + current_user.refresh}


class PostsApi:
    path = "posts"

    @classmethod
    def _endpoint(cls, endpoint: str = "") -> str:
        return URI + cls.path + endpoint

    @classmethod
    def get_all(cls) -> list:
        resp = requests.get(cls._endpoint())

        return resp.json()

    @classmethod
    def get_by_id(cls, post_id) -> tuple[bool, list | str]:
        resp = requests.get(cls._endpoint(f"/{int(post_id)}"))

        return resp.ok, [resp.json()] or resp.json().get("detail")

    @classmethod
    def get_posts_by_username(cls, username) -> list | str:
        resp = requests.get(cls._endpoint(f"/{username}/posts"))

        return resp.json()

    @classmethod
    def post_new(cls, **kwargs) -> tuple[bool, str]:
        resp = requests.post(
            cls._endpoint(),
            json=kwargs,
            headers=_authorization(),
        )
        return resp.ok, resp.json().get("detail")

    @classmethod
    def post_add_or_remove_like(cls, post_id) -> tuple[bool, str]:
        resp = requests.post(
            cls._endpoint(f"/{int(post_id)}/like"), headers=_authorization()
        )
        return resp.ok, resp.json().get("detail")

    @classmethod
    def delete(cls, post_id) -> tuple[bool, str]:
        resp = requests.delete(
            cls._endpoint(f"/{int(post_id)}"), headers=_authorization()
        )
        return resp.ok, resp.json().get("detail")

    @classmethod
    def update(cls, post_id, **kwargs) -> tuple[bool, str]:
        resp = requests.patch(
            cls._endpoint(f"/{int(post_id)}"),
            json=kwargs,
            headers=_authorization(),
        )
        return resp.ok, resp.json().get("detail")


class ReplyApi(PostsApi):
    path = "replies"

    @classmethod
    def get_replies_by_post_id(cls, reply_id) -> tuple[bool, list | str]:
        resp = requests.get(cls._endpoint(f"/{int(reply_id)}/replies"))

        return resp.ok, resp.json() or ""

    @classmethod
    def post_new(cls, post_id: str, **kwargs) -> tuple[bool, str]:
        resp = requests.post(
            cls._endpoint(f"/{int(post_id)}"),
            json=kwargs,
            headers=_authorization(),
        )
        return resp.ok, resp.json().get("detail")
