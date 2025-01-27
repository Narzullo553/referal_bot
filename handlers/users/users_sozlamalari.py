from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, db



@dp.callback_query_handler(text='referal')
async def referal_callback(call: types.CallbackQuery):
    try:
        text = (f"Diqat !!"
                f"\nBu bo'limda hamma foydalanuvchilar"
                f"\nreferallari 0 qiymatga o'zgaradi"
                f"\nboshlash uchun tugamani bosing")
        tugma = InlineKeyboardMarkup(row_width=1)
        tugma.add(InlineKeyboardButton("Boshlash", callback_data="referal_boshlash"))
        await call.message.answer(text=text, reply_markup=tugma)
    except:
        await call.message.answer(text="Hatolik yuz berdi")


@dp.callback_query_handler(text="referal_boshlash")
async def referal_boshlash(call: types.CallbackQuery):
    try:
        await call.message.delete()
        db.updete_users_referal_clear()
        await call.message.answer(text="Referallar o'chirildi. 0 qiymatga o'zgartirildi")
    except:
        await call.message.answer(text="O'chirishda xatolik")


@dp.callback_query_handler(text="referal_edit")
async def referal_edit(call: types.CallbackQuery):
    try:
        await call.message.delete()
        text = (f"Diqat!!"
                f"\nBu bo'limda siz tanlagan foydalanuvchini"
                f"\nreferallari sonini o'zgartiradi"
                f"\nreferallarini o'zgartirish uchun tugamani bosing")
        tugma = InlineKeyboardMarkup(row_width=1)
        tugma.add(InlineKeyboardButton("O'zgartirish", callback_data="referal_edit_start"))
        await call.message.answer(text=text, reply_markup=tugma)
    except:
        await call.message.answer(text="Hatolik yuz berdi")

@dp.callback_query_handler(text="referal_edit_start")
async def referal_edit_start(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
        await call.message.answer(text="Siz tanlagan foydalanuvchini"
                                       "telegram_id:refsoni ko'rinishda yozing"
                                       "misol: 5609632063:15")
        await state.set_state("referal_edit_soni")
    except:
        await call.message.answer(text="Hatolik yuz berdi")

@dp.message_handler(state="referal_edit_soni")
async def referal_edit_soni(msg: types.Message, state: FSMContext):
    try:
        user_id, ref_soni = msg.text.split(":")
        user_id = int(user_id)
        ref_soni = int(ref_soni)
        db.add_users_referal(tg_id=user_id, number=ref_soni)
        await msg.answer(text=f"Foydalanuvchi {user_id}ning referallari {ref_soni}ga o'zgartirildi")
        await state.finish()
    except:
        await msg.answer(text="Xato. Telegram_id:refsoni formatida yozing")


@dp.callback_query_handler(text="user_edit")
async def user_edit(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
        text = (f"Diqat!!"
                f"\nBu bo'limda siz tanlagan foydalanuvchini"
                f"\ntelegram idni  o'zgartira olasiz"
                f"\nold_tg_id:new_tg_id ko'rinishda yozing"
                f"misol: 5609632063:5609632065")
        await call.message.answer(text=text)
        await state.set_state("user_edit_start")
    except:
        await call.message.answer(text="Hatolik yuz berdi")

@dp.message_handler(state="user_edit_start")
async def user_edit_start(msg: types.Message, state: FSMContext):
    try:
        old_tg_id, new_tg_id = msg.text.split(":")
        old_tg_id = int(old_tg_id)
        new_tg_id = int(new_tg_id)
        db.updete_users(old_tg_id, new_tg_id)
        await msg.answer(text=f"Foydalanuvchi {old_tg_id}ning telegram idsi {new_tg_id}ga o'zgartirildi")
        await state.finish()
    except:
        await msg.answer(text="Xato. old_tg_id:new_tg_id formatida yozing")