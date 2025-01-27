from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import ChatNotFound
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot, db
from data.config import msge


class SubscriptionMiddleware(BaseMiddleware):


    async def on_pre_process_update(self, update: types.Update, data: dict):
        user_id = None
        if update.message:
            user_id = update.message.from_user.id
        elif update.callback_query:
            user_id = update.callback_query.from_user.id
        elif update.inline_query:
            user_id = update.inline_query.from_user.id

        if not user_id:
            return
        not_subscribed_channels = True
        tugma = InlineKeyboardMarkup(row_width=1)
        for channel in db.select_k():
            try:
                channel =list(channel)[0]
                if channel[0] == "h":
                    tugma.add(
                        InlineKeyboardButton(
                            text="Obuna bo'lish ✅",
                            url=channel,
                        )
                    )
                elif channel[0] == '@':
                    url = f"https://t.me/{channel.replace('@', '')}"
                    member = await update.bot.get_chat_member(chat_id=channel, user_id=user_id)
                    if member.status == 'left':
                        not_subscribed_channels = False
                        tugma.add(
                            InlineKeyboardButton(
                                text="Obuna bo'lish ✅",
                                url=url,
                            )
                        )
                else:
                    chat = await bot.get_chat(channel)
                    url = chat.invite_link
                    member = await update.bot.get_chat_member(chat_id=channel, user_id=user_id)
                    if member.status == 'left':
                        not_subscribed_channels = False
                        tugma.add(
                            InlineKeyboardButton(
                                text="Obuna bo'lish ✅",
                                url=url,
                            )
                        )
            except ChatNotFound:
                tugma.add(
                    InlineKeyboardButton(
                        text="Obuna bo'lish ✅",
                        url=f"https://t.me/{channel.replace('@', '')}",
                    )
                )

        if not not_subscribed_channels:
            text = "Botdan foydalanish uchun quyidagi kanal(lar)ga obuna bo‘ling:\n"
            tugma.add(InlineKeyboardButton(text="✅ — Obuna bo'ldim", callback_data='tekshir'))
            await bot.send_message(
                chat_id=user_id,
                text=text,
                parse_mode="Markdown",
                disable_web_page_preview=True,
                reply_markup=tugma,
            )
            if update.message:
                msg = msge.get(user_id, {})
                if not msg:
                    ref_id = update.message.get_args()
                    if ref_id != user_id:
                        msge[user_id] = update.message
            raise CancelHandler()
