from aiogram import types

from loader import dp


@dp.message_handler(commands=['get_id'])
async def send_chat_id(message: types.Message):
    chat_id = message.chat.id
    await message.reply(f"Chat ID: {chat_id}")


@dp.channel_post_handler()
async def channel_post_handler(message: types.Message):
    if message.text == '/get_id_c':  # Xabarni tekshirish
        chat_id = message.chat.id
        await message.answer(f"Kanalning chat_id si: {chat_id}")
