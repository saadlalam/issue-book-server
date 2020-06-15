from flask import Blueprint, request, jsonify, make_response


import datetime
import json
import logging
import uuid

from app.services.firestore import Firestore

from app.models.user import User, Role

from app.utils import *

users = Blueprint('users', __name__)
firestore_service = Firestore()


@users.route('/create', methods=['POST'])
@get_claims
def get(claims):
    data = request.get_json()
    user = firestore_service.get_user(claims['user_id'])
    if user.role is Role.MANAGER:
        try:
            userId = firestore_service.create_login_password_user(
                data['email'], data['password'])
            resp = make_response(jsonify({"userId": userId.uid}), 200)
            return resp
        except Exception as e:
            logging.info("Creating user triggered the below error :")
            logging.info(e)

    else:
        return make_response(jsonify({"message": 'unauthorized'}), 403)


@users.route('/getByEmail', methods=['POST'])
@get_claims
def get_user_by_email(claims):
    data = request.get_json()
    email = data['email']
    try:
        user_data = firestore_service.get_user_by_email(email)
        resp = make_response(jsonify({"user": user_data}), 200)
    except Exception as e:
        logging.info("An error occured while trying to get user !")
        logging.info(e)
        return make_response(jsonify({"message": 'Internal error'}), 403)


@users.route('/get', methods=['GET'])
@get_claims
def get_current_user(claims):
    if(claims):
        return make_response(jsonify({"user": claims}))
    else:
        return make_response(jsonify({"message": 'Internal error'}), 403)


@users.route('/delete', methods=['POST'])
@get_claims
def delete(claims):
    data = request.get_json()
    user_id = data['userId']
    try:
        firestore_service.delete_user_document(user_id)
        firestore_service.delete_user_account(user_id)
        resp = make_response(jsonify({"Deleted account : ": user_id}), 200)
        return resp
    except Exception as e:
        logging.info("An error occured while trying to delete the user !")
        logging.info(e)
        return make_response(jsonify({"message": 'Internal error'}), 500)
