import logging

from flask import Flask, render_template, request

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        response = {"new_item_text": request.form.get('item_text', "")}
        item = response.get("new_item_text", "")
        return render_template("index.html", item=item)

    return render_template("index.html")
