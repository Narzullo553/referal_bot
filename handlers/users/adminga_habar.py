
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.config import ADMINS
from filters import IsAdmin_bot, IsPrivate
from loader import dp, db, bot





@dp.callback_query_handler(text="yozish")
async def zamdekanga_murojaat_boshlash(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Bot adminiga murojaatingizni yozishingiz munkin:")
    await state.set_state("admin_murojaat")


@dp.message_handler(state="admin_murojaat")
async def zamdekanga_murojaat_qabul(msg: types.Message, state: FSMContext):
    try:
        murojaat_matni = msg.text
        admin_id = ADMINS[0]
        tugma = InlineKeyboardMarkup(row_width=2)
        tugma.insert(InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel:{msg.from_user.id}"))
        tugma.insert(InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"confirm:{msg.from_user.id}"))
        tugma.insert(InlineKeyboardButton(text="✍️ Javob yozish", callback_data=f"yozish:{msg.from_user.id}"))
        # await msg.copy_to(chat_id=admin_id)
        await bot.send_message(
            chat_id=admin_id,
            text=f"Yangi murojaat:\n\n"
                 f"👤 Foydalanuvchi: {msg.from_user.full_name}\n"
                 f"🆔 ID: {msg.from_user.id}\n\n"
                 f"📩 Murojaat: {murojaat_matni}", reply_markup=tugma
        )
        await msg.answer("Rahmat! Sizning murojaatingiz adminga yuborildi. Tez orada javob olasiz.")
        await state.finish()

    except Exception as e:
        await msg.answer("Xatolik yuz berdi! Keyinroq urinib ko'ring.")
        await state.finish()


@dp.callback_query_handler(lambda call: "cancel:" in call.data)
async def cancel_xabar(call: types.CallbackQuery):
    data = int(call.data.replace('cancel:', '').strip())
    await bot.send_message(chat_id=data, text="Murojatingiz rad etildi !!")
    await call.message.delete()
    await call.answer("Murojaat rad qilindi!")

@dp.callback_query_handler(lambda call: "confirm:" in call.data)
async def confirm_xabar(call: types.CallbackQuery):
    foydalanuvchi_id = call.data.split(":")[1]
    await bot.send_message(chat_id=foydalanuvchi_id, text="Sizning murojaatingiz qabul qilindi!")
    await call.answer("Murojaat qabul qilindi!")
    await call.message.delete()

@dp.callback_query_handler(IsAdmin_bot(), lambda call: "yozish:" in call.data, state=None)
async def javob_yozish(call: types.CallbackQuery, state: FSMContext):
    tg_id = int(call.data.replace("yozish:", '').strip())
    await call.message.answer("javob yozishingiz mumkin !!")
    await state.update_data(
        {
            'id': tg_id
        }
    )
    await state.set_state("javob_yozish_boshlash")

@dp.message_handler(state='javob_yozish_boshlash',content_types=types.ContentType.ANY)
async def foydalanuchiga_habar_yuborish(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    id_t = data.get('id')
    await msg.copy_to(chat_id=id_t)
    await msg.answer(text="xabaringiz yuborildi")
    await state.finish()