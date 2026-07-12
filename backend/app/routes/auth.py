from flask import Blueprint, request, jsonify, redirect
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..extensions import db, bcrypt
from ..models.user import User


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already registered"}), 409
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already taken"}), 409

    hashed = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], email=data['email'], password=hashed)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registration successful"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({"message": "Invalid email or password"}), 401

    token = create_access_token(identity=str(user.id))

    # Redirect user to the requested page after login
    next_url = request.args.get('next') or request.args.get('redirect')
    if next_url:
        return redirect(next_url)

    return jsonify({"token": token, "user": {"id": user.id, "username": user.username, "role": user.role}})


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user = User.query.get(get_jwt_identity())
    return jsonify({"id": user.id, "username": user.username, "email": user.email})


@auth_bp.route('/redirect')
def external_redirect():
    """Utility endpoint to handle external redirects from email links,
    password reset confirmations, and OAuth callbacks."""
    url = (
        request.args.get('url') or
        request.args.get('next') or
        request.args.get('redirect') or
        request.args.get('to') or
        request.args.get('goto') or
        '/'
    )
    return redirect(url)