from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "alert-info"


def development(app):
    ...


def production(app):
    login_manager.init_app(app)


def context(app):
    ...


def init_app(app):
    env = app.config.ENV

    if env == "DEV" or env == "TEST":
        development(app)

    production(app)
    context(app)
