import logging
import asyncio
import sys
from openai import OpenAI
from aiogram import *
from aiogram.types import *
from aiogram.enums import ParseMode
from aiogram.filters import *
from aiogram.fsm.context import FSMContext
from aiohttp import BasicAuth
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import Filter
from config import Kanal_id
from config import TOKEN, API_KEY
from bottons import Menyu

auth=BasicAuth(login='login', password='password')
session=AiohttpSession(proxy=('http://proxy.server:3128',auth))
bot = Bot(token=TOKEN)
bot.default_parse_mode = ParseMode.HTML
router=Router()

client=OpenAI(api_key=API_KEY)

Admin = 6207650392

dp=Dispatcher()
@router.message(Command("start"))
async def start_get(message: Message):
    ism = message.from_user.first_name
    lastname = message.from_user.last_name
    user_id= message.from_user.id
    nom = message.from_user.username
    number=+998
    from users import USERS
    USERS(user_id, ism, lastname, number)
    await bot.send_message(Admin, f"Botga yangi foydalanuvchi qo'shildi!\nFoydalanuvchi - {ism}\nID raqami - {user_id}") 
    await bot.send_message(user_id, f"Assalomu alaykum! {ism or nom} ", parse_mode=ParseMode.HTML)

@router.message(Command('clear'))
async def clear(message: Message, state: FSMContext):
    await message.answer('Yangi chat ochildi')
    await state.update_data({'user_messages': []})
    await state.update_data({'context': ''})

@router.callback_query(F.data=="azolik")
async def azolik(callback_query: CallbackQuery):
    pass


@router.message(F.text)
async def message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    user_messages = data.get('user_messages')
    context = data.get('context')

    s = message.text
    try:
        user_messages.append(s)
    except AttributeError:
        await state.update_data({'user_messages': []})
        await state.update_data({'context': ''})
        data = await state.get_data()
        user_messages = data.get('user_messages')
        context = data.get('context')
        user_messages.append(s)

    stream = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {'role': 'system', 'content': context},
            {'role': 'user', 'content': s}
            ],
        stream = True
        )

    result=''
    for chunk in stream:
        if not chunk.choices[0].delta.content == None:
            result += chunk.choices[0].delta.content
    await message.answer(result)

    context = '\n'.join([f"User: {i}" for i in user_messages])
    await state.update_data({'user_messages': user_messages})
    await state.update_data({'context': context})






async def main():
    dp = Dispatcher()
    dp.include_router(router = router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
