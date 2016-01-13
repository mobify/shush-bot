from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ENUM


app = Flask(__name__)
db = SQLAlchemy(app)


class ShushBot(db.Model):
    __tablename__ = 'shush_bots'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    state = db.Column(ENUM('load', 'quiet', 'off'))
    volume = db.Column(db.Integer())
    last_config = db.Column(db.DateTime)

    def __repr__(self):
        return '<ShushBot {}>'.format(self.id)


class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer(), primary_key=True)
    timestamp = db.Column(db.DateTime)
    state = db.Column(ENUM('load', 'quiet', 'off'))
    decibels = db.Column(db.Float())
    shush = db.Column(db.Boolean)


    def __repr__(self):
        return '<Report {}>'.format(self.id)


@app.route('/')
def hello():
    return 'Hello'


if __name__ == '__main__':
    app.run(debug=True)
