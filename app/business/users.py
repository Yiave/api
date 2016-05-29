from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Notebook


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.toJSON())


@api.route('/users/<int:id>/notebooks/')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.notebooks.order_by(Notebook.create_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1, _external=True)
    return jsonify({
        'notebooks': [post.toJSON() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })