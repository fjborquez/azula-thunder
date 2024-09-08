from database import create_transition
from enums.observations import Observations
from enums.status import Status


def handle(details):
    if details is None:
        return

    if not details:
        return

    if isinstance(details, dict):
        details = [details]
    for detail in details:
        if detail.get('status') is None:
            if detail.get('expíration_date') is None:
                new_product(detail, Status.FRESH)
                return

def new_product(detail, status):
    is_active: bool = True
    create_transition(detail, status, is_active, Observations.FIRST_DEFINED_STATUS_BY_USER_ACTION)