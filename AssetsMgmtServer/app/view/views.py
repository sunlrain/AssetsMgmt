from app import app
from flask import render_template,request, jsonify
from datetime import datetime
import time

from json import *

# from sqlalchemy import create_engine, MetaData
from app.db.db import *


@app.route('/')
def index():
    return jsonify(status="success")


@app.route('/add_user', methods=['POST',])
def add_user():
    json_data = request.json
    ret = add("user",json_data)
    return ret


@app.route('/get_user')
def get_user_all():
    ret = get("user")
    return ret

@app.route('/add_ont', methods=['POST',])
def add_ont():
    json_data = request.json
    ret = add("ont",json_data)
    return ret


@app.route('/get_ont')
def get_ont_all():
    ret = get("ont")
    return ret



@app.route('/testConn')
def testConn():
    db = AssetsMgmtDB(host="106.187.46.80",port=27017)

    db.test_connection()

    return jsonify(status="success ")


def add(collection_name, data):
    json_data = request.json

    db = AssetsMgmtDB(host="106.187.46.80",port=27017)
    data = db.add_data_to_collection(collection_name, json_data)

    if data is not 0:
        print data
        del data["_id"]
        return jsonify(data)
    else:
        return jsonify(status="success ")


def get(collection_name):
    db = AssetsMgmtDB(host="106.187.46.80",port=27017)
    data = db.get_collection(collection_name)

    if data is -1:
        print "Get collection fail:"+str(collection_name)
        return jsonify(status="fail")
    #
    # print type(data)
    # print data
    # return jsonify(data)
    return JSONEncoder().encode(data)
