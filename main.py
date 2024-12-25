import base64
import json

import functions_framework

from product_discarder import discarder
from product_status_updater import updater


@functions_framework.cloud_event
def update_product_status(cloud_event):
    event_data = base64.b64decode(cloud_event.data['message']['data'])
    event_data_json = json.loads(event_data)

    inventory = event_data_json['inventory']
    process_action = event_data_json['process_action']

    if inventory is None:
        return

    updater(inventory, process_action)

@functions_framework.cloud_event
def discard_product_status(cloud_event):
    event_data = base64.b64decode(cloud_event.data['message']['data'])
    event_data_json = json.loads(event_data)

    inventory = event_data_json['inventory']

    if inventory is None:
        return

    discarder(inventory)

