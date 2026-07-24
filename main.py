from aiogram import Dispatcher, Bot
from config_reader import config

bot = Bot(token=config.TOKEN)
dispatcher = Dispatcher()


if __name__ == '__main__':
    ...
