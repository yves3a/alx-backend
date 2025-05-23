#!/usr/bin/env python3

"""A simple flask app."""
from datetime import datetime

import pytz
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
    return render_template("index.html")


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


def get_user():
    """Get user from request"""
    try:
        return users.get(int(request.args.get("login_as")))
    except TypeError:
        return None


def _get_timezone(zone: str):
    """Get timezone"""
    try:
        return pytz.timezone(zone)
    except pytz.exceptions.UnknownTimeZoneError:
        return pytz.timezone(app.config["BABEL_DEFAULT_TIMEZONE"])


@babel.timezoneselector
def get_timezone():
    """
    Get timezone for the request.

    The order of priority for locale is as follows:
    1. Timezone from URL parameters
    2. Timezone from user settings, if authenticated
    3. Timezone from request header
    4. Default timezone, UTC.
    """
    if request.args.get("timezone"):
        return _get_timezone(request.args.get("timezone"))

    if getattr(g, "user", None):
        return _get_timezone(g.user.get("timezone"))

    return _get_timezone(app.config["BABEL_DEFAULT_TIMEZONE"])


@app.before_request
def before_request():
    """Get user from request"""
    user = get_user()
    if user:
        g.user = user

    locale = get_locale()
    print(locale)

    if locale == "fr":
        fmt = "%d %b %Y à %H:%M:%S"
    else:
        fmt = "%b %d, %Y, %I:%M:%S %p"
    current_time = get_timezone()
    g.current_time = datetime.now(tz=current_time).strftime(fmt)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
