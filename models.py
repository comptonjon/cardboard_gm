from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 
from constants import AWS_URL
import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class TradeRequest(db.Model):

    __tablename__ = "trade_requests"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    to_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    accepted = db.Column(db.Boolean, default=None)
    valid_items = db.Column(db.Boolean, default=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    #cards = db.relationship('Card', secondary='request_cards', backref="trade_requests", cascade='all, delete-orphan')
    to_user = db.relationship('User', foreign_keys=[to_id], backref="trades_received")
    from_user = db.relationship('User', foreign_keys=[from_id], backref="trades_sent")
    items = db.relationship('RequestCard', backref="request", cascade='all, delete')

class RequestCard(db.Model):

    __tablename__ = "request_cards"

    request_id = db.Column(db.Integer, db.ForeignKey("trade_requests.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey("cards.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    requested = db.Column(db.Boolean, default=False)



class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    img_url = db.Column(db.Text)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    cards = db.relationship("Card", backref="user", order_by="Card.year.desc()", cascade='all, delete-orphan')

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def register(cls, username, password, email, first_name, last_name, img_url=None):

        hashed = bcrypt.generate_password_hash(password)
        pwd_utf8 = hashed.decode("utf8")

        return cls(username=username,
                   password=pwd_utf8,
                   email=email,
                   first_name=first_name,
                   last_name=last_name,
                   img_url=img_url)

    @classmethod
    def authenticate(cls, username, password):

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    def imgurl(self):
        if self.img_url:
            return f"{AWS_URL}{self.img_url}"
        else:
            return None

    def thumburl(self):
        if self.img_url:
            return f"{AWS_URL}profile-images/{self.id}/{self.id}_thumb.JPEG"
        else:
            return None

    def serialize(self):
        return {'username'   : self.username,
                'first_name' : self.first_name,
                'last_name'  : self.last_name,
                'email'      : self.email,
                'id'         : self.id,
                'img_url'    : self.imgurl(),
                'thumb_url'  : self.thumburl()
                }


class CardMaster(db.Model):

    __tablename__ = "card_masters"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player = db.Column(db.String(50), nullable=False)
    set_name = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(20), nullable=False)

class Card(db.Model):

    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #master = db.Column(db.Integer, db.ForeignKey("card_masters.id"))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    player = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    set_name = db.Column(db.Text, nullable=False)
    number = db.Column(db.Text)
    desc = db.Column(db.Text)
    img_url = db.Column(db.Text, default=None)
    title = db.Column(db.Text, default=None)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    requests = db.relationship("TradeRequest", secondary="request_cards", backref="cards", cascade='all, delete')
    grouping = db.relationship("RequestCard", backref="info", cascade='all, delete')

    def serialize(self):
        return {'player'      : self.player,
                'year'        : self.year,
                'set_name'    : self.set_name,
                'number'      : self.number,
                'description' : self.desc,
                'img_url'     : self.img_url,
                'title'       : self.to_string(),
                'thumb_url'   : self.thumb_url(),
                'full_url'    : self.full_img_url(),
                'id'          : self.id }

    def to_string(self):
        return f"{self.year} {self.set_name} #{self.number} {self.player} {self.desc}"

    def full_img_url(self):
        return f"{AWS_URL}{self.img_url}"

    def thumb_url(self):
        if self.img_url:
            thumbnail_url = self.img_url.replace("_full", "_thumb")
            return f"{AWS_URL}{thumbnail_url}"
        else:
            return None

    @classmethod
    def create(cls, owner_id, player, year, set_name, number, desc, img_url=None):
        return cls(owner_id=owner_id, player=player, year=year, set_name=set_name, number=number, desc=desc, title=f"{year} {set_name} #{number} {player} {desc}", img_url=img_url )



