from flask import Blueprint, request, jsonify, make_response


import datetime
import json
import logging

from app.services.stackexchange import StackOverFlow


posts = Blueprint('posts', __name__)
stackoverflow = StackOverFlow()


@posts.route('/related', methods=['POST'])
def get():
    data = request.get_json()
    filtered_results = []
    if data is None:
        return {}
    if 'titles' in data and type(data['titles']) == list:
        titles = data['titles']
        results = stackoverflow.get_posts(titles)
        if results == {}:
            make_response(jsonify({"posts": []}), 200)
        filtered_results = stackoverflow.map_posts(results, titles)
        resp = make_response(jsonify({"posts": filtered_results}), 200)
        return resp
    else:
        return make_response(jsonify({"posts": filtered_results}), 200)
