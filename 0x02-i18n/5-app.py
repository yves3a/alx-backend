#!/usr/bin/env python3

"""A simple flask app."""

from flask import Flask, g, render_template, request
from flask_babel import Babel

app = Flask(__name__)
app.url_map.strict_slashes = False

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Config for the app."""

    DEBUG = True
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app)


@app.route("/", methods=["GET"])
def home():
    """Get the locale from request"""
    return render_template("5-index.html")


@babel.localeselector
def get_locale():
    """Get the locale from request"""
    if request.args.get("locale") in app.config["LANGUAGES"]:
        return request.args.get("locale")

    return request.accept_languages.best_match(app.config["LANGUAGES"])


def get_user():
    """Get user from request"""
    try:
        return users.get(int(request.args.get("login_as")))
    except TypeError:
        return None


@app.before_request
def before_request():
    """Get user from request"""
    user = get_user()
    if user:
        g.user = user


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
