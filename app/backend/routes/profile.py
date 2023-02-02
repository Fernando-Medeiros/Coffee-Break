from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required
from app.backend.api.client import ClientApi
from app.backend.api.posts import PostsApi
from app.backend.forms.update import (
    FormUploadAvatar,
    FormUploadBackground,
    FormUpdateBio,
    FormUpdateAccount,
    FormUpdateBirthday,
)
from app.backend.factory import ConvertBytesToBase64

route = Blueprint("profile", __name__, url_prefix="/profile")


@route.route("/", methods=["GET", "POST"])
@login_required
def timeline():
    context = {
        "form_avatar": FormUploadAvatar(),
        "form_background": FormUploadBackground(),
        "form_bio": FormUpdateBio(),
    }

    if "user" in request.args.keys():
        profile = ClientApi.get_profile_by_username(request.args["user"])
    else:
        profile = ClientApi.get_account_data()

        if request.files.get("avatar"):
            return ConvertBytesToBase64.inner(
                request.files["avatar"],
                ClientApi.upload_avatar,
            )
        if request.files.get("background"):
            return ConvertBytesToBase64.inner(
                request.files["background"],
                ClientApi.upload_background,
            )
        if request.form.get("content"):
            ClientApi.update_profile(**context["form_bio"].dict())
            return redirect(url_for("profile.timeline"))

    context.update(
        profile,
        posts=PostsApi.get_posts_by_username(profile["username"]),
    )
    return render_template("pages/profile.html", **context)


@route.route("/update", methods=["GET", "POST"])
@login_required
def update():
    context = {
        "form_account": FormUpdateAccount(),
        "form_birthday": FormUpdateBirthday(),
    }

    if "name" in request.form.keys() or "email" in request.form.keys():
        resp, detail = ClientApi.update_account(**context["form_account"].dict())

        flash(detail, "alert-success") if resp else flash(detail, "alert-danger")

    if request.form.get("date"):
        resp, detail = ClientApi.put_birthday(**context["form_birthday"].dict())

        flash(detail, "alert-success") if resp else flash(detail, "alert-danger")

    return render_template("pages/update.html", **context)


@route.route("/delete", methods=["GET", "DELETE"])
@login_required
def delete():
    detail = ClientApi.delete()
    flash(detail, "alert-info")

    return redirect(url_for("auth.login"))
