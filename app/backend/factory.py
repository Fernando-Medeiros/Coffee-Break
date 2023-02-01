import os
import base64
from typing import Callable
from flask import flash, redirect, render_template, url_for, request, Response
from flask_wtf.file import FileStorage
from werkzeug.utils import secure_filename

from app.backend.api.posts import PostsApi
from app.backend.api.client import ClientApi


def inner_auth(endpoint: str, formModel: Callable, func: Callable):
    form = formModel()

    if form.validate_on_submit():
        response, detail = func(**form.dict())
        if response:
            flash(detail, "alert-success")
            return redirect(url_for(endpoint))

        flash(detail, "alert-danger")
    return render_template("pages/auth.html", form=form)


def inner_post(endpoint: str, formModel: Callable, func: Callable, **kwargs):
    form = formModel()
    post_id = request.args.get("id", "-0")

    context = {
        "form": form,
        "profiles": ClientApi.get_profiles(),
        "posts": kwargs.get("posts") or PostsApi.get_by_id(post_id)[1],
    }
    context.update(kwargs)

    if form.validate_on_submit():
        response, detail = func(post_id=post_id, **form.dict())
        if response:
            return redirect(url_for(endpoint, id=post_id))

        flash(detail, "alert-danger")
    return render_template("pages/posts.html", **context)


class ConvertBytesToBase64:
    path = "./tmp"

    @classmethod
    def _get_secure_filename(cls, filename: str) -> str:
        return secure_filename(filename)

    @classmethod
    def _save(cls, file: FileStorage, filename) -> None:
        file.save(os.path.join(cls.path, filename))

    @classmethod
    def _read_file(cls, filename) -> bytes:
        with open(f"{cls.path}/{filename}", mode="rb") as file:
            return base64.b64encode(file.read())

    @classmethod
    def _delete_file(cls):
        if len(os.listdir(cls.path)) >= 1:

            for image in os.listdir(cls.path):
                os.remove("{}/{}".format(cls.path, image))

    @classmethod
    def inner(cls, file: FileStorage, func: Callable) -> Response:
        if file.filename is not None:
            filename = cls._get_secure_filename(file.filename)

            cls._save(file, filename)

            if file.content_type.split("/")[1] in ["jpg", "jpeg", "png"]:
                resp, detail = func(image=cls._read_file(filename))

                if resp:
                    flash(detail, "alert-success")
            else:
                flash("Images only", "alert-danger")

            # CLEAR TMP FILES
            cls._delete_file()

        return redirect(url_for("profile.timeline"))
