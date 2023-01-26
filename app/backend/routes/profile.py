from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required
from app.backend.api.client import ClientApi
from app.backend.api.posts import PostsApi

route = Blueprint("profile", __name__, url_prefix="/profile")


@route.route("/", methods=["GET"])
@login_required
def timeline():
    context = {}

    if "user" in request.args.keys():
        profile = ClientApi.get_profile_by_username(request.args.get("user", ""))
    else:
        profile = ClientApi.get_account_data()

    context.update(
        profile,
        posts=PostsApi.get_posts_by_username(profile["username"])[::-1],
    )
    return render_template("pages/profile.html", **context)


@route.route("/update", methods=["GET", "PATCH"])
@login_required
def update():
    context = {}
    return render_template("pages/update.html", **context)


@route.route("/delete", methods=["GET", "DELETE"])
@login_required
def delete():
    detail = ClientApi.delete()
    flash(detail, "alert-info")
    return redirect("/")
