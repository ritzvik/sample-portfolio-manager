from enum import Enum


class SchemeTypes(Enum):
    HIGH_RISK = "HIGH_RISK"
    RETIREMENT = "RETIREMENT"


class DepositTypes(Enum):
    LUMPSUM = "LUMPSUM"
    RECURRING = "RECURRING"
