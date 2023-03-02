from enum import Enum


class FamilyStatusEnum(str, Enum):
    single = "s"
    married = "m"
    divorced = "d"