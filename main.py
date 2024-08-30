import logging

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goat.db'
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(200), nullable = False)
    # print(db.__dict__)

    def save(self):
        if not self.text:
            pass
        else:
            print(self.text)
            db.session.add(self)
            db.session.commit()


@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        response = {"new_item_text": request.form.get('item_text', "")}
        item = response.get("new_item_text", "")
        return render_template("index.html", item=item)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

