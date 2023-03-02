from multiprocessing.pool import Pool
import json
import telebot
from PoolUtils import *
from GenderEnum import GenderEnum
from EducationEnum import EducationEnum
from FamilyStatusEnum import FamilyStatusEnum
bot = telebot.TeleBot('1246017447:AAF_Cu1V6MDp1XVkOBBXZ-eFKcvWSZGlyH0')
# имя - текст
# индекс - число
# пол - 3 кнопки (м/ж/н)
# возраст - число
# образование - 3 кнопки (начальное/среднее/высшее)
# статус работы - 2 кнопки (да/нет)
# семейное положение - 3 кнопки

def createButton(text:str, data:str):
    return telebot.types.InlineKeyboardButton(text=text, callback_data=data)

def writeCsv(userRecord: PoolRecord):
    # 1. определиться с названием файла(расширение обязательно .csv - userRecords.csv)
    # 2. Проверить есть ли файл
    #     есть - дописываем данные в конец
    #     нет  - записываем в файл заголовок и дописываем данные в конец
    # "user, name, zip, ...."
    pass

def processUserState(userRecord:PoolRecord, chatId: int):
    reply = getPoolStateHelp(userRecord.state)
    keyboard = telebot.types.InlineKeyboardMarkup()

    if userRecord.state == PoolStateEnum.init:
        keyboard.add(createButton("Да", "yes"), createButton("Нет", "no"))
        bot.send_message(chatId, reply, reply_markup=keyboard)
        return
    elif userRecord.state == PoolStateEnum.gender:
        keyboard.add(
            createButton("Ж", GenderEnum.Female.name),
            createButton("М", GenderEnum.Male.name),
            createButton("Не важно", GenderEnum.No.name),
            row_width = 3)
        bot.send_message(chatId, reply, reply_markup=keyboard)
        return
    elif userRecord.state == PoolStateEnum.education:
        keyboard.add(
            createButton("Начальное", EducationEnum.elementary.name),
            createButton("Среднее", EducationEnum.secondary.name),
            createButton("Высшее", EducationEnum.higher.name),
            row_width=3)
        bot.send_message(chatId, reply, reply_markup=keyboard)
        return
    elif userRecord.state == PoolStateEnum.employed:
        keyboard.add(
            createButton("Работаю", "True"),
            createButton("Безработный", "False"),
            row_width=2)
        bot.send_message(chatId, reply, reply_markup=keyboard)
        return
    elif userRecord.state == PoolStateEnum.familyStatus:
        keyboard.add(
            createButton("Холост(ая)", FamilyStatusEnum.single.name),
            createButton("Женат/Замужем", FamilyStatusEnum.married.name),
            createButton("Разведен(а)", FamilyStatusEnum.divorced.name),
            row_width=3)
        bot.send_message(chatId, reply, reply_markup=keyboard)
        return
    elif userRecord.state == PoolStateEnum.end:
        bot.send_message(chatId, reply, reply_markup=None)
        if userRecord.familyStatus != None:
            jsString = json.dumps(userRecord.__dict__)
            bot.send_message(chatId, "Введенная информация: {}".format(jsString))
            writeCsv(userRecord)
        return

    bot.send_message(chatId, reply)

def processUserTextReply(message, userRecord: PoolRecord):
    if userRecord.state == PoolStateEnum.name:
        if message.text.isnumeric(): # признак некорректного ввода
            bot.send_message(message.from_user.id, "Некорректное имя - {}.".format(message.text))
        else:
            userRecord.name = message.text
            userRecord.state = PoolStateEnum.zip
            bot.send_message(message.from_user.id, "Привет {}".format(userRecord.name))
    elif userRecord.state == PoolStateEnum.zip:
        if not message.text.isnumeric():
            bot.send_message(message.from_user.id, "Некорректное значение индекса - {}".format(message.text))
        else:
            userRecord.zip = message.text
            userRecord.state = PoolStateEnum.gender
            bot.send_message(message.from_user.id, "Индекс принял: {}".format(userRecord.zip))
    elif userRecord.state == PoolStateEnum.age:
        if not message.text.isnumeric():
            bot.send_message(message.from_user.id, "Некорректный возраст: {}".format(message.text))
        else:
            age = int(message.text)
            if age < 16:
                bot.send_message(message.from_user.id, "Извините. Опрос для 16+")
                # можем поменять текущее состояние на end
            elif age > 100:
                bot.send_message(message.from_user.id, "Многовато: {}".format(age))
            else:
                userRecord.age = age
                userRecord.state = PoolStateEnum.education
                bot.send_message(message.from_user.id, "Хороший возраст: {}".format(age))

    processUserState(userRecord, message.chat.id)


def processKeyboardReply(call, userRecord: PoolRecord):
    if userRecord.state == PoolStateEnum.init:
        if call.data == "no":
            userRecord.state = PoolStateEnum.none
        else:
            userRecord.state = PoolStateEnum.name
    elif userRecord.state == PoolStateEnum.gender:
        userRecord.gender = GenderEnum[call.data]
        userRecord.state = PoolStateEnum.age
    elif userRecord.state == PoolStateEnum.education:
        userRecord.education = EducationEnum[call.data]
        userRecord.state = PoolStateEnum.employed
    elif userRecord.state == PoolStateEnum.employed:
        userRecord.employed = bool(call.data)
        userRecord.state = PoolStateEnum.familyStatus
    elif userRecord.state == PoolStateEnum.familyStatus:
        userRecord.familyStatus = FamilyStatusEnum[call.data]
        userRecord.state = PoolStateEnum.end

    processUserState(userRecord, call.message.chat.id)

@bot.message_handler(commands=['start'])
def process_start_command(message):
    userRecord = getPoolStateForUser(message.from_user.id)
    if userRecord.state == PoolStateEnum.none:
        userRecord.state = PoolStateEnum.init
    processUserState(userRecord, message.chat.id)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    userRecord = getPoolStateForUser(message.from_user.id)
    processUserTextReply(message, userRecord)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    userRecord = getPoolStateForUser(call.from_user.id)
    processKeyboardReply(call, userRecord)

bot.polling(none_stop=True)



