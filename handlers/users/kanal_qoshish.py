from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS, msge
from keyboards.default.bosh_menu import admin_reply_buttons, user_reply_buttons
from loader import dp, db, bot

@dp.callback_query_handler(text="qosh:")
async def qoshish_kanal(call: types.CallbackQuery, state: FSMContext):
    try:
        text = """
        🌟 Majburiy obuna kanal qo'shmoqchi bo'lsangiz 🌟
        📩 Kanal (yoki guruh) linkini yoki ID raqamini yuboring!
        ⚠️ Eslatma:
        🤖 Bot ushbu kanal (yoki guruh)da Admin bo'lishi shart!
        misol: @MurodullayevNarzullo
        """
        await call.message.delete()
        await  call.message.answer(text)
        await state.set_state('kanal_qosh')
    except Exception as e:
        print(e)
@dp.message_handler(state='kanal_qosh')
async def kanalni_qosh(msg: types.Message, state: FSMContext):
    db.add_k(msg.text)
    await msg.answer("Kanallar ro'yhatiga qo'shildi")
    await state.finish()


@dp.callback_query_handler(text ='tekshir')
async def tegishir(call: types.CallbackQuery, state: FSMContext):
    try:
        user = call.from_user
        m_user = db.select_one_users(user.id)
        if m_user is None:
            msg = msge.get(user.id, {})
            if msg:
                referrer_id = msg.get_args()
                del msge[user.id]
            else:
                referrer_id = call.data.get_args()
            if referrer_id:
                referrer_id = int(referrer_id)
                if referrer_id != user.id:
                    big_user = db.select_one_users(referrer_id)
                    db.add_users_referal(referrer_id, number=int(big_user[3])+1)
                    await bot.send_message(chat_id=referrer_id, text=f"{big_user[1]} teklif havolangiz orqali {user.full_name} qo'shildi"
                                                                     f"\nhozida referalingiz: {big_user[3]+1} ")
            db.add_users(fullname=user.full_name, telegram_id=user.id, referal=0)
        await call.message.delete()
        if str(user.id) in ADMINS:
            await call.message.answer("Assalomu alaykum \nbo'limlardan birini tanlang!!", reply_markup=admin_reply_buttons())
        else:
            await call.message.answer("Assalomu alaykum \nbo'limlardan birini tanlang!!", reply_markup=user_reply_buttons())
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=f"tekshir: {e}")
