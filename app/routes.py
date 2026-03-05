from flask import Blueprint, jsonify, request
from .extensions import db
from .models import User, Post

bp = Blueprint('api', __name__, url_prefix='/api')

# User Routes
@bp.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'email': u.email} for u in users])

@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user"""
    user = User.query.get_or_404(user_id)
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

@bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()
    if not data or not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400

    user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username}), 201

# Post Routes
@bp.route('/posts', methods=['GET'])
def get_posts():
    """Get all posts"""
    posts = Post.query.all()
    return jsonify([{'id': p.id, 'title': p.title, 'user_id': p.user_id} for p in posts])

@bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get a specific post"""
    post = Post.query.get_or_404(post_id)
    return jsonify({'id': post.id, 'title': post.title, 'content': post.content, 'user_id': post.user_id})

@bp.route('/posts', methods=['POST'])
def create_post():
    """Create a new post"""
    data = request.get_json()
    if not data or not all(k in data for k in ['title', 'content', 'user_id']):
        return jsonify({'error': 'Missing required fields'}), 400

    post = Post(title=data['title'], content=data['content'], user_id=data['user_id'])
    db.session.add(post)
    db.session.commit()
    return jsonify({'id': post.id, 'title': post.title}), 201

@bp.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update a post"""
    post = Post.query.get_or_404(post_id)
    data = request.get_json()

    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']

    db.session.commit()
    return jsonify({'id': post.id, 'title': post.title, 'content': post.content})

@bp.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return '', 204

