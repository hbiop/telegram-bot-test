from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.db_utils.base import User

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, session: AsyncSession):
    # Проверяем, есть ли пользователь в нашей PostgreSQL
    result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
    user = result.scalar_one_or_none()

    if not user:
        # Если пользователя нет — создаем новую запись
        user = User(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name
        )
        session.add(user)
        await session.commit() # Сохраняем в базу данных
        text = f"Привет, {message.from_user.full_name}! Рад видеть тебя впервые."
    else:
        text = f"С возвращением, {user.full_name}! Рад тебя снова видеть."

    await message.answer(text)

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Доступные команды:\n/start - запуск\n/help - помощь")

@router.message(F.text.lower().contains("как дела"))
async def how_are_you_flexible(message: types.Message):
    await message.answer("Отлично! Рад, что спросили.")