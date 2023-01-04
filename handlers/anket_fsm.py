from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.bot_db import sql_command_insert
from keyboards import client_kb

# SQL - Structured Query Language
# СУБД - Систему Управления Базой Данных


class FSMAdmin(StatesGroup):
    name = State()
    age = State()
    gender = State()
    region = State()
    photo = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.chat.type == "private":
        await FSMAdmin.name.set()
        await message.answer("Как звать?", reply_markup=client_kb.cancel_markup)
    else:
        await message.answer("Пиши в личку!")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["id"] = message.from_user.id
        data["username"] = f"@{message.from_user.username}"
        data["name"] = message.text
    await FSMAdmin.next()
    await message.answer("Скока лет?")


async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пиши числа!")
    elif int(message.text) < 16 or int(message.text) > 50:
        await message.answer("Возрастное ограничение!")
    else:
        async with state.proxy() as data:
            data["age"] = message.text
        await FSMAdmin.next()
        await message.answer("Какого пола?", reply_markup=client_kb.gender_markup)


async def load_gender(message: types.Message, state: FSMContext):
    if message.text not in ["Мужчина", "Женщина", "Незнаю"]:
        await message.answer("Такого варианта нет!")
    else:
        async with state.proxy() as data:
            data["gender"] = message.text
        await FSMAdmin.next()
        await message.answer("Откуда будишь???", reply_markup=client_kb.cancel_markup)


async def load_region(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["region"] = message.text
    await FSMAdmin.next()
    await message.answer("Скинь фотку)")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id
        await message.answer_photo(data['photo'],
                                   caption=f"{data['name']} {data['age']} {data['gender']} "
                                   f"{data['region']}\n{data['username']}")
    await FSMAdmin.next()
    await message.answer("Все верно?", reply_markup=client_kb.submit_markup)


async def submit_fsm(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await sql_command_insert(state)
        await state.finish()
        await message.answer('Все свободен!')
    elif message.text.lower() == "нет":
        await state.finish()
        await message.answer("Отменено!")
    else:
        await message.answer("НИПОНЯЛ!?")


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer("Отменено!")


def register_handlers_fsm_anketa(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, state='*', commands=['cancel'])
    dp.register_message_handler(cancel_fsm, Text(equals='cancel', ignore_case=True), state='*')

    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_gender, state=FSMAdmin.gender)
    dp.register_message_handler(load_region, state=FSMAdmin.region)
    dp.register_message_handler(load_photo, state=FSMAdmin.photo, content_types=['photo'])
    dp.register_message_handler(submit_fsm, state=FSMAdmin.submit)