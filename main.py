from auth import TG_KEY

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from SQL_Base import creat_base,add_record,get_records,get_record,del_record

bot = Bot(token=TG_KEY)
dp = Dispatcher(bot)

cd = CallbackData("fab", "action", "r_user_id")  # <= надо так
global times
times = " "

def get_keboard_card(r_id):
    buttons = [types.InlineKeyboardButton(text="Удалить запись", callback_data=cd.new(r_user_id=r_id, action="del")),
               types.InlineKeyboardButton(text="Подробнее", callback_data=cd.new(r_user_id=r_id, action="detailed")),
               ]
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard

def get_keyboard_add(message: types.Message):
    global times
    times = message.text
    buttons = [types.InlineKeyboardButton(text="Запись в базу",callback_data=cd.new(r_user_id=message.from_user.id, action="add")),
               ]
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_main():    
    button1 = KeyboardButton('/get')
    button2 = KeyboardButton('/help')              
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(button1).insert(button2) 
    return keyboard    


@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.reply("Для внесения записей набрать текст и отправит его.\n Для получения списка записей команда /get")


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет!", reply_markup=get_keyboard_main())


@dp.message_handler(commands=["get"])
async def get_records_bot(message: types.Message):
    result = get_records(message.from_user.id)
    if result:
        for r in result:
            await message.answer(f'''Дата:{r[2][:19]}\n {r[3][:30]}''',reply_markup=get_keboard_card(r[0]))
    else:
        await message.answer(f'''Записей нет''')

@dp.callback_query_handler(cd.filter(action=["del"]))
async def del_record_bot(call: types.CallbackQuery, callback_data: dict):
    del_record(callback_data["r_user_id"])
    await call.message.answer(f'Запись с ID {callback_data["r_user_id"]} удалена')


@dp.callback_query_handler(cd.filter(action=["add"]))
async def add_record_bot(call: types.CallbackQuery, callback_data: dict):
    add_record(callback_data["r_user_id"], times)
    await call.message.answer("Запись добавлена")

@dp.callback_query_handler(cd.filter(action=["detailed"]))
async def add_record_bot(call: types.CallbackQuery, callback_data: dict):
    result = get_record(callback_data["r_user_id"])
    await call.message.answer(f'''Дата:{result[2][:19]}\nТекст: {result[3]}''',reply_markup=get_keboard_card(result[0]))
    
    
@dp.message_handler()
async def echo_message(message: types.Message):
    await message.answer(message.text, reply_markup = get_keyboard_add(message))


if __name__ == "__main__":
    print("create base DB")
    creat_base()
    print("start Polling")
    executor.start_polling(dp)
