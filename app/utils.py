#!/usr/bin/env python
import coloredlogs
from firebase_admin import auth
from flask import abort, request, make_response, jsonify
from functools import wraps
import logging
import jwt
from app.services.firestore import Firestore
from app.models.user import *
from google.cloud import translate
from google.oauth2 import service_account
from datetime import datetime

firestore_service = Firestore()

credentials = service_account.Credentials.from_service_account_file(
    './config/key.json')


def init_logger():
    """
    Init the logger, loading configuration from config file.
    Args:
        pattern (unicode): Pattern for the logger.
        pattern_debug (unicode): Pattern for the logger in debug mode.
        level (lvl): Level of the logger.
    """
    coloredlogs.install(fmt='%(levelname)-8s %(name)-8s : %(message)s')


def get_claims(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            access_token = request.headers["Authorization"].split(" ")[1]
            claims = auth.verify_id_token(access_token)
        except Exception as e:
            if (str(e)).startswith('Token expired'):
                user_data = jwt.decode(request.headers["Authorization"].split(" ")[
                                       1], 'secret', algorithms=['RS256'])
                new_access_token = auth.create_custom_token(
                    user_data['user_id'])
                claims = auth.verify_id_token(access_token)
            else:
                logging.error(f"Error decoding token: {e}")
                return make_response(jsonify({"result": "Not authorized"}), 401)

        return f(claims)
    return decorated_function


def get_server_date():
    d = datetime.timestamp(datetime.now())
    return d

