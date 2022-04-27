import os

from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from dragnet import extract_content, extract_content_and_comments


USERNAME = os.getenv("USR", "admin")
PASSWORD = generate_password_hash(os.getenv("PASSWD", "secret"))

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username == USERNAME and check_password_hash(PASSWORD, password):
        return username


@app.post("/extract_content")
@auth.login_required
def content():
    data_src = request.get_json() if request.is_json else request.form
    html = data_src.get('html', '')
    content_ = extract_content(html)

    if request.is_json:
        return jsonify({'content': content_})
    else:
        return content_


@app.post("/extract_content_and_comments")
@auth.login_required
def content_and_comments():
    data_src = request.get_json() if request.is_json else request.form
    html = data_src.get('html', '')
    content_and_comments_ = extract_content_and_comments(html)

    if request.is_json:
        return jsonify({'content_and_comments': content_and_comments_})
    else:
        return content_and_comments_
