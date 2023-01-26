from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from typing import Callable
from app.backend.forms.post import FormPost
from app.backend.api.posts import PostsApi, ReplyApi
from app.backend.api.client import ClientApi

route = Blueprint("home", __name__, url_prefix="/posts")


def inner(endpoint: str, func: Callable, **kwargs):
    form, post_id = FormPost(), request.args.get("id", "-0")

    context = {
        "form": form,
        "profiles": ClientApi.get_profiles(),
        "posts": PostsApi.get_by_id(post_id)[1],
    }
    context.update(kwargs)

    if form.validate_on_submit():
        response, detail = func(post_id=post_id, content=form.content.data)
        if response:
            return redirect(url_for(endpoint, id=post_id))

        flash(detail, "alert-danger")
    return render_template("pages/posts.html", **context)


@route.route("/", methods=["GET", "POST"])
@login_required
def timeline():
    return inner(
        "home.timeline",
        PostsApi.post_new,
        posts=PostsApi.get_all(),
    )


@route.route("/like", methods=["GET", "POST"])
@login_required
def like():
    match request.args.get("action"):
        case "like":
            PostsApi.post_add_or_remove_like(request.args.get("id", "-0"))
        case "like-reply":
            ReplyApi.post_add_or_remove_like(request.args.get("id", "-0"))

    return redirect(str(request.headers.get("referer")))


@route.route("/comment", methods=["GET", "POST"])
@login_required
def comment():
    return inner(
        "home.comment",
        ReplyApi.post_new,
        replies=ReplyApi.get_replies_by_post_id(request.args.get("id", "-0"))[1],
    )


@route.route("/update", methods=["GET", "POST", "PATCH"])
@login_required
def update():
    match request.args.get("action"):
        case "update":
            return inner("home.update", PostsApi.update)

        case "update-reply":
            return inner(
                "home.update",
                ReplyApi.update,
                replies=ReplyApi.get_by_id(request.args.get("id", "-0"))[1],
            )

    return redirect(str(request.headers.get("referer")))


@route.route("/delete", methods=["GET", "DELETE"])
@login_required
def delete():
    match request.args.get("action"):
        case "delete":
            response, detail = PostsApi.delete(request.args.get("id", "-0"))
            if not response:
                flash(detail, "alert-danger")

        case "delete-reply":
            response, detail = ReplyApi.delete(request.args.get("id", "-0"))
            if not response:
                flash(detail, "alert-danger")

    return redirect(str(request.headers.get("referer")))
