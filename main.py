#!/usr/bin/env python
from app.api.posts import posts
from app.api.users import users
from app.utils import get_claims
from app.models.user import *
from flask_cors import CORS
from app.services.firestore import Firestore
from flask import Flask, make_response, jsonify
import json
import logging
import config
from datetime import datetime


app = Flask(__name__)
app.register_blueprint(users, url_prefix=f'/users')
app.register_blueprint(posts, url_prefix=f'/posts')

CORS(app, resources={
     r"/*": {"origins": config.AUTHORIZED_ORIGIN}}, supports_credentials=True)

firestore_service = Firestore()


@app.route('/login', methods=["GET"])
@get_claims
def login(claims):
    try:
        user = firestore_service.get_user(claims['user_id'])
        if user is not None:
            additional_claims = {
                'role': user.role.value
            }
            custom_token = firestore_service.generate_custom_token(
                claims['user_id'], additional_claims)
            resp = make_response(
                jsonify({"result": "Authorized", "token": custom_token.decode("utf-8")}), 200)
            return resp
        else:
            user = firestore_service.get_user_by_email(claims['email'])
            if user:
                firestore_service.initialize_first_connexion(claims, user)
                user = firestore_service.get_user(claims['user_id'])
                additional_claims = {
                    'role': user.role.value
                }
                custom_token = firestore_service.generate_custom_token(
                    claims['user_id'], additional_claims)
                resp = make_response(
                    jsonify({"result": "Authorized", "token": custom_token.decode("utf-8")}), 200)
                return resp
            else:
                resp = make_response(
                    jsonify({"result": "Not authorized"}), 403)
    except Exception as e:
        logging.info(e)
        resp = make_response(jsonify({"result": "Not authorized"}), 403)
        return resp


if __name__ == '__main__':
    app.run(debug=config.DEBUG)
