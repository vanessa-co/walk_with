from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from config import db
from email_validator import validate_email, EmailNotValidError

class User(db.Model, SerializerMixin):
    __tablename__ = 'user'
    serialize_only = ('id', 'username', 'email')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    walks = db.relationship('Walk', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    followers = db.relationship('Follow', foreign_keys='Follow.followed_id', backref='followed', lazy='dynamic')
    following = db.relationship('Follow', foreign_keys='Follow.follower_id', backref='follower', lazy='dynamic')

    followed_users = association_proxy('following', 'followed')
    follower_users = association_proxy('followers', 'follower')

    @validates('email')
    def validate_email_format(self, key, email):
        try:
            valid_email = validate_email(email)
            return valid_email["email"]
        except EmailNotValidError as e:
            raise ValueError(str(e))

    @validates('username')
    def validate_username_length(self, key, username):
        min_length = 3
        if len(username) < min_length:
            raise ValueError(f"Username must be at least {min_length} characters long.")
        return username

    @validates('password')
    def validate_password_length(self, key, password):
        min_length = 3
        if len(password) < min_length:
            raise ValueError(f"Password must be at least {min_length} characters long.")
        return password

class Walk(db.Model, SerializerMixin):
    __tablename__ = 'walk'
    serialize_only = ('id', 'location', 'distance', 'photo', 'created_at', 'user_id')

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(255), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    photo = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    reviews = db.relationship('Review', backref='walk', lazy=True)

class Review(db.Model, SerializerMixin):
    __tablename__ = 'review'
    serialize_only = ('id', 'text', 'created_at', 'user_id', 'walk_id')

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    walk_id = db.Column(db.Integer, db.ForeignKey('walk.id'), nullable=False)

class Follow(db.Model, SerializerMixin):
    __tablename__ = 'follow'
    serialize_only = ('id', 'created_at', 'follower_id', 'followed_id')

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
