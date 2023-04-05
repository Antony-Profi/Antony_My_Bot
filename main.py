import openai
from configuration import BOT_API, OPEN_AI_API
from aiogram import Bot, executor, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


bot = Bot(BOT_API)
dp = Dispatcher(bot)

openai.api_key = OPEN_AI_API
model_engine = 'text-davinci-003'

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
b_1 = KeyboardButton('/help')
b_2 = KeyboardButton('/img')
b_3 = KeyboardButton('/stickers')
b_4 = KeyboardButton('/location')
keyboard.add(b_1).insert(b_2).add(b_3).insert(b_4)

HELP_COMMAND = """
<b>/start</b> - <em>при вызове этой команде мы запускаем бота</em>
<b>/img</b> - <em>при вызове этой команде нам отправляют картинку</em>
<b>/stickers</b> - <em>при вызове этой команде нам отправляют стикер приветствия</em>
<b>/help</b> - <em>при вызове этой команде мы запрашиваем объяснения, при котором нам всё объяснят</em>
<b>/location</b> - <em>при вызове этой команде нам показывают гео-лакацию</em>
"""


async def start(_):
    print('Бот был успешно запущен!')


@dp.message_handler(commands=['start'])
async def start_sticker(message: types.Message):
    await message.answer('<em>Привет, <b>добро</b> пожаловать в наш бот!</em>',
                         parse_mode='HTML',
                         reply_markup=keyboard)
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=HELP_COMMAND,
                           parse_mode='HTML')
    await message.delete()


@dp.message_handler(commands=['img'])
async def send_image(message: types.Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo='https://wroom.ru/i/cars2/lincoln_navigator_4.jpg')
    await message.delete()


@dp.message_handler(commands=['location'])
async def sending_geolocation(message: types.Message):
    await bot.send_location(chat_id=message.from_user.id,
                            latitude=55,
                            longitude=74)
    await message.delete()


@dp.message_handler(commands=['stickers'])
async def start_sticker(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAEHzoxj8fyR8lzhy4y3wqF2AAGXXOTJlY0AAhwAA_cCyA9wHHItbZMYeC4E')
    await message.delete()


@dp.message_handler()
async def send_emoji(message: types.Message):
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=message.text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )
    response = completion.choices[0].text
    await message.reply(response + ' 😉')

executor.start_polling(dp, on_startup=start, skip_updates=True)
