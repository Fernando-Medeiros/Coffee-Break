import os
import requests
from flask_login import current_user

URI: str = os.environ["API_URI"]


def authorization(token: str) -> dict:
    return {"Authorization": "Bearer " + token}


class PostsApi:
    path = "posts"

    @classmethod
    def get_all(cls) -> list:
        response = requests.get(URI + cls.path)
        return response.json()

    @classmethod
    def get_by_id(cls, post_id) -> tuple[bool, list | str]:
        response = requests.get(URI + f"{cls.path}/{int(post_id)}")

        return response.ok, [response.json()] or response.json().get("detail")

    @classmethod
    def get_posts_by_username(cls, username) -> list | str:
        response = requests.get(URI + cls.path + f"/{username}/posts")

        return response.json()

    @classmethod
    def post_new(cls, **kwargs) -> tuple[bool, str]:
        response = requests.post(
            URI + cls.path,
            json=kwargs,
            headers=authorization(current_user.refresh),
        )
        return response.ok, response.json().get("detail")

    @classmethod
    def post_add_or_remove_like(cls, post_id) -> tuple[bool, str]:
        response = requests.post(
            URI + f"{cls.path}/{int(post_id)}/like",
            headers=authorization(current_user.refresh),
        )

        return response.ok, response.json().get("detail")

    @classmethod
    def delete(cls, post_id) -> tuple[bool, str]:
        response = requests.delete(
            URI + f"{cls.path}/{int(post_id)}",
            headers=authorization(current_user.refresh),
        )

        return response.ok, response.json().get("detail")

    @classmethod
    def update(cls, post_id, **kwargs) -> tuple[bool, str]:
        response = requests.patch(
            URI + f"{cls.path}/{int(post_id)}",
            json=kwargs,
            headers=authorization(current_user.refresh),
        )

        return response.ok, response.json().get("detail")


class ReplyApi(PostsApi):
    path = "replies"

    @classmethod
    def get_replies_by_post_id(cls, post_id) -> tuple[bool, list | str]:
        response = requests.get(URI + f"{cls.path}/{int(post_id)}/replies")

        return response.ok, response.json() or ""

    @classmethod
    def post_new(cls, post_id: str, **kwargs) -> tuple[bool, str]:
        response = requests.post(
            URI + f"{cls.path}/{int(post_id)}",
            json=kwargs,
            headers=authorization(current_user.refresh),
        )
        return response.ok, response.json().get("detail")
