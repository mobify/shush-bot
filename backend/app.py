from flask import abort, current_app, Flask, json, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ENUM, UUID


app = Flask(__name__)
db = SQLAlchemy(app)


# Models
class ShushBot(db.Model):
    __tablename__ = 'shush_bots'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    state = db.Column(db.Integer, default=50)
    volume = db.Column(db.Integer, default=50)
    enabled = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<ShushBot {}>'.format(self.id)


class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer(), primary_key=True)
    timestamp = db.Column(db.DateTime)
    state = db.Column(db.Integer)
    decibels = db.Column(db.Float())
    shush = db.Column(db.Boolean)

    def __repr__(self):
        return '<Report {}>'.format(self.id)


# Utility methods
def get_bot_or_create(bot_id):
    bot = ShushBot.query.get(bot_id)
    if not bot:
        bot = ShushBot(id=bot_id)
        try:
            db.session.add(bot)
        except Exception:
            db.session.rollback()
            abort(500, "Bot could not be created")
        db.session.commit()
    return bot


def get_bot_or_404(bot_id):
    bot = ShushBot.query.get(bot_id)
    if not bot:
        abort(404)
    return bot


# Routes
@app.route('/')
def hello():
    return 'Hello'


@app.route('/bots/<bot_id>')
def get_bot(bot_id):
    bot = get_bot_or_404(bot_id)
    res = dict(
        state=bot.state,
        volume=bot.volume,
        enabled=bot.enabled
    )
    return json.jsonify(res)


@app.route('/bots/<bot_id>/configuration', methods=['GET', 'POST'])
def get_configuration(bot_id):
    if request.method == 'POST':
        bot = get_bot_or_404(bot_id)
        res = dict(
            state=bot.state,
            volume=bot.volume,
            enabled=bot.enabled
        )
        return

    # GET Request
    bot = get_bot_or_create(bot_id)
    res = dict(
        state=bot.state,
        volume=bot.volume,
        enabled=bot.enabled
    )
    return json.jsonify(res)


if __name__ == '__main__':
    with app.app_context():
        current_app.config.from_object('settings')
        db.create_all()
    app.run(debug=True)
