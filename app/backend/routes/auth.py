from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user

from app.backend.api.auth import AuthApi
from app.backend.forms.auth import (
    FormLogin,
    FormNewAccount,
    FormSendToken,
    FormNewPassword,
)
from setup import login_manager

route = Blueprint("auth", __name__)


@login_manager.user_loader
def load_current_client(refresh_token):
    client_or_none = AuthApi.post_refresh(refresh_token=refresh_token)
    return client_or_none


@route.route("/", methods=["GET", "POST"])
def login():
    form = FormLogin()

    if form.validate_on_submit():
        response, detail = AuthApi.post_login(
            username=form.email.data,
            password=form.password.data,
            remember=form.remember.data,
        )

        if response:
            return redirect(request.args.get("next") or url_for("home.timeline"))

        flash(detail, "alert-danger")

    return render_template("pages/auth.html", form=form)


@route.route("/register", methods=["GET", "POST"])
def register():
    form = FormNewAccount()

    if form.validate_on_submit():
        response, detail = AuthApi.post_register(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        if response:
            flash(detail, "alert-success")
            return redirect(url_for("auth.login"))

        flash(detail, "alert-danger")

    return render_template("pages/auth.html", form=form)


@route.route("/recover", methods=["GET", "POST"])
def recover():
    form = FormSendToken()

    if form.validate_on_submit():
        response, detail = AuthApi.post_recover_password(email=form.email.data)

        if response:
            flash(detail, "alert-success")
            return redirect(url_for("auth.login"))

        flash(detail, "alert-danger")

    return render_template("pages/auth.html", form=form)


@route.route("/reset/<token>", methods=["GET", "POST"])
def reset(token: str):
    form = FormNewPassword()

    if form.validate_on_submit():
        response, detail = AuthApi.patch_reset_password(
            token=token,
            password=form.password.data,
            confirm=form.auth.data,
        )

        if response:
            flash(detail, "alert-success")
            return redirect(url_for("auth.login"))

        flash(detail, "alert-danger")

    return render_template("pages/auth.html", form=form)


@route.route("/logout", methods=["GET"])
@login_required
def logout():

    logout_user()
    return redirect("/")


@route.before_request
def _():
    if current_user.is_authenticated and current_user.is_active:
        if request.endpoint not in ["auth.logout"]:

            return redirect(url_for("home.timeline"))
