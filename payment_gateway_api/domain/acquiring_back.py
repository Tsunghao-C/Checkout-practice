from enum import Enum


class AcquiringBankStatus(Enum):
    """
    Response status from acquiring bank
    """
    AUTHORIZED = "Authorized"
    DECLINED = "Declined"
