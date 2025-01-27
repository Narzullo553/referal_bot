from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS, msge
from filters import IsPrivate
from loader import dp, db, bot


# Echo bot
@dp.message_handler(IsPrivate(), state='*')
async def bot_echo(message: types.Message, state: FSMContext):
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
        if '@' in message.text:
            chat = await bot.get_chat(str(message.text))
            text = chat.id
        else:
            text = message.text
        await message.answer(text)
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=f"echo: {e}")
