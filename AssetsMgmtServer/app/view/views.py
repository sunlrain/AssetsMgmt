from app import app
from flask import render_template,request, jsonify
from datetime import datetime
import time

from json import *

from app.controller.controllerUser import *
from app.controller.controllerAsset import *


@app.route('/')
def index():
    return jsonify(status="success")


@app.route('/add_user', methods=['POST',])
def add_user():
    jsondata = request.json
    controller_user = ControllerUser()
    ret = controller_user.add_user_to_collection(jsondata)
    return jsonify(ret)


@app.route('/get_user')
def get_user_all():
    controller_user = ControllerUser()
    ret = controller_user.get_user_from_collection()
    return jsonify(ret)

@app.route('/get_user_summary')
def get_user_summary():
    controller_user = ControllerUser()
    user_summary = controller_user.get_user_summary()

    return jsonify(user_summary)

@app.route('/add_asset', methods=['POST',])
def add_asset():
    jsondata = request.json
    controller_asset = ControllerAsset()
    ret = controller_asset.add_asset_to_collection(jsondata)
    return jsonify(ret)


@app.route('/get_asset')
def get_asset():
    controller_asset = ControllerAsset()
    ret = controller_asset.get_asset_from_collection()
    return jsonify(ret)

@app.route('/get_asset_summary')
def get_asset_summary():
    controller_asset = ControllerAsset()
    ret = controller_asset.get_asset_summary()
    return jsonify(status="success")
