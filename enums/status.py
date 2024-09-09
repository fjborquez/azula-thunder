from enum import Enum


class StatusEnum(Enum):
    FRESH = 1
    APPROACHING_EXPIRY = 2
    EXPIRED = 3
    CONSUMED = 4
    DISCARDED = 5
    UNDEFINED = 6