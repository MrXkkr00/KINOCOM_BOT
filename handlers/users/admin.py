from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove

from data.config import ADMINS
from handlers.users.rek import Reklama_State
from keyboards.default.Barchasi import admin_menu, admin_only
from loader import dp, bot
from utils.db_api.films_sql import Database_Film

db = Database_Film()


#     KeyboardButton(text="Kino yuklash"),
#     KeyboardButton(text="Kino yangilash")


class Kino_Yuklash_State(StatesGroup):
    film_cod = State()  # 1
    film_number = State()  # 2
    name = State()  # 3
    tili = State()  # 4
    hajmi = State()  # 5
    sifati = State()  # 6
    janri = State()  # 7
    korish_yoshi = State()  # 8
    davomiyligi = State()  # 9


@dp.message_handler(text='//data')
async def asfdsfr(message: types.Message):
    await db.create()
    await db.create_table_films()
    await db.disconnect()


@dp.message_handler(lambda message: message.text == '/admin' and str(message.from_user.id) in ADMINS)
async def admin_handler(message: types.Message):
    await message.answer("Admin bo'limga kirdingiz", reply_markup=admin_menu)


@dp.message_handler(text='/admin', state=[Kino_Yuklash_State.film_cod, Kino_Yuklash_State.film_number,
                                          Kino_Yuklash_State.name, Kino_Yuklash_State.tili,
                                          Kino_Yuklash_State.hajmi, Kino_Yuklash_State.sifati,
                                          Kino_Yuklash_State.janri, Kino_Yuklash_State.korish_yoshi,
                                          Kino_Yuklash_State.davomiyligi])
async def admin_handler_2(message: types.Message, state: FSMContext):
    await message.answer("Admin bo'limga kirdingiz", reply_markup=admin_menu)
    await state.finish()


@dp.message_handler(text='/start', state=[Kino_Yuklash_State.film_cod, Kino_Yuklash_State.film_number,
                                          Kino_Yuklash_State.name, Kino_Yuklash_State.tili,
                                          Kino_Yuklash_State.hajmi, Kino_Yuklash_State.sifati,
                                          Kino_Yuklash_State.janri, Kino_Yuklash_State.korish_yoshi,
                                          Kino_Yuklash_State.davomiyligi])
async def admin_handler_2(message: types.Message, state: FSMContext):
    await message.answer(f"👋 Assalomu alaykum {message.from_user.full_name}. Botimizga xush kelibsiz!\n\n"
                         f"*✍️ Kino kodini yuboring:*", reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(text='/admin', state=[Reklama_State.text_1, Reklama_State.text])
async def admin_handler_3(message: types.Message, state: FSMContext):
    await message.answer("Admin bo'limga kirdingiz", reply_markup=admin_menu)
    await state.finish()


@dp.message_handler(text='/start', state=[Reklama_State.text_1, Reklama_State.text])
async def admin_handler_3(message: types.Message, state: FSMContext):
    await message.answer(f"👋 Assalomu alaykum {message.from_user.full_name}. Botimizga xush kelibsiz!\n\n"
                         f"*✍️ Kino kodini yuboring:*", reply_markup=ReplyKeyboardRemove())
    await state.finish()


# 1
@dp.message_handler(lambda message: message.text == 'Kino yuklash' and str(message.from_user.id) in ADMINS)
async def asafsler(message: types.Message):
    await message.answer(f'Kino yuklang', reply_markup=admin_only)
    await Kino_Yuklash_State.film_cod.set()


# 1
@dp.message_handler(content_types=['video'], state=Kino_Yuklash_State.film_cod)
async def psfsd(message: types.Message, state: FSMContext):
    video_id = message.video.file_id
    await state.update_data({"video_id": str(video_id)})
    await message.answer(f'Kino radamini yuboring\nFaqat raqam bilan')
    await Kino_Yuklash_State.film_number.set()


@dp.message_handler(state=Kino_Yuklash_State.film_cod)
async def gfdggdsg(message: types.Message):
    await message.answer(f'Bu yerga faqat video yuboring')


# 2
@dp.message_handler(lambda message: message.text.isdigit(), state=Kino_Yuklash_State.film_number)
async def psfsd(message: types.Message, state: FSMContext):
    number = message.text
    film = []
    try:
        await db.create()
        film = await db.select_film(film_number=number)
        await db.disconnect()
    except:
        pas = 0
    if not film is None:
        await message.answer(f"Bu raqamda film mavjud\n", reply_markup=admin_menu)
        await message.answer_video(video=film[2], caption=f"🍿 | Nomi: {film[3]}\n"
                                                          f"🇺🇿 | Tili: {film[4]}\n"
                                                          f"🗂 | Hajmi: {film[5]}\n"
                                                          f"🎞 | Sifati: {film[6]}\n"
                                                          f"🎭 | Janri:  {film[7]}\n"
                                                          f"👀 | Ko’rish katigoriyasi: {film[8]}\n"
                                                          f"⏳ | Davomiyligi: {film[9]}\n"
                                                          f"➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                                          f"🤖 | Bizning bot: @KINOKOM_BOT\n")
        # await message.answer(f'Kino nomini yuboring')
        #
        # film_number = message.text
        # await state.update_data({"film_number": str(film_number)})
        #
        # await Kino_Yuklash_State.name.set()
        yangilash = 1
    else:
        yangilash = 0
    await message.answer(f'Kino nomini yuboring')

    film_number = message.text
    await state.update_data({"film_number": str(film_number)})
    await state.update_data({"yangilash": yangilash})

    await Kino_Yuklash_State.name.set()


# 3
@dp.message_handler(state=Kino_Yuklash_State.name)
async def psfsd(message: types.Message, state: FSMContext):
    await message.answer(f'Kino qaysi tilda yuboring')
    name = message.text

    await state.update_data({"name": str(name)})

    await Kino_Yuklash_State.tili.set()


# 4
@dp.message_handler(state=Kino_Yuklash_State.tili)
async def pdsffsdfd(message: types.Message, state: FSMContext):
    await message.answer(f'Kino hajmini yuboring')
    tili = message.text

    await state.update_data({"tili": str(tili)})

    await Kino_Yuklash_State.hajmi.set()


# 5
@dp.message_handler(state=Kino_Yuklash_State.hajmi)
async def pddfsfsd(message: types.Message, state: FSMContext):
    await message.answer(f'Kino sifatini yuboring')
    hajmi = message.text

    await state.update_data({"hajmi": str(hajmi)})

    await Kino_Yuklash_State.sifati.set()


# 6
@dp.message_handler(state=Kino_Yuklash_State.sifati)
async def pddfsfsd(message: types.Message, state: FSMContext):
    await message.answer(f'Kino janrini yuboring')
    sifati = message.text

    await state.update_data({"sifati": str(sifati)})

    await Kino_Yuklash_State.janri.set()


# 7
@dp.message_handler(state=Kino_Yuklash_State.janri)
async def pddfsfsd(message: types.Message, state: FSMContext):
    await message.answer(f"Kino ko'rish yoshini yuboring")
    janri = message.text

    await state.update_data({"janri": str(janri)})

    await Kino_Yuklash_State.korish_yoshi.set()


# 8
@dp.message_handler(state=Kino_Yuklash_State.korish_yoshi)
async def pddfsfsd(message: types.Message, state: FSMContext):
    await message.answer(f"Kino davomiyligini yuboring")
    korish_yoshi = message.text

    await state.update_data({"korish_yoshi": str(korish_yoshi)})

    await Kino_Yuklash_State.davomiyligi.set()


# 9
@dp.message_handler(state=Kino_Yuklash_State.davomiyligi)
async def pddfsfsd(message: types.Message, state: FSMContext):
    data = await state.get_data()

    yangilash = int(data.get('yangilash'))

    film_cod = data.get('video_id')
    film_number = data.get('film_number')
    name = data.get('name')
    tili = data.get('tili')
    hajmi = data.get('hajmi')
    sifati = data.get('sifati')
    janri = data.get('janri')
    korish_yoshi = data.get('korish_yoshi')
    davomiyligi = str(message.text)

    film_yangi = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    try:
        await db.create()
        if yangilash == 0:
            film_yangi = await db.add_film(film_number=film_number, film_cod=film_cod, name=name, tili=tili,
                                           hajmi=hajmi, sifati=sifati, janri=janri, korish_yoshi=korish_yoshi,
                                           davomiyligi=davomiyligi)
            await message.answer(f"✅Kino yuklandi", reply_markup=admin_menu)
        if yangilash == 1:
            await db.update_film(str(film_number), film_cod=film_cod, name=name, tili=tili,
                                 hajmi=hajmi, sifati=sifati, janri=janri, korish_yoshi=korish_yoshi,
                                 davomiyligi=davomiyligi)
            film_yangi = await db.select_film(name=name)
            await message.answer(f"🔄Kino yangilandi", reply_markup=admin_menu)

        await db.disconnect()
    except:
        await bot.send_message(chat_id=7010118152, text=f"Xato admin.py pddfsfsd_fuction")

    await message.answer_video(video=film_yangi[2], caption=f"🍿 | Nomi: {film_yangi[3]}\n"
                                                            f"🇺🇿 | Tili: {film_yangi[4]}\n"
                                                            f"🗂 | Hajmi: {film_yangi[5]}\n"
                                                            f"🎞 | Sifati: {film_yangi[6]}\n"
                                                            f"🎭 | Janri:  {film_yangi[7]}\n"
                                                            f"👀 | Ko’rish katigoriyasi: {film_yangi[8]}\n"
                                                            f"⏳ | Davomiyligi: {film_yangi[9]}\n"
                                                            f"➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                                            f"🤖 | Bizning bot: @KINOKOM_BOT\n")

    await state.finish()
