from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.filters.state import StatesGroup, State

from data.config import ADMINS
from keyboards.default.Barchasi import admin_only, admin_menu
from loader import dp, bot


class Reklama_State(StatesGroup):
    text_1 = State()
    text = State()


@dp.message_handler(lambda message: message.text == '//reklama' and str(message.from_user.id) in ADMINS)
async def bot2342dsfsdrt(message: types.Message, state: FSMContext):
    await message.answer(f"Text yuboring", reply_markup=admin_only)
    await Reklama_State.text_1.set()


@dp.message_handler(state=Reklama_State.text_1)
async def bot2342_start(message: types.Message, state: FSMContext):
    msg = message.text
    await state.update_data(
        {"msg": msg}
    )

    await message.answer(f"Rasm yuboring")
    await Reklama_State.text.set()


@dp.message_handler(content_types=["photo"], state=Reklama_State.text)
async def bot_text(message: types.Message, state: FSMContext):
    document_id = message.photo[0].file_id
    file_info = await bot.get_file(document_id)
    data = await state.get_data()
    msg = data.get("msg")
    f = open("./data/reklama.txt", "r")
    text = f.read()
    idd = ""
    for i in range(len(text)):
        try:
            if not text[i] == f"\n":
                idd += text[i]
            else:
                await bot.send_photo(chat_id=int(idd), photo=file_info.file_id, caption=msg, reply_markup=admin_menu)
                idd = ""
        except:
            idd = ""
    await state.finish()


@dp.message_handler(lambda message: message.text == '//count' and str(message.from_user.id) in ADMINS)
async def bot22_start(message: types.Message):
    f = open("./data/reklama.txt", "r")
    text = f.read()
    sum = 0
    for i in range(len(text)):
        if text[i] == f"\n":
            sum = sum + 1
    await message.answer(f"{sum}")
