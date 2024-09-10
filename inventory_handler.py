from datetime import datetime

from database import create_transition, change_active_transition
from enums.process_actions import ProcessActionsEnum
from enums.observations import ObservationsEnum
from enums.status import StatusEnum


def handle(details, process_action: int):
    if details is None:
        return

    if not details:
        return

    if isinstance(details, dict):
        details = [details]

    for detail in details:
        if detail.get('quantity') is not None and float(detail.get('quantity')) <= 0:
            observation: ObservationsEnum

            if process_action == ProcessActionsEnum.SYSTEM_PROCESS:
                observation = ObservationsEnum.QUANTITY_IS_ZERO_BY_SYSTEM_PROCESS
            else:
                observation = ObservationsEnum.QUANTITY_IS_ZERO_BY_USER_ACTION

            add_status(detail, StatusEnum.CONSUMED, observation)
            return

        if detail.get('expiration_date') is not None:
            delta = datetime.strptime(detail.get('expiration_date'), "%Y-%m-%d").date() - datetime.now().date()
            if delta.days <= 0 and process_action == ProcessActionsEnum.USER_ACTION.value:
                continue

        if detail.get('status') is None:
            if detail.get('expiration_date') is None:
                add_status(detail, StatusEnum.UNDEFINED, ObservationsEnum.NO_EXPIRATION_DATE_BY_USER_ACTION)
                return
            else:
                status, observation = get_status(detail)
                add_status(detail, status, ObservationsEnum.NO_STATUS_BY_USER_ACTION)
                return
        else:
            if detail.get('expiration_date'):
                status, observation = get_status(detail)
                add_status(detail, status, observation)
                return
            else:
                add_status(detail, StatusEnum.UNDEFINED, ObservationsEnum.NO_EXPIRATION_DATE_BY_SYSTEM_PROCESS)
                return

def add_status(detail, status: StatusEnum, observation: ObservationsEnum):
    is_active: bool = True
    change_active_transition(detail, not is_active)
    create_transition(detail, status, is_active, observation)

def get_status(detail):
    today = datetime.now().date()
    expiration_date = datetime.strptime(detail.get('expiration_date'), "%Y-%m-%d").date()
    delta = expiration_date - today

    if delta.days > 7:
        return StatusEnum.FRESH, ObservationsEnum.FIRST_DEFINED_STATUS_BY_USER_ACTION
    elif 7 >= delta.days > 0:
        return StatusEnum.APPROACHING_EXPIRY, ObservationsEnum.FIRST_DEFINED_STATUS_BY_USER_ACTION
    else:
        return StatusEnum.EXPIRED