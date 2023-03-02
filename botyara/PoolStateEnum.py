from enum import Enum


class PoolStateEnum(str, Enum):
    none = "non"
    init = "ini"
    name = "nam"
    zip = "zip"
    gender = "gen"
    age = "age"
    education = "edu"
    employed = "emp"
    familyStatus = "fam"
    end = "end"
