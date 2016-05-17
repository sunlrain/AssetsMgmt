from app import app
from flask import render_template,request, jsonify
from datetime import datetime
import time

# from sqlalchemy import create_engine, MetaData
from app.db.db import *

@app.route('/')
def index():
    return jsonify(status="success")


@app.route('/adduser', methods=['POST',])
def addUser():
    jsondata = request.json

    print type(jsondata)
    print jsondata['name']
    print jsondata["full_name"]
    print jsondata["email"]
    print jsondata["password"]

    db = AssetsMgmtDB()
    print db
    uid = db._create_user(name=jsondata["name"], full_name=jsondata["full_name"],email=jsondata["email"],password=jsondata["password"],add_time=time.localtime())
    print uid


    return jsonify(status="success ")

@app.route('/getUser')
def getUser():
    # jsondata = request.json
    #
    # for(k,v) in jsondata.items():
    #     if (k == "addUser"):
    #         db = AssetsMgmtDB()
    #         uid = db._create_user(name=v["name"], full_name=v["full_name"],email=v["email"], password=v["password"])
    #         print uid
    #     else:
    #         print "Not support type:",k
    #         return jsonify(status="Fail: not support type")

    return jsonify(status="success")



@app.route('/delete/<string:todo_id>')
def delete(todo_id):
    return jsonify(status="success")


@app.route('/update', methods=['POST',])
def update():
    print "here"
    return jsonify(status="success")

