from flask import Blueprint, redirect, request, url_for
from flask_login import current_user, login_required, logout_user

from app.backend.factory import inner_auth
from app.backend.api.auth import AuthApi
from app.backend.forms.auth import (
    FormLogin,
    FormNewAccount,
    FormSendToken,
    FormNewPassword,
)
from setup import login_manager

route = Blueprint("auth", __name__)


@route.route("/", methods=["GET", "POST"])
def login():

    return inner_auth("home.timeline", FormLogin, AuthApi.post_login)


@route.route("/register", methods=["GET", "POST"])
def register():

    return inner_auth("auth.login", FormNewAccount, AuthApi.post_register)


@route.route("/recover", methods=["GET", "POST"])
def recover():

    return inner_auth("auth.login", FormSendToken, AuthApi.post_recover_password)


@route.route("/reset/<token>", methods=["GET", "POST"])
def reset(token: str):

    return inner_auth("auth.login", FormNewPassword, AuthApi.patch_reset_password)


@login_manager.user_loader
def load_current_client(refresh_token):
    client_or_none = AuthApi.post_refresh(refresh_token=refresh_token)

    return client_or_none


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
