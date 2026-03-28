# app/utils/response.py
from flask import jsonify

def success(data=None, message="OK", code=200):
    return jsonify({"status": "success", "message": message, "data": data}), code

def error(message="Error", code=400):
    return jsonify({"status": "error", "message": message}), code