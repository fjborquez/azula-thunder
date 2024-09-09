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
        if detail.get('quantity') <= 0:
            observation: ObservationsEnum

            if process_action == ProcessActionsEnum.SYSTEM_PROCESS:
                observation = ObservationsEnum.QUANTITY_IS_ZERO_BY_SYSTEM_PROCESS
            else:
                observation = ObservationsEnum.QUANTITY_IS_ZERO_BY_USER_ACTION

            add_status(detail, StatusEnum.CONSUMED, observation)
            return

        if detail.get('status') is None:
            if detail.get('expiration_date') is None:
                add_status(detail, StatusEnum.UNDEFINED, ObservationsEnum.NO_EXPIRATION_DATE_BY_USER_ACTION)
                return

def add_status(detail, status: StatusEnum, observation: ObservationsEnum):
    is_active: bool = True
    change_active_transition(detail, not is_active)
    create_transition(detail, status, is_active, observation)