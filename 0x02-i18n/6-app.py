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


@app.route("/", methods=["GET"])
def home():
    """Get the locale from request"""
    return render_template("6-index.html")


@babel.localeselector
def get_locale():
    """
    Get the locale from request

    The order of priority for locale is as follows:
    1. Locale from URL parameters
    2. Locale from user settings, if authenticated
    3. Locale from request header
    4. Default locale
    """
    if request.args.get("locale") in app.config["LANGUAGES"]:
        return request.args.get("locale")

    user = getattr(g, "user", None)
    if user and user.get("locale") in app.config["LANGUAGES"]:
        return user.get("locale")

    return request.accept_languages.best_match(app.config["LANGUAGES"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
