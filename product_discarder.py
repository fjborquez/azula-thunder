from database import get_current_status, change_active_transition, create_transition
from enums.observations import ObservationsEnum
from enums.status import StatusEnum


def discarder(inventory):
    for item in inventory:
        if not product_status_exist(item):
            continue

        current_status = get_current_status(item)

        if no_apply_status(current_status):
            continue

        observation = get_observation(current_status)
        change_active_transition(item, False)
        create_transition(item, StatusEnum.DISCARDED, True, observation)

def product_status_exist(detail):
    return not detail['product_status'] is None

def no_apply_status(status):
    return (status['id'] == StatusEnum.EXPIRED
            or status['id'] == StatusEnum.CONSUMED)

def status_is_expired(status):
    return status['id'] == StatusEnum.EXPIRED

def get_observation(status):
    if status_is_expired(status):
        return ObservationsEnum.PRODUCT_DISCARED_BECAUSE_EXPIRED_PRODUCT
    else:
        return ObservationsEnum.PRODUCT_DISCARED_BECAUSE_OF_USER_ACTION