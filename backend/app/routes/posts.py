# app/routes/posts.py
import sqlite3, subprocess
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.post import Post
import re

posts_bp = Blueprint('posts', __name__)

def slugify(text):
    return re.sub(r'[\W_]+', '-', text.lower()).strip('-')

# ============ ENDPOINT NORMAL ============

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
                    "created_at": p.created_at})

@posts_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    data    = request.json
    user_id = get_jwt_identity()
    if not data.get('title') or not data.get('content'):
        return jsonify({"message": "Title dan content wajib diisi"}), 400
    post = Post(
        title   = data['title'],
        content = data['content'],
        slug    = slugify(data['title']),
        user_id = int(user_id)
    )
    db.session.add(post)
    db.session.commit()
    return jsonify({"message": "Post dibuat", "id": post.id}), 201

@posts_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    post = Post.query.get_or_404(id)
    if str(post.user_id) != get_jwt_identity():
        return jsonify({"message": "Forbidden"}), 403
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post dihapus"})


@posts_bp.route('/search', methods=['GET'])
def search_vuln():
    q = request.args.get('q', '')
    try:
        # Pakai db.engine — pasti ketemu DB yang sama
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

@posts_bp.route('/redirect', methods=['GET'])
def open_redirect():
    next_url = request.args.get('next', '/')
    return jsonify({
        "redirect": next_url,
        "message": "Redirecting..."
    })

@posts_bp.route('/ping', methods=['GET'])
def ping_vuln():
    host = request.args.get('host', '127.0.0.1')
    try:
        result = subprocess.check_output(
            f"ping -n 2 {host}",
            shell=True, text=True, timeout=10,
            stderr=subprocess.STDOUT
        )
        return jsonify({"output": result, "host": host})
    except subprocess.TimeoutExpired:
        return jsonify({"output": "timeout", "host": host})
    except Exception as e:
        return jsonify({"output": str(e), "host": host})