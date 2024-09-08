import base64
import json

import functions_framework

from inventory_handler import handle


def extract_inventory(inventory) -> None:
    if inventory is None:
        return

    handle(inventory)

@functions_framework.cloud_event
def main(cloud_event):
    event_data = base64.b64decode(cloud_event.data['message']['data'])
    event_data_json = json.loads(event_data)
    extract_inventory(event_data_json['inventory'])