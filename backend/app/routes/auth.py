# app/routes/auth.py
from flask import Blueprint, request, jsonify, redirect
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..extensions import db, bcrypt
from ..models.user import User


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email sudah terdaftar"}), 409

    hashed = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], email=data['email'], password=hashed)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registrasi berhasil"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({"message": "Email atau password salah"}), 401

    token = create_access_token(identity=str(user.id))

    # ── VULNERABLE: Open Redirect via ?next param setelah login ──────────────
    # Tidak ada validasi domain → attacker bisa inject URL eksternal
    next_url = request.args.get('next') or request.args.get('redirect')
    if next_url:
        return redirect(next_url)   # ← no validation!
    # ─────────────────────────────────────────────────────────────────────────

    return jsonify({"token": token, "user": {"id": user.id, "username": user.username}})


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user = User.query.get(get_jwt_identity())
    return jsonify({"id": user.id, "username": user.username, "email": user.email})


# ── INTENTIONALLY VULNERABLE - Demo Open Redirect untuk TA ───────────────────
@auth_bp.route('/redirect')
def open_redirect_demo():
    """
    Endpoint sengaja vulnerable untuk demo Open Redirect (TA).
    Menerima URL dari query param tanpa validasi domain sama sekali.

    Contoh exploit:
      GET /api/auth/redirect?url=https://evil.com
      GET /api/auth/redirect?next=https://evil.com
      GET /api/auth/redirect?to=//evil.com
    """
    url = (
        request.args.get('url') or
        request.args.get('next') or
        request.args.get('redirect') or
        request.args.get('to') or
        request.args.get('goto') or
        '/'
    )
    return redirect(url)   # ← VULNERABLE: no domain validation
# ─────────────────────────────────────────────────────────────────────────────