from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from filters import IsPrivate
from loader import dp, db, bot



@dp.message_handler(IsPrivate(),text="Statistika 📊", state='*')
async def statistika(msg: types.Message, state: FSMContext):
    try:
        text, tugma = await kanal_xammasi11()
        if text != 2:
            await msg.answer(text, reply_markup=tugma)
        else:
            await msg.answer(text="Malumotlar topilmadi")
        await state.finish()
    except:
        await msg.answer("hatolik yuz berdi")


async def kanal_xammasi11(page=1):
    try:
        uzunlik = db.select_count_users()[0]
        if uzunlik+10 - page*10 >=0:
            users = db.select_all_users1(page=page)
        else:
            users = None
        create_quiz_menu1 = InlineKeyboardMarkup(row_width=5)
        if users:
            s = page*10-10+1
            text = f"foydalanuvchilar ro'yhati {s}-{page*10}: {uzunlik}"
            for son, nomi in enumerate(users, start=1):
                text += '\n' + f"{s+son-1}. name:  {nomi[1]} tg_id: {nomi[2]}  referal: {nomi[3]}"
            create_quiz_menu1.row(
                InlineKeyboardButton("◀", callback_data=f"page11:{page-1}"),
                InlineKeyboardButton("❌", callback_data=f"clear"),
                InlineKeyboardButton("▶", callback_data=f"page11:{page+1}"),
            )
            return text, create_quiz_menu1
        else:
            return 2, 2
    except Exception as e:
        return
@dp.callback_query_handler(lambda call: "clear" in call.data)
async def clear(call: types.CallbackQuery):
    await call.message.delete()

@dp.callback_query_handler(lambda call: "page11:" in call.data)
async def testlar121(call: types.CallbackQuery):
    try:
        _, page = call.data.split(":")
        if int(page) > 0:
            text, tugma = await kanal_xammasi11(page=int(page))
            if tugma != 2:
                await call.message.delete()
                await call.message.answer(text=f"📋 {text}", reply_markup=tugma)
            else:
                await call.answer("foydalanuvchilar topilmadi")
        else:
            await call.answer("foydalanuvchilar topilmadi")
    except:
        await call.answer("foydalanuvchilar topilmadi")