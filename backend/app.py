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
    threshold = db.Column(db.Float, default=-7)
    volume = db.Column(db.Integer, default=0)
    enabled = db.Column(db.Boolean, default=False)
    reports = db.relationship('Report', backref='shush_bot', cascade="all, delete-orphan")


    def __init__(self, *args, **kwargs):
        super(ShushBot, self).__init__(*args, **kwargs)
        self.name = "ShushBot-{}".format(self.id)

    def __repr__(self):
        return '<ShushBot {}>'.format(self.id)


class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer(), primary_key=True)
    timestamp = db.Column(db.DateTime)
    threshold = db.Column(db.Float)
    decibels = db.Column(db.Float())
    shush = db.Column(db.Boolean)
    shush_bot_id = db.Column(db.Integer(), db.ForeignKey('shush_bots.id'))

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


def transform_bot(bot):
    configuration = dict(
        id=bot.id,
        threshold=bot.threshold,
    )

    return dict(
        name=bot.name,
        configuration=configuration
    )


# Routes
@app.route('/')
def hello():
    return app.send_static_file('index.html')


@app.route('/js/<path:path>')
def return_static_files(path):
    return app.send_static_file(path)


@app.route('/bots')
def get_bots():
    bots = ShushBot.query.all()

    res = dict(
        bots=[transform_bot(bot) for bot in bots]
    )
    return json.jsonify(res)


@app.route('/bots/<bot_id>')
def get_bot(bot_id):
    bot = get_bot_or_404(bot_id)
    res = dict(
        threshold=bot.threshold,
        volume=bot.volume,
        enabled=bot.enabled
    )
    return json.jsonify(res)


@app.route('/bots/<bot_id>/configuration', methods=['GET', 'POST'])
def get_configuration(bot_id):
    if request.method == 'POST':
        bot = get_bot_or_404(bot_id)
        bot.threshold = float(request.form['threshold'])
        try:
            db.session.add(bot)
        except Exception:
            db.session.rollback()
        db.session.commit()

        return json.jsonify(transform_bot(bot))

    # GET Request
    bot = get_bot_or_create(bot_id)
    res = dict(
        threshold=bot.threshold,
        volume=bot.volume,
        enabled=bot.enabled
    )
    return json.jsonify(res)


if __name__ == '__main__':
    with app.app_context():
        current_app.config.from_object('settings')
        db.create_all()
    app.run()
