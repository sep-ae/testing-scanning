from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from ..extensions import db
from ..models.user import User
from ..models.post import Post
from ..models.comment import Comment

admin_bp = Blueprint('admin', __name__)


def admin_required(fn):
    """Decorator that checks if the current user has admin role."""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = User.query.get(int(get_jwt_identity()))
        if not user or user.role != 'admin':
            return jsonify({"message": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


# --- Stats ---

@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats():
    """Overview stats for the admin dashboard."""
    return jsonify({
        "total_users":    User.query.count(),
        "total_posts":    Post.query.count(),
        "total_comments": Comment.query.count()
    })


# --- User Management ---

@admin_bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    """List all registered users."""
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify([{
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "role": u.role,
        "created_at": u.created_at.isoformat() if u.created_at else None,
        "post_count": len(u.posts),
        "comment_count": len(u.comments)
    } for u in users])


@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete a user and all their posts and comments."""
    user = User.query.get_or_404(user_id)
    if str(user.id) == get_jwt_identity():
        return jsonify({"message": "Cannot delete yourself"}), 400
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})


@admin_bp.route('/users/<int:user_id>', methods=['PATCH'])
@admin_required
def update_user_role(user_id):
    """Change a user's role (user/admin)."""
    user = User.query.get_or_404(user_id)
    data = request.json
    if data.get('role') not in ('user', 'admin'):
        return jsonify({"message": "Role must be 'user' or 'admin'"}), 400
    user.role = data['role']
    db.session.commit()
    return jsonify({"message": f"User role updated to {user.role}"})


# --- Post Management ---

@admin_bp.route('/posts', methods=['GET'])
@admin_required
def list_posts():
    """List all posts with author info."""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([{
        "id": p.id,
        "title": p.title,
        "author": p.author.username,
        "comment_count": len(p.comments),
        "created_at": p.created_at.isoformat() if p.created_at else None
    } for p in posts])


@admin_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@admin_required
def delete_post(post_id):
    """Delete any post (admin privilege)."""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted"})


# --- Comment Management ---

@admin_bp.route('/comments', methods=['GET'])
@admin_required
def list_comments():
    """List all comments across all posts."""
    comments = Comment.query.order_by(Comment.created_at.desc()).all()
    return jsonify([{
        "id": c.id,
        "content": c.content,
        "author": c.commenter.username,
        "post_id": c.post_id,
        "post_title": c.post.title,
        "created_at": c.created_at.isoformat() if c.created_at else None
    } for c in comments])


@admin_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@admin_required
def delete_comment(comment_id):
    """Delete any comment (admin privilege)."""
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted"})
