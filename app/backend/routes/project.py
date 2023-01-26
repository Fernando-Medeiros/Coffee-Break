import os

from flask import Blueprint, render_template
from flask_login import login_required

route = Blueprint("project", __name__, url_prefix="/project")


@route.route("/", methods=["GET"])
@login_required
def about():
    context = {
        "api_img": os.environ["API_IMG"],
        "app_img": os.environ["APP_IMG"],
        "api_url": os.environ["API_URL"],
        "app_url": os.environ["APP_URL"],
    }
    return render_template("pages/project.html", **context)
