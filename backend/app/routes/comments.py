from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.comment import Comment
from ..models.post import Post
from ..models.user import User

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    """List all comments for a given post."""
    Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id)\
        .order_by(Comment.created_at.asc()).all()
    return jsonify([{
        "id": c.id,
        "content": c.content,
        "author": c.commenter.username,
        "created_at": c.created_at.isoformat() if c.created_at else None
    } for c in comments])


@comments_bp.route('/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    """Add a comment to a post. Requires authentication."""
    Post.query.get_or_404(post_id)
    data = request.json
    if not data or not data.get('content', '').strip():
        return jsonify({"message": "Comment content is required"}), 400

    comment = Comment(
        content = data['content'],
        user_id = int(get_jwt_identity()),
        post_id = post_id
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({
        "message": "Comment added",
        "id": comment.id,
        "content": comment.content,
        "author": comment.commenter.username,
        "created_at": comment.created_at.isoformat() if comment.created_at else None
    }), 201


@comments_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """Delete a comment. Only the comment author or an admin can delete."""
    comment = Comment.query.get_or_404(comment_id)
    user = User.query.get(int(get_jwt_identity()))

    if str(comment.user_id) != get_jwt_identity() and user.role != 'admin':
        return jsonify({"message": "Forbidden"}), 403

    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted"})
