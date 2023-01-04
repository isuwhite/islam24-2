from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types, Dispatcher
from config import bot, dp
from keyboards.client_kb import start_markup
from database.bot_db import sql_command_random
from parser.anime import ParserAnime


# @dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Салалекум {message.from_user.first_name}",
                           reply_markup=start_markup)
    # await message.answer("This in an answer method")
    # await message.reply("This in a reply method")


async def help_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"/start - Запуск\n"
                                f"/help - Помошь\n"
                                f"/quiz - Викторина")


# @dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT 1", callback_data="button_call_1")
    markup.add(button_call_1)

    question = "Чему равняется число ПИ"
    answers = [
        "2.34",
        "3.13",
        "4.13",
        "1.14",
        "3.14",
    ]

    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=4,
        explanation="Иди учись",
        open_period=5,
        reply_markup=markup
    )


async def get_random_user(message: types.Message):
    await sql_command_random(message)


async def get_anime(message: types.Message):
    anime = ParserAnime.parser()
    for i in anime:
        await message.answer(
            f"{i['link']}\n\n"
            f"{i['title']}\n"
            f"{i['status']}\n"
            f"#Y{i['date']}\n"
            f"#{i['country']}\n"
            f"#{i['genre']}\n"
        )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(help_handler, commands=['help'])
    dp.register_message_handler(get_random_user, commands=['get'])
    dp.register_message_handler(get_anime, commands=['anime'])