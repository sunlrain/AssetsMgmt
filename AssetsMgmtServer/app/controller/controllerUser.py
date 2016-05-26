from app import app
from datetime import datetime
import time

# from json import *

from ControllerBase import *


COLLECTIONNAME="user"


class ControllerUser(ControllerBase):

    def add_user_to_collection(self, entry_data):
        # Add user entry to user collection
        ret = self.add_entry_to_collection(COLLECTIONNAME, entry_data)
        return ret

    def get_user_from_collection(self):
        # Get lists from user collection
        print "get_user_from_collection 1"
        ret = self.get_collection_entries(COLLECTIONNAME)
        print "get_user_from_collection 2"
        return ret

    def get_user_summary(self):
        # Get user Summary
        users = self.get_collection_entries(COLLECTIONNAME)

        numbers_of_user = len(users)
        print numbers_of_user
        # Get Assets Summary
        # assets = get_collection("asset")
        user_summary = {"name":"user","info":"0"}
        user_summary["info"] = numbers_of_user

        return user_summary







