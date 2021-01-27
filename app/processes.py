import os
import bleach
from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from flask_login import login_required, current_user
from models import Movies, Genres, Reviews
from auth import check_rights
from tools import PostersSaver
from config import UPLOAD_FOLDER
from app import db
from sqlalchemy import exc

bp = Blueprint('processes', __name__, url_prefix='/processes')

PERMITTED_PARAMS = ['name', 'production_year', 'country', 'producer', 'scenarist', 'actors', 'duration']
PERMITTED_REVIEW_PARAMS = ['user_id', 'movie_id', 'text', 'rating']

def params():
    return { p: request.form.get(p) for p in PERMITTED_PARAMS }


def review_params():
    return { p: request.form.get(p) for p in PERMITTED_REVIEW_PARAMS }

@bp.route('/read/<int:movie_id>/create_review', methods=['POST', 'GET'])
@login_required
def create_review(movie_id):
    movie = Movies.query.get(movie_id)

    if request.method == "POST":
        p = review_params()
        p['user_id'] = current_user.id
        review = Reviews(**p)
        review.text = bleach.clean(request.form.get('text'))
        db.session.add(review)
        db.session.commit()
        movie.rating_num = movie.rating_num+1
        movie.rating_sum = movie.rating_sum+int(request.form.get('rating'))
        db.session.add(movie)
        db.session.commit()
        flash("Рецензия успешно оставлена", "success")

        return redirect(url_for('processes.read', movie_id=movie_id))

    return render_template('reviews/create_review.html', movie_id=movie_id)

@bp.route('/create', methods=['POST'])
@login_required
@check_rights('create_movie')
def create():
    b_img = request.files.get('background_img') 
    img = None
    if b_img and b_img.filename:
        img_saver = PostersSaver(b_img)
        img = img_saver.save()

    if img == None:
        flash(f'Ошибка создания фильма! Нельзя добавить один постер к двум фильмам!', 'danger')
        return redirect(url_for('processes.create'))

    description = bleach.clean(request.form.get('description'))
    genres = request.form.getlist('genre_ids')
    movie = Movies(**params(), poster_id=img.id, description=description)

    try:
        movie = Movie(**params(), poster_id=img.id, description=description)
        if img:
            img_saver.bind_to_object(movie)
    except:
        db.session.rollback()
        flash(f'Ошибка!Повторите ввод!', 'danger')
        return redirect(url_for('crud.create'))

    try:
        db.session.add(movie)

        for genre_id in genres:
            genre = Genre.query.filter(Genre.id == genre_id).first()
            movie.genres.append(genre)

        db.session.commit()
    except exc.DBAPIError or exc.SQLAlchemyError or exc.DatabaseError: 
        flash(f'Ошибка создания фильма! Извините, внесите данные снова :(', 'danger')
        return redirect(url_for('crud.create'))

    flash(f'Фильм {movie.name} был успешно создан!', 'success')

    return redirect(url_for('processes.read', movie_id=movie.id))

@bp.route('/new')
@login_required
@check_rights('create_movie')
def new():
    genres = Genres.query.all()
    return render_template(
        'processes/new.html', 
        genres=genres, movie={} 
        
    )

@bp.route('/read/<int:movie_id>')
def read(movie_id):
    movie = Movies.query.get(movie_id)
    currentuser = None
    notcurr = []
    
    if current_user.is_authenticated:
        for review in movie.reviews:
            if current_user.id == review.user_id:
                currentuser = review
            else:
                if review.status:
                    notcurr.append(review)
    else:
        notcurr = movie.reviews
    
    return render_template('processes/check_film.html', movie=movie, notcurr=notcurr, currentuser=currentuser)


@bp.route('/update/<int:movie_id>', methods=['GET','POST'])
@login_required
@check_rights('update_movie')
def update(movie_id):
    movie = Movies.query.get(movie_id)
    genres = Genres.query.all()
    
    if request.method == "POST":
        description = bleach.clean(request.form.get('description'))
        genres = request.form.getlist('genre_ids')
        movie.name = request.form.get('name')
        movie.production_year = request.form.get('production_year')
        movie.country = request.form.get('country')
        movie.producer = request.form.get('producer')
        movie.scenarist = request.form.get('scenarist')
        movie.actors = request.form.get('actors')
        movie.duration = request.form.get('duration')
        movie.description = description
        
        temp_genres = []
        for i in movie.genres:
            temp_genres.append(i)

        for genre_id_del in temp_genres:
            print('remove' + str(genre_id_del))
            genre_del = Genres.query.filter(Genres.name == genre_id_del.name).first()
            movie.genres.remove(genre_del)
        db.session.add(movie)
        for genre_id_add in genres:
            genre_add = Genres.query.filter(Genres.id == genre_id_add).first()
            if genre_add not in movie.genres:
                movie.genres.append(genre_add)

        db.session.commit()
        flash(f'Фильм {movie.name} был успешно обновлён!', 'success')
        return redirect(url_for('processes.read', movie_id=movie_id))


    return render_template('processes/update.html', movie=movie, genres=genres)

@bp.route('/delete/<int:movie_id>', methods=['POST'])
@login_required
@check_rights('delete_movie')
def delete(movie_id):
    movie = Movies.query.get(movie_id)
    #os.remove(UPLOAD_FOLDER + '/' + str(movie.poster.storage_filename))

    db.session.delete(movie)
    db.session.commit()

    flash('Фильм успешно удалён', 'success')
    return redirect(url_for('index'))