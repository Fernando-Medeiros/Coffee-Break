from flask import flash, redirect, render_template, url_for, request
from typing import Callable
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
