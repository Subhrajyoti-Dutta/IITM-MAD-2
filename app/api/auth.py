from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api, abort
from app.models import *
import random

auth_blueprint = Blueprint('auth', __name__)
api = Api(auth_blueprint)

def abort_if_user_doesnt_exist(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, message=f"Influencer {user_id} doesn't exist")

class UserAPI(Resource):
    def get(self, user_id):
        abort_if_user_doesnt_exist(user_id)
        user = User.query.get(user_id)
        return jsonify(user.to_dict())

    def put(self, user_id):
        abort_if_user_doesnt_exist(user_id)
        user = User.query.get(user_id)
        data = request.get_json()

        user.user_id = data.get('username', user.username)
        user.password = data.get('password', user.password)  # You should hash the password in a real application
        user.role = data.get('role', user.role)

        db.session.commit()
        return jsonify(user.to_dict())

    def post(self):
        data = request.get_json()
        while True:
            new_id = random.randint(1, 2**31 - 1)
            if not User.query.get(new_id):
                break
        new_user = User(
            id = new_id,
            username=data.get('username'),
            password=data.get('password'),  # You should hash the password in a real application
            role=data.get('role')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201

    def delete(self, user_id):
        abort_if_user_doesnt_exist(user_id)
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

class UserListAPI(Resource):
    def get(self):
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])