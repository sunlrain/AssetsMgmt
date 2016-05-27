import time
import os
from threading import RLock
import types

import pymongo
from CollectionModel import CollectionModel


class _AssetsMgmtDB(object):
    """Assets Management result/log database class. It is designed to be thread-safe.
    """

    state = "disconnect"

    # lock = RLock()
    def __init__(self, host="106.187.46.80", port=27017, logger=None):
        """constructor

        Args:
            db_uri (string): data url string. default ("sqlite:///my_sqlite.db")
            echo (bool): True - to turn on the sqlachemy debug log print; False otherwise
            logger (object): Cafe CLogger object

        Returns:
            None

        """
        self.state = "disconnect"
        self.db_host = host
        self.db_port = port

        try:
            self.db_conn = pymongo.MongoClient(host=host, port=port)
        except:
            return
        self.state = "connected"

    # Parameter:
    #     collection_name: the collection name
    #     data: the entry data in dict format
    # Return value:
    #     0: Add success
    #     -1: Can not connect data base
    #     -2: Found existing record
    #     -3: parameter incorrect
    def add_entry_to_collection(self, collection_name, data):
        print "Add entry to collection: "
        if self.state is "disconnect":
            return -1
        # check and see if test suite already exist gracefully
        id = self.get_entry_from_collection(collection_name, data)
        # print "id=",id
        if id > -1:
            print "Add_data_to_collection: find existing record"
            return -2

        if self.validate_data_with_collection(collection_name,data) != 0 :
            print "Add_data_to_collection: parameter incorrect"
            return -3


        db = self.db_conn.AssetsMgmt
        collection = db[collection_name]

        # print data
        # print type(data)
        # mydict = {"status": "Active", "name": "kliu", "full_name": "Kevin Liu", "password": "12345678", "email": "kevin.liu@calix.com", "add_time": "5/18/2016"}

        us = collection.insert(data)

        for post in collection.find():
            print post

        print us
        # print "_Create_User here 2"

        return 0

    def validate_collection_keys(self, model, data):
        ret = -1

        if type(model) is not types.DictionaryType:
            print "validate_collection_keys: Parameter type incorrect: model"
            return ret

        if type(data) is not types.DictionaryType:
            print "validate_collection_keys: Parameter type incorrect: data"
            return ret

        try:
            for key in data.keys():
                if (model.has_key(key)):
                    pass
                else:
                    return ret
            ret = 0
        except:
            pass
        finally:
            pass
        return ret

    # Return definition of collection
    def get_collection_definition(self, collection_name):
        ret = -1
        try:
            for(k,v) in CollectionModel.items():
                if (k == collection_name):
                    print "validate_data_with_collection: found collection"
                    ret = v
        except:
            pass
        finally:
            pass
        return ret

    def validate_data_with_collection(self, collection_name, data):
        ret = -1
        try:
            v = self.get_collection_definition(collection_name)
            if v is not -1:
                ret = self.validate_collection_keys(v["fields"], data)
        except:
            pass
        finally:
            pass
        return ret

    def get_entry_from_collection(self, collection_name, data):
        if type(data) is not types.DictionaryType:
            print "get_data_from_collection: Parameter type incorrect: data"
            return -1
        if self.state is "disconnect":
            return -1

        collection_definition = self.get_collection_definition(collection_name)
        print collection_definition
        if collection_definition is -1:
            print "get_data_from_collection: Can not find collection definition: " + collection_name
            return -1
        if (not collection_definition.has_key("primaryKey")):
            print "get_data_from_collection: definition has no primiary key "
            return -1
        if (not data.has_key(collection_definition["primaryKey"])):
            print "get_data_from_collection: data has no primary key info " + collection_definition["primaryKey"]
            return -1

        db = self.db_conn.AssetsMgmt
        collection = db[collection_name]

        # print collection_definition["primaryKey"]
        # print data[collection_definition["primaryKey"]]
        us = collection.find_one({collection_definition["primaryKey"]:data[collection_definition["primaryKey"]]})

        if us is None:
            return -1
        else:
            return us


    # Get all data from collection
    def get_collection(self, collection_name):
        if self.state is "disconnect":
            return -1

        collection_definition = self.get_collection_definition(collection_name)
        if collection_definition is -1:
            print "get_data_from_collection: Can not find collection definition: " + collection_name
            return -1

        db = self.db_conn.AssetsMgmt
        collection = db[collection_name]

        # us = collection.find_one()
        i = 0

        colls = {}

        for item in collection.find():
            del item["_id"]
            colls["col"+str(i)] = item
            i = i + 1

        # print colls
        return colls

    def test_connection(self):
        print "test_connection"
        # print self.db_conn.collection_names()

AssetsMgmtDB = _AssetsMgmtDB