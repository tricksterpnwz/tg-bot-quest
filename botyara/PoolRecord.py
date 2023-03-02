from GenderEnum import GenderEnum
from EducationEnum import EducationEnum
from FamilyStatusEnum import FamilyStatusEnum
from PoolStateEnum import PoolStateEnum


class PoolRecord:
    userId: int
    name: str
    zip: str
    gender: GenderEnum
    age: int
    education: EducationEnum
    employed: bool
    familyStatus: FamilyStatusEnum
    state: PoolStateEnum

    def __init__(self, user_id:int):
        self.userId = user_id
        self.name = None
        self.zip = None
        self.gender = None
        self.age = None
        self.education = None
        self.employed = None
        self.familyStatus = None
        self.state = PoolStateEnum.none



