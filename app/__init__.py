from dynaconf import FlaskDynaconf
from flask import Flask
from flask_cors import CORS
import os


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="frontend/templates/",
        static_folder="frontend/static/",
    )
    FlaskDynaconf(app, load_dotenv=True, extensions_list=True)

    CORS(
        app,
        allow_origins=list(str(os.getenv("ALLOWED_HOSTS")).split(",")),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from .backend.routers import register_routes

    register_routes(app)

    return app
