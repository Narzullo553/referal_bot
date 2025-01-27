from aiogram import Dispatcher
from . majburiy_obuna import SubscriptionMiddleware
from loader import dp
from .throttling import ThrottlingMiddleware



if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(SubscriptionMiddleware())
