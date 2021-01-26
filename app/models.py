import os
from flask import url_for
import sqlalchemy as sa
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import markdown
from app import db
from users_policy import UsersPolicy
from sqlalchemy.dialects import mysql


class Genres(db.Model): #таблица жанры
    __tablename__ = 'exam_genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)

    def __repr__(self):
        return '<Genres %r' % self.name

#связь жанр фильма
genres = db.Table('exam_genre_movie', db.Column('movie_id', db.Integer, db.ForeignKey('exam_movies.id'), primary_key=True), db.Column('genre_id', db.Integer, db.ForeignKey('exam_genres.id'), primary_key=True))

class Movies(db.Model): #таблица фильмы
    __tablename__ = 'exam_movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    production_year = db.Column(mysql.YEAR, nullable=False)
    country = db.Column(db.String(128), nullable=False)
    producer = db.Column(db.String(128), nullable=False)
    scenarist = db.Column(db.String(128), nullable=False)
    actors = db.Column(db.String(256), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    rating_sum = db.Column(db.Integer, default=0)
    rating_num = db.Column(db.Integer, default=0)
    poster_id = db.Column(db.String(36), db.ForeignKey('exam_posters.id'), nullable=False)
    poster = db.relationship('Posters', backref='movies')
    genres = db.relationship('Genres', secondary=genres, backref=db.backref('movies', lazy='dynamic'))

    def __repr__(self):
        return '<Movies %r>' % self.name

    @property
    def html(self):
        return markdown.markdown(self.description)

#таблица с постерами
class Posters(db.Model):
    __tablename__ = 'exam_posters'

    id = db.Column(db.String(36), primary_key=True)
    file_name = db.Column(db.String(128), nullable=False)
    mime_type = db.Column(db.String(128), nullable=False)
    md5_hash = db.Column(db.String(128), nullable=False, unique=True)

    def __repr__(self):
        return '<Posters %r>' % self.name

    @property
    def url(self):
        return url_for('image', image_id=self.id)

    @property
    def storage_filename(self):
        _, ext = os.path.splitext(self.file_name)
        return self.id + ext

class Reviews(db.Model): #таблица рецензии
    __tablename__ = 'exam_reviews'

    id = db.Column(db.Integer, primary_key=True)
    

    movie_id = db.Column(db.Integer, db.ForeignKey('exam_movies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('exam_users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=sa.sql.func.now())
    movie = db.relationship('Movies', backref='reviews')
    user = db.relationship('Users', backref='reviews')
    status = db.Column(db.String(128), db.ForeignKey('exam_statuses.name'), nullable=False, default='На рассмотрении')

    def __repr__(self):
        return '<Reviews %r>' % self.status
    
    @property
    def html(self):
        return markdown.markdown(self.text)

class Users(db.Model, UserMixin): #Таблица пользоватлеи
    __tablename__ = 'exam_users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    middle_name = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('exam_roles.id'))
    role = db.relationship('Roles', backref='users')

    def __repr__(self):
        return '<Users %r>' % self.name

    @property
    def full_name(self):
        return ' '.join([self.last_name, self.first_name, self.middle_name or ''])

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def can(self, action, record=None):
        policy = UsersPolicy(record=record)
        method = getattr(policy, action, None)
        if method:
            return method()
        return False


class Roles(db.Model): #Таблица роли
    __tablename__ = 'exam_roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return '<Roles %r>' % self.name

class Status(db.Model):
    __tablename__ = 'exam_statuses'

    name = db.Column(db.String(128), primary_key=True)