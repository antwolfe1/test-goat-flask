# from flask import current_app
# from flask_sqlalchemy import SQLAlchemy
#
# DB_PATH = 'sqlite:///goat.sqlite'
# db = SQLAlchemy()
#
# def get_db(app):
#     app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
#
#     db.app = app
#     db.init_app(app)
#     with app.app_context():
#         db.create_all()
#
#
#
# class Item(db.Model):
#     text = db.Column(db.String(200), nullable = False)
