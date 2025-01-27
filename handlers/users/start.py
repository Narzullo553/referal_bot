from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS, admin
from filters import IsPrivate
from keyboards.default.bosh_menu import admin_reply_buttons, user_reply_buttons
from loader import dp, db, bot
from data.config import msge, admin
from aiogram.dispatcher import FSMContext


@dp.message_handler(text='/cancel', state='*')
async def bekor_qil(msg:types.Message, state: FSMContext):
    await msg.answer("jarayon yakunlandi")
    await msg.delete()
    await state.finish()

# @dp.message_handler('admins')
# async def admin_list(message: types.Message):
#     admin.append(str(message.from_user.id))
#     await message.answer(f"Adminga aylandingiz")


@dp.message_handler(IsPrivate(), CommandStart())
async def bot_start(message: types.Message):
    try:
        user = message.from_user
        m_user = db.select_one_users(user.id)
        if m_user is None:
            msg = msge.get(user.id, {})
            if msg:
                referrer_id = msg.get_args()
                del msge[user.id]
            else:
                referrer_id = message.get_args()
            if referrer_id:
                referrer_id = int(referrer_id)
                if referrer_id != user.id:
                    big_user = db.select_one_users(referrer_id)
                    db.add_users_referal(referrer_id, number=int(big_user[3])+1)
                    await bot.send_message(chat_id=referrer_id, text=f"{big_user[1]} teklif havolangiz orqali {user.full_name} qo'shildi"
                                                                     f"\nhozida referalingiz: {big_user[3]+1} ")
            db.add_users(fullname=user.full_name, telegram_id=user.id, referal=0)
        if str(user.id) in ADMINS:
            await message.answer("Assalomu alaykum \nbo'limlardan birini tanlang!!",reply_markup=admin_reply_buttons())
        else:
            await message.answer("Assalomu alaykum \nbo'limlardan birini tanlang!!",reply_markup=user_reply_buttons())
    except Exception as err:
        await bot.send_message(chat_id=ADMINS[0], text=f"start: {err}")

