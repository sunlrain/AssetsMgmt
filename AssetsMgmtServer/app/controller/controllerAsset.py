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
        # print type(assets)

        asset_summary = []

        for(k,v) in assets.items():
            found_in_summary=0
            for element in asset_summary:
                if (v["asset_name"] == element["name"]):
                    element["total_number"] = element["total_number"]+1
                    if(v["owner"] == "NULL"):
                        element["free_number"] = element["free_number"]+1
                    found_in_summary=1
                    break
            if found_in_summary == 0:
                asset_item = {"name":v["asset_name"],"total_number":1, "free_number":0, "info":""}
                asset_summary.append(asset_item)

        # print asset_summary

        for element in asset_summary:
            element["info"]=str(element["free_number"])+"/"+str(element["total_number"])
            del element["free_number"]
            del element["total_number"]

        print asset_summary

        return asset_summary







