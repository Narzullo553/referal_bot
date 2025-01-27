from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from filters import IsPrivate, IsAdmin_bot
from loader import dp, db


@dp.message_handler(IsPrivate(),IsAdmin_bot(), text="Channel Settings ⚙️", state='*')
async def kanal_qosh(msg: types.Message, state: FSMContext):
    try:
        await state.finish()
        text, create_quiz_menu1 = await kanal_xammasi1()
        if text==2:
            await msg.answer(text=f"📋 sizda hozirda kanallar mavjud emas", reply_markup=create_quiz_menu1)
        else:
            await msg.answer(text=f"📋 {text}", reply_markup=create_quiz_menu1)
    except Exception as e:
        await msg.answer(text=f"📋 sizda hozirda kanallar mavjud emas")

@dp.message_handler(IsPrivate(),IsAdmin_bot(),text="Announcement 📢", state='*')
async def announcement(msg: types.Message, state: FSMContext):
    try:
        tugma = InlineKeyboardMarkup(row_width=2)
        tugma.insert(InlineKeyboardButton(text="✍️E'lon Yozish", callback_data=f"yangilik: yozish"))
        tugma.insert(InlineKeyboardButton(text="✍️Habar Yozish", callback_data=f"habar: yozish"))
        await msg.answer("Habar yuborish bo'limlaridan birini tanlang", reply_markup=tugma)
        await state.finish()
    except Exception as e:
        await msg.answer('hatolik yuz berdi')


@dp.message_handler(IsPrivate(),IsAdmin_bot(),text="Users 👥", state='*')
async def users(msg: types.Message, state: FSMContext):
    try:
        tugma = InlineKeyboardMarkup(row_width=2)
        tugma.insert(InlineKeyboardButton(text="referal 0", callback_data=f"referal"))
        tugma.insert(InlineKeyboardButton(text="referal edit", callback_data=f"referal_edit"))
        tugma.insert(InlineKeyboardButton(text="user edit", callback_data=f"user_edit"))
        await msg.answer(text="Foydalanuvchi malumotlarini o'zgartirish", reply_markup=tugma)
        await state.finish()
    except Exception as e:
        await msg.answer(text=f"�� hatolik yuz berdi")





















async def kanal_xammasi1(page=1):
    try:
        uzunlik = db.count_kanal()[0]
        if uzunlik+10 - page*10 >=0:
            kanal = db.select_all_kanal1(page=page)
        else:
            kanal = None
        create_quiz_menu1 = InlineKeyboardMarkup(row_width=5)
        if kanal:
            s = page*10-10+1
            text = f"kanallar ro'yhati {s}-{page*10}: {uzunlik}"
            for son, nomi in enumerate(kanal, start=1):
                text += '\n' + f"{son}. {nomi[0]}"
                create_quiz_menu1.insert(InlineKeyboardButton(text=f"{son}",
                                                           callback_data=f"kanallar_r:{nomi[0]}"))
            create_quiz_menu1.row(
                InlineKeyboardButton("◀", callback_data=f"page1:{page-1}"),
                InlineKeyboardButton("+", callback_data=f"qosh:"),
                InlineKeyboardButton("▶", callback_data=f"page1:{page+1}"),
            )
            return text, create_quiz_menu1
        else:
            create_quiz_menu1.row(InlineKeyboardButton("+", callback_data=f"qosh:"))
            return 2, create_quiz_menu1
    except Exception as e:
        return


@dp.callback_query_handler(lambda call: "page1:" in call.data)
async def testlar12(call: types.CallbackQuery):
    try:
        _, page = call.data.split(":")
        if int(page) > 0:
            text, test= await kanal_xammasi1(page=int(page))
            if test != 2:
                await call.message.delete()
                await call.message.answer(text=f"📋 {text}", reply_markup=test)
            else:
                await call.answer("kanall topilmadi")
        else:
            await call.answer("kanallar topilmadi")
    except:
        await call.answer("kanallar topilmadi")
