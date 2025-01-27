from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, db, bot

@dp.callback_query_handler(lambda call: "kanallar_r:" in call.data)
async def ochir_kanal(call: types.CallbackQuery, state: FSMContext):
    try:
        nom = call.data.replace("kanallar_r:", '')
        tugma = InlineKeyboardMarkup(row_width=1)
        tugma.add(InlineKeyboardButton("❌", callback_data=f"ochir:{nom}"))
        text = (f"{nom} nomli kanalni"
                f"\no'chirish uchun ❌ bosing")
        await call.message.answer(text=text, reply_markup=tugma)
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: "ochir:" in call.data)
async def remove_kanal(call: types.CallbackQuery):
    try:
        nom = call.data.replace("ochir:", '')
        db.delete_k(kanal_nomi=nom)
        await call.message.delete()
        await call.message.answer(text=f"{nom} nomli kanal o'chirildi")
    except:
        await call.answer("O'chirishda xatolik")