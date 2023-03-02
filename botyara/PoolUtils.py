from PoolStateEnum import PoolStateEnum
from PoolRecord import PoolRecord

pool = {} # user_id : PoolRecord

help = {
    PoolStateEnum.none : "Начните опрос с помощью команды /start",
    PoolStateEnum.init : "Ответите на вопросы?",
    PoolStateEnum.name : "Ваше имя:",
    PoolStateEnum.zip : "Ваш индекс:",
    PoolStateEnum.gender : "Ваш пол:",
    PoolStateEnum.age : "Ваш возраст:",
    PoolStateEnum.education : "Ваше образование:",
    PoolStateEnum.employed : "Ваш статус работы:",
    PoolStateEnum.familyStatus: "Ваш семейный статус:",
    PoolStateEnum.end: "Спасибо. Опрос завершен."
}


def getPoolStateForUser(userId: int):
    if userId in pool:
        return pool[userId]
    record = PoolRecord(userId)
    pool[userId] = record
    return record


def getPoolStateHelp(poolState: PoolStateEnum):
    return help[poolState]
