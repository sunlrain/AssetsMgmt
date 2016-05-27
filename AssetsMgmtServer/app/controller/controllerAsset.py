from app import app
from datetime import datetime
import time

# from json import *


from ControllerBase import *

COLLECTIONNAME="asset"


class ControllerAsset(ControllerBase):
    def add_asset_to_collection(self, entry_data):
        # Add user entry to user collection
        ret = self.add_entry_to_collection(COLLECTIONNAME, entry_data)
        return ret

    def get_asset_from_collection(self):
        # Get lists from asset collection
        ret = self.get_collection_entries(COLLECTIONNAME)
        return ret

    def get_asset_summary(self):
        # Get Assets Summary
        assets = self.get_collection_entries("asset")



        print type(assets)

        return







