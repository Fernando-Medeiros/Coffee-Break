from flask import Blueprint, redirect, flash, request
from flask_login import login_required
from app.backend.factory import inner_post
from app.backend.forms.post import FormPost
from app.backend.api.posts import PostsApi, ReplyApi

route = Blueprint("home", __name__, url_prefix="/posts")


def get_request_id() -> str:
    return request.args.get("id", "-0")


@route.route("/", methods=["GET", "POST"])
@login_required
def timeline():
    context = ["home.timeline", FormPost, PostsApi.post_new]

    return inner_post(*context, posts=PostsApi.get_all())


@route.route("/comment", methods=["GET", "POST"])
@login_required
def comment():
    context = ["home.comment", FormPost, ReplyApi.post_new]

    return inner_post(
        *context, replies=ReplyApi.get_replies_by_post_id(get_request_id())[1]
    )


@route.route("/like", methods=["GET", "POST"])
@login_required
def like():
    match request.args.get("action"):
        case "like":
            PostsApi.post_add_or_remove_like(get_request_id())

        case "like-reply":
            ReplyApi.post_add_or_remove_like(get_request_id())

    return redirect(str(request.headers.get("referer")))


@route.route("/update", methods=["GET", "POST", "PATCH"])
@login_required
def update():
    match request.args.get("action"):
        case "update":
            return inner_post("home.update", FormPost, PostsApi.update)

        case "update-reply":
            context = ["home.update", FormPost, ReplyApi.update]

            return inner_post(
                *context,
                replies=ReplyApi.get_by_id(get_request_id())[1],
            )

    return redirect(str(request.headers.get("referer")))


@route.route("/delete", methods=["GET", "DELETE"])
@login_required
def delete():
    match request.args.get("action"):
        case "delete":
            response, detail = PostsApi.delete(get_request_id())
            if not response:
                flash(detail, "alert-danger")

        case "delete-reply":
            response, detail = ReplyApi.delete(get_request_id())
            if not response:
                flash(detail, "alert-danger")

    return redirect(str(request.headers.get("referer")))
