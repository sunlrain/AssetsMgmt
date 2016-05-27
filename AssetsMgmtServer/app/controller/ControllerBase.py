from app.db.db import *

DBHOST="106.187.46.80"
DBPORT=27017

class ControllerBase(object):

    def __init__(self):
        self.db = AssetsMgmtDB(host=DBHOST,port=DBPORT)

    # Format of entry data is exact the same as the data model
    # Return 0 if success
    def add_entry_to_collection(self, collection_name, entry_data):
        ret = {"Status": ""}
        data = self.db.add_entry_to_collection(collection_name, entry_data)

        if data == 0:
            ret["Status"] = "Success"
        elif data == -1:
            ret["Status"] = "Error: Can not connect database"
        elif data == -2:
            ret["Status"] = "Error: Found existing record"
        elif data == -3:
            ret["Status"] = "Error: Parameter mismatch"
        else:
            ret["Status"] = "Error: Unknown error"

        return ret

    def get_collection_entries(self, collection_name):
        data = self.db.get_collection(collection_name)
        if data is -1:
            print "Get_collection_entries fail"+str(collection_name)
        return data

    # Format of entry data is exact the same as the data model, primary key is required
    # Return entry if success, -1 if fail or can't found
    def get_entry_from_collection(self, collection_name, entry_data):
        data = self.db.get_entry_from_collection(collection_name, entry_data)
        return data

    def edit_entry_to_collection(self, collection_name, data):
        return

    def delete_entry_from_collection(self, collection_name, data):
        return