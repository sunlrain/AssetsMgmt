CollectionModel = \
    {
        "user": {
            "primaryKey": "name",
            "fields":
                {
                    "name": "",
                    "password": "",
                    "email": "",
                    "full_name": "",
                    "add_time": "",
                    "status": "",
                    "note": ""
                }
        },
        "asset": {
            "primaryKey": "premises_label",
            "fields":
                {
                    "premises_label": "",
                    "asset_name": "",
                    "serial_number": "",
                    "fsan": "",
                    "mac_address": "",
                    "owner": "",
                    "add_time": "",
                    "status": "",
                    "note": ""
                }
        }
    }

# Note: model, fsan, mac_address are only used for ONT
