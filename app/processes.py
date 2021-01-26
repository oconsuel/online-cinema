import os
import bleach
from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from flask_login import login_required, current_user
from models import Movies, Genres, Reviews
from auth import check_rights
from tools import PostersSaver
from config import UPLOAD_FOLDER
from app import db

bp = Blueprint('processes', __name__, url_prefix='/processes')

PERMITTED_PARAMS = ['name', 'production_year', 'country', 'producer', 'scenarist', 'actors', 'duration']
PERMITTED_REVIEW_PARAMS = ['user_id', 'movie_id', 'text', 'rating']

PER_PAGE = 5

def params():
    return { p: request.form.get(p) for p in PERMITTED_PARAMS }


def review_params():
    return { p: request.form.get(p) for p in PERMITTED_REVIEW_PARAMS }

@bp.route('/create', methods=['POST'])
@login_required
@check_rights('create_movie')
def create():
    f = request.files.get('background_img') 
    img = None
    if f and f.filename:
        img_saver = PostersSaver(f)
        img = img_saver.save()

    description = bleach.clean(request.form.get('description'))
    movie = Movies(**params(), poster_id=img.id, description=description)
    db.session.add(movie)
    db.session.commit()

    if img:
        img_saver.bind_to_object(movie)

    flash(f'Фильм {movie.name} был успешно создан!', 'success')

    return redirect(url_for('index'))

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
                if review.is_moderated:
                    ncur.append(review)
    else:
        notcurr = movie.reviews
    
    return render_template('processes/check_film.html', movie=movie, notcurr=notcurr, currentuser=currentuser)


@bp.route('/update/<int:movie_id>', methods=['GET','POST'])
@login_required
@check_rights('update_movie')
def update(movie_id):
    movie = Movies.query.get(movie_id)
    genres = Genres.query.all()
    return render_template('processes/update.html', movie=movie, genres=genres)




@bp.route('<int:course_id>/reviews', methods=['GET','POST'])
def reviews(course_id):
    course = Course.query.get(course_id)
    
    if request.method == "POST":
        review = Review(**review_params())
        db.session.add(review)
        db.session.commit()
        course.rating_num = course.rating_num+1
        course.rating_sum = course.rating_sum+int(request.form.get('rating'))
        db.session.add(course)
        db.session.commit()
        flash("Отзыв успешно оставлен", "success")

        return  redirect(url_for('courses.reviews',course_id=course_id, course=course))


    page = request.args.get('page', 1, type=int)
    review_filter = ReviewsFilter(**search_review_params(course_id))
    rewiews = review_filter.perform()

    curse = None
    for review in rewiews:
        if current_user.is_authenticated:
            if current_user.id == review.user_id:
                curse = review

    if current_user.is_authenticated and curse:
        rewiews = rewiews.filter(Review.user_id != curse.user_id)
    pagination = rewiews.paginate(page, PER_PAGE)
    rewiews = pagination.items

    return render_template('/courses/reviews.html', course=course, rewiews=rewiews,curse=curse, pagination=pagination, search_params=search_review_params(course_id), course_id=course_id
    )

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