from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import ADMINS
from filters import IsPrivate
from loader import dp, bot, db
from aiogram import types



@dp.message_handler(IsPrivate(),text="🔗 Referal",state='*')
async def referrals_handler(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        referral_link = f"https://t.me/{(await bot.get_me()).username}?start={user_id}"
        await message.answer(
            f"Assalomu alaykum! Sizning shaxsiy taklif havolangiz: \n{referral_link}\n\n"
        )
        await state.finish()
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=f"referrals_handler: {e}")
@dp.message_handler(IsPrivate(), text="📊 Mening natijalarim",state='*')
async def natijam(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        referal = db.select_one_users(user_id)[3]
        if not referal:
            referal = 0
        await message.answer(
            f"Siz {referal} ta do'stingizni taklif qilgansiz!"
        )
        await state.finish()
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=f"natijam: {e}")

@dp.message_handler(IsPrivate(),text="✉️ Murojaat", state='*')
async def murojaat(message: types.Message, state: FSMContext):
    try:
        tugma = InlineKeyboardMarkup(row_width=2)
        tugma.insert(InlineKeyboardButton(text="✍️ Yozish", callback_data="yozish"))
        text = "yozishni boshlash uchun tugmani bosing"
        await message.answer(text, reply_markup=tugma)
        await state.finish()
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=f"murojaat: {e}")