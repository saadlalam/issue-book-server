#!/usr/bin/env python
import json
import logging
import firebase_admin

from enum import Enum
from firebase_admin import firestore
from firebase_admin import auth

from app.models.user import User
from datetime import datetime
import time
import datetime as dt

import config

cred = firebase_admin.credentials.Certificate('./config/key.json')
default_app = firebase_admin.initialize_app(cred)


class Firestore():
    def __init__(self, *args, **kwargs):
        self.db = firestore.client()

    def generate_custom_token(self, uid, claims):
        custom_token = auth.create_custom_token(uid, claims)
        return custom_token

    def get_user(self, uid: str):
        result = self.db.collection(config.usersPath).document(uid).get()
        if result.to_dict() is None:
            return None
        user = User(result.to_dict())
        user.id = result.id
        return user

    def get_user_by_email(self, email: str):
        result = self.db.collection(config.usersPath).where(
            'email', '==', email).get()
        result = next(result)
        userSnap = result.to_dict()
        if userSnap is None:
            return None
        user = User(userSnap)
        user.id = result.id
        return user

    def initialize_first_connexion(self, claims, user: User):
        user.picture = claims['picture']
        user.name = claims['name']
        user.firstConnexion = False
        self.db.collection(config.usersPath).document(user.id).delete()
        self.db.collection(config.usersPath).document(
            claims['uid']).set(user.to_dict(without_Id=True))
        return

    def delete_user_document(self, uid):
        result = self.db.collection(config.usersPath).document(uid).delete()
        return result

    def delete_user_account(self, uid):
        result = auth.delete_user(uid)
        return result

    def get_issues(self):
        result = self.db.collection(config.issuesPath).document().get()
        if result is None:
            return None
        return result
