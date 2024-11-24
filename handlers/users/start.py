from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatMemberStatus, ReplyKeyboardRemove

from data.config import ADMINS, channel_1, channel_2, channel_3
from keyboards.inline.barchasi import obuna_inline
from loader import dp, bot
from utils.db_api.films_sql import Database_Film

db = Database_Film()


# async def check_membership(user_id: int) -> bool:
#     member = await bot.get_chat_member(GROUP_ID, user_id)
#     return member.status != ChatMemberStatus.LEFT and member.status != ChatMemberStatus.BANNED

async def check_membership(user_id: int) -> bool:
    group_ids = [channel_1, channel_2, channel_3]  # List of group IDs
    for group_id in group_ids:
        member = await bot.get_chat_member(group_id, user_id)
        if member.status == ChatMemberStatus.LEFT or member.status == ChatMemberStatus.BANNED:
            return False
    return True


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    f = open("./data/reklama.txt", "r")
    text = f.read()
    if not str(user_id) in text:
        f = open("./data/reklama.txt", "a")
        f.write(f"{user_id}\n")
        f.close()
    await message.answer(f"👋 Assalomu alaykum {message.from_user.full_name}. Botimizga xush kelibsiz!\n\n"
                         f"*✍️ Kino kodini yuboring:*", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text.isdigit())
async def dvxcvxfs(message: types.Message):
    number = str(message.text)
    is_member = await check_membership(message.from_user.id)
    film = []
    if is_member:
        try:
            await db.create()
            film = await db.select_film(film_number=str(number))
            await db.disconnect()
        except:
            await bot.send_message(chat_id=ADMINS[0], text=f'Xato start.py 40-page')
        if not film is None:
            await message.answer_video(video=film[2], caption=f"🍿 | Nomi: {film[3]}\n"
                                                              f"🇺🇿 | Tili: {film[4]}\n"
                                                              f"🗂 | Hajmi: {film[5]}\n"
                                                              f"🎞 | Sifati: {film[6]}\n"
                                                              f"🎭 | Janri:  {film[7]}\n"
                                                              f"👀 | Ko’rish katigoriyasi: {film[8]}\n"
                                                              f"⏳ | Davomiyligi: {film[9]}\n"
                                                              f"➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                                              f"🤖 | Bizning bot: @KINOKOM_BOT\n")

        else:
            await message.answer(f"Siz yuborgan raqamga tegishli kino topilmadi\n"
                                 f"Iltimos tekshirib qaytadan yuboring")
    else:
        await message.answer(f"Siz tanlagan kino ko'rish uchun quyidagi barcha kanallarga a'zo bo'ling:",
                             reply_markup=obuna_inline)


@dp.callback_query_handler(text_contains='tasdiklash')
async def handle_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    is_member = await check_membership(user_id)
    if is_member:
        await call.message.delete()
        await call.message.answer(f"Obuna bo'lgansiz\n"
                                  f"👋 Assalomu alaykum {call.from_user.full_name}. Botimizga xush kelibsiz!\n\n"
                                  f"*✍️ Kino kodini yuboring:*")
    else:
        await call.message.answer(f"Siz hali barcha kanallarimizga a'zo bo'lmadingiz")
