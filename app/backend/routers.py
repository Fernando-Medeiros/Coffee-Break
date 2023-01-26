from .routes import auth, home, profile, project


def register_routes(app) -> None:
    routes = [
        auth.route,
        home.route,
        profile.route,
        project.route,
    ]

    for route in routes:
        app.register_blueprint(route)
