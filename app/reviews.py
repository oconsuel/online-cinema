from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Reviews
from auth import check_rights
from app import db

PER_PAGE = 5

bp = Blueprint('reviews', __name__, url_prefix='/reviews')

@bp.route('/unmoderated')
@login_required
@check_rights('moderate_reviews')
def unmoderated():
    page = request.args.get('page', 1, type=int)
    pagination = Reviews.query.order_by(Reviews.created_at.desc()).filter(
        Reviews.status == 'На рассмотрении').paginate(page, PER_PAGE)
    reviews = pagination.items

    return render_template('reviews/unmoderated.html', pagination=pagination, reviews=reviews)

@bp.route('/user_reviews')
@login_required
def user_reviews():
    page = request.args.get('page', 1, type=int)
    pagination = Reviews.query.order_by(Reviews.created_at.desc()).filter(
        Reviews.user == current_user).paginate(page, PER_PAGE)
    reviews = pagination.items

    return render_template('reviews/user_reviews.html', pagination=pagination, reviews=reviews)

@bp.route('/approved')
@login_required
@check_rights('moderate_reviews')
def approved():
    page = request.args.get('page', 1, type=int)
    pagination = Reviews.query.order_by(Reviews.created_at.desc()).filter(
        Reviews.status == 'Одобрено').paginate(page, PER_PAGE)
    reviews = pagination.items

    return render_template('reviews/approved.html', pagination=pagination, reviews=reviews)

@bp.route('/rejected')
@login_required
@check_rights('moderate_reviews')
def rejected():
    page = request.args.get('page', 1, type=int)
    pagination = Reviews.query.order_by(Reviews.created_at.desc()).filter(
        Reviews.status == 'Отклонено').paginate(page, PER_PAGE)
    reviews = pagination.items

    return render_template('reviews/rejected.html', pagination=pagination, reviews=reviews)

@bp.route('/read_review/<int:review_id>')
@login_required
@check_rights('moderate_reviews')
def read_review(review_id):
    review = Reviews.query.filter(Reviews.id == review_id).first()

    return render_template('reviews/read_review.html', review=review)

@bp.route('/confirm_cancel')
@login_required
@check_rights('moderate_reviews')
def confirm_cancel():
    review_id = request.args.get('review_id')
    confirm = request.args.get('confirm')
    print(confirm)

    review = Reviews.query.filter(Reviews.id == review_id).first()

    if confirm == 'true':
        review.status = 'Одобрено'
        review.movie.rating_num = review.movie.rating_num+1
        review.movie.rating_sum = review.movie.rating_sum+int(review.rating)
        print(review.status)
        flash("Рецензия успешно одобрена", "success")
    else:
        review.status = 'Отклонено'
        print(review.status)
        flash("Рецензия успешно отклонена", "success")

    db.session.commit()

    return redirect(url_for('reviews.unmoderated'))