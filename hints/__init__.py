from flask import Flask

# from ctf.error_handlers import register_error_handlers  # Adjust the
# import based on your project structure


def create_app():
    print("Creating app")
    app = Flask(
        __name__,
        static_folder="static",
        static_url_path="/",
        template_folder="templates",
    )
    app.config["SECRET_KEY"] = "CTF_K3YF0RS355i0n5!"
    # ensure session cookie is httponly
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    # ensure session cookie is same site
    app.config["SESSION_COOKIE_SAMESITE"] = "Strict"
    # ensure remember cookie is secure
    app.config["REMEMBER_COOKIE_SECURE"] = True
    # ensure session cookie is secure
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_PERMANENT"] = True
    app.config["PERMANENT_SESSION_LIFETIME"] = 60  # in seconds
    with app.app_context():
        from . import routes

        app.register_blueprint(routes.bp)
    # register_error_handlers(app)
    # app.config['referrer_policy'] = 'strict-origin-when-cross-origin'
    return app


# app = Flask(
#     __name__,
#     static_folder="static",
#     static_url_path="/",
#     template_folder="templates",
# )


# register_error_handlers(app)
# app.config['referrer_policy'] = 'strict-origin-when-cross-origin'
from hints import routes  # nopep8
