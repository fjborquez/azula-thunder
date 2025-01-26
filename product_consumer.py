from database import get_current_status, change_active_transition, create_transition
from enums.observations import ObservationsEnum
from enums.status import StatusEnum



def consumer(inventory):
    for item in inventory:
        if not product_status_exist(item):
            continue

        current_status = get_current_status(item)

        if no_apply_status(current_status):
            continue

        observation = get_observation(current_status)
        change_active_transition(item, False)
        create_transition(item, StatusEnum.CONSUMED, True, observation)

def product_status_exist(detail):
    return 'product_status' in detail and detail['product_status'] is not None

def no_apply_status(status):
    return (status['id'] == StatusEnum.EXPIRED or status['id'] == StatusEnum.CONSUMED
            or status['id'] == StatusEnum.DISCARDED)

def get_observation(status):
    if (status['id'] == StatusEnum.FRESH or status['id'] == StatusEnum.APPROACHING_EXPIRY
            or status['id'] == StatusEnum.UNDEFINED):
        return ObservationsEnum.CONSUMED_BY_USER
    raise ValueError("There are not any observation for the status")