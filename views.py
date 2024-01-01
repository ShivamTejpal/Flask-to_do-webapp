# views.py

from urllib.parse import quote_plus, urlencode
from flask import Blueprint, render_template, abort, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import json

# Create a Blueprint
auth_bp = Blueprint('auth', __name__)

# OAuth setup (retain this setup from your code)
oauth = OAuth()
oauth.register(...)

# Define your routes within the Blueprint
@auth_bp.route("/")
def home():
    return render_template(
        "login.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )

@auth_bp.route("/callback")
def callback():
    token = oauth.myApp.authorize_access_token()
    session["user"] = token
    session["user_id"] = token["sub"]
    return redirect(url_for("auth.home"))

@auth_bp.route("/login")
def login():
    if "user" in session:
        abort(404)
    return oauth.myApp.authorize_redirect(redirect_uri='http://127.0.0.1:8000/')

@auth_bp.route("/loggedout")
def loggedOut():
    if "user" in session:
        abort(404)
    return redirect(url_for("auth.home"))

@auth_bp.route("/logout")
def logout():
    id_token = session["user"]["id_token"]
    session.clear()
    return redirect(
        appConf.get("OAUTH2_ISSUER")
        + "/protocol/openid-connect/logout?"
        + urlencode(
            {
                "post_logout_redirect_uri": url_for("auth.loggedOut", _external=True),
                "id_token_hint": id_token
            },
            quote_via=quote_plus,
        )
    )
