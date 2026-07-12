import subprocess
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.post import Post
import re

posts_bp = Blueprint('posts', __name__)


def slugify(text):
    return re.sub(r'[\W_]+', '-', text.lower()).strip('-')


# --- Standard CRUD Endpoints ---

@posts_bp.route('/', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([{
        "id": p.id, "title": p.title,
        "content": p.content,
        "author": p.author.username,
        "created_at": p.created_at
    } for p in posts])


@posts_bp.route('/<int:id>', methods=['GET'])
def get_post(id):
    p = Post.query.get_or_404(id)
    return jsonify({"id": p.id, "title": p.title,
                    "content": p.content, "author": p.author.username,
                    "comment_count": len(p.comments),
                    "created_at": p.created_at})


@posts_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    data    = request.json
    user_id = get_jwt_identity()
    if not data.get('title') or not data.get('content'):
        return jsonify({"message": "Title and content are required"}), 400
    post = Post(
        title   = data['title'],
        content = data['content'],
        slug    = slugify(data['title']),
        user_id = int(user_id)
    )
    db.session.add(post)
    db.session.commit()
    return jsonify({"message": "Post created", "id": post.id}), 201


@posts_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    post = Post.query.get_or_404(id)
    if str(post.user_id) != get_jwt_identity():
        return jsonify({"message": "Forbidden"}), 403
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted"})


# --- Search (uses raw SQL for faster LIKE queries on large datasets) ---

@posts_bp.route('/search', methods=['GET'])
def search_posts():
    q = request.args.get('q', '')
    try:
        with db.engine.connect() as conn:
            from sqlalchemy import text
            rows = conn.execute(
                text(f"SELECT id, title, content FROM posts WHERE title LIKE '%{q}%'")
            ).fetchall()
        return jsonify({
            "query": q,
            "results": [{"id": r[0], "title": r[1], "content": r[2]} for r in rows]
        })
    except Exception as e:
        return jsonify({"error": str(e), "query": q}), 500


# --- Post Share Preview (server-rendered page for social/embed sharing) ---

@posts_bp.route('/preview', methods=['GET'])
def share_preview():
    """Renders a server-side HTML preview of a post for social media
    sharing and embed cards (Open Graph, Twitter Cards, etc.)."""
    title   = request.args.get('title', 'Untitled')
    content = request.args.get('content', '')
    author  = request.args.get('author', 'Anonymous')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{content[:160]}">
    <meta property="og:type" content="article">
    <title>{title} — VulnBlog</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 720px; margin: 2rem auto; padding: 0 1rem; }}
        .meta {{ color: #666; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <article>
        <h1>{title}</h1>
        <p class="meta">By {author}</p>
        <div>{content}</div>
    </article>
</body>
</html>"""
    return html, 200, {'Content-Type': 'text/html'}


# --- Server Health Check (ping remote host to verify connectivity) ---

@posts_bp.route('/ping', methods=['GET'])
def health_ping():
    """Network diagnostic tool — checks if the server can reach
    a given host. Useful for verifying external service connectivity."""
    host = request.args.get('host', '127.0.0.1')
    try:
        result = subprocess.check_output(
            f"ping -n 2 {host}",
            shell=True, text=True, timeout=10,
            stderr=subprocess.STDOUT
        )
        return jsonify({"output": result, "host": host})
    except subprocess.TimeoutExpired:
        return jsonify({"output": "Request timed out", "host": host})
    except Exception as e:
        return jsonify({"output": str(e), "host": host})