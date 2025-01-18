from datetime import datetime

from database import create_transition, change_active_transition
from enums.process_actions import ProcessActionsEnum
from enums.observations import ObservationsEnum
from enums.status import StatusEnum


def updater(details, process_action: int):
    if not details:
        return

    details = details if isinstance(details, list) else [details]

    for detail in details:
        if is_detail_in_final_phase_status(detail):
            continue

        if has_zero_or_less_quantity(detail):
            observation = determine_zero_quantity_observation(process_action)
            add_status(detail, StatusEnum.CONSUMED, observation)
            continue

        if should_skip_due_to_expiry(detail, process_action):
            continue

        update_status_for_detail(detail, process_action)

def is_detail_in_final_phase_status(detail) -> bool:
    product_status = detail.get('product_status')
    return product_status.get('is_final_phase') == True

def has_zero_or_less_quantity(detail) -> bool:
    quantity = detail.get('quantity')
    return quantity is not None and float(quantity) <= 0

def determine_zero_quantity_observation(process_action: int) -> ObservationsEnum:
    if process_action == ProcessActionsEnum.USER_ACTION.value:
        return ObservationsEnum.QUANTITY_IS_ZERO_BY_USER_ACTION
    else:
        return ObservationsEnum.QUANTITY_IS_ZERO_BY_SYSTEM_PROCESS

def should_skip_due_to_expiry(detail, process_action: int) -> bool:
    expiration_date = detail.get('expiration_date')
    return expiration_date and is_expired(expiration_date) and process_action == ProcessActionsEnum.USER_ACTION.value

def is_expired(expiration_date: str) -> bool:
    delta = datetime.strptime(expiration_date, "%Y-%m-%d").date() - datetime.now().date()
    return delta.days <= 0

def update_status_for_detail(detail, process_action: int):
    if detail.get('product_status') is None:
        handle_no_status(detail, process_action)
    else:
        handle_with_status(detail, process_action)

def handle_no_status(detail, process_action: int):
    if detail.get('expiration_date') is None:
        if process_action == ProcessActionsEnum.USER_ACTION.value:
            observation = ObservationsEnum.NO_EXPIRATION_DATE_BY_USER_ACTION
        else:
            observation = ObservationsEnum.NO_STATUS_AND_NO_EXPIRATION_DATE_BY_SYSTEM_PROCESS
        add_status(detail, StatusEnum.UNDEFINED, observation)
    else:
        status = get_status(detail)
        if process_action == ProcessActionsEnum.USER_ACTION.value:
            observation = ObservationsEnum.FIRST_STATUS
        else:
            observation = ObservationsEnum.NO_STATUS_BY_SYSTEM_PROCESS
        add_status(detail, status, observation)

def handle_with_status(detail, process_action: int):
    if detail.get('expiration_date'):
        status = get_status(detail)
        if process_action == ProcessActionsEnum.USER_ACTION.value:
            observation = ObservationsEnum.STATUS_UPDATED_BY_USER_ACTION
        else:
            observation = ObservationsEnum.STATUS_UPDATED_BY_SYSTEM_PROCESS
        add_status(detail, status, observation)
    else:
        if process_action == ProcessActionsEnum.USER_ACTION.value:
            observation = ObservationsEnum.STATUS_UPDATED_BY_USER_ACTION
        else:
            observation = ObservationsEnum.NO_STATUS_AND_NO_EXPIRATION_DATE_BY_SYSTEM_PROCESS
        add_status(detail, StatusEnum.UNDEFINED, observation)

def add_status(detail, status: StatusEnum, observation: ObservationsEnum):
    for old_status in detail.get('product_status', []):
        pivot = old_status.get('pivot')
        if pivot.get('is_active') and status.value == old_status.get('id'):
            return

    is_active = True
    change_active_transition(detail, False)
    create_transition(detail, status, is_active, observation)


def get_status(detail) -> StatusEnum:
    expiration_date = datetime.strptime(detail.get('expiration_date'), "%Y-%m-%d").date()
    delta = expiration_date - datetime.now().date()

    if delta.days > 7:
        return StatusEnum.FRESH
    elif 7 >= delta.days > 0:
        return StatusEnum.APPROACHING_EXPIRY
    else:
        return StatusEnum.EXPIRED