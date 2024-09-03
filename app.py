import os.path

from flask import Flask, render_template, request, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'goat.sqlite')}"
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)

class CRUD:

    def save(self):
        # print(self.text)
        if self.text:
            db.session.add(self)
            db.session.commit()



class Item(db.Model, CRUD):
    # __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(200), nullable = False)

    # def all(self):
    #     print(Item.query.all())
    #     print(self.query.all())

    def delete_all(self):
        db.session.query(Item).delete()
        db.session.commit()

    def __repr__(self):
        return '<Item %r>' % self.text


@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        response = {"new_item_text": request.form.get('item_text', "")}
        item = Item()
        item.text = response.get("new_item_text", "")
        item.save()
        return redirect("/")

    items = Item.query.all()
    return render_template("index.html", items=items)

if __name__ == "__main__":
    app.run(debug=True)

