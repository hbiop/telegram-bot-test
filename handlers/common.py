from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Я бот на aiogram 3.")

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Доступные команды:\n/start - запуск\n/help - помощь")

@router.message(F.text.lower == "как дела?")
async def how_are_you(message: types.Message):
    await message.answer("Отлично! Работаю без выходных.")