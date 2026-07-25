from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

class OrderForm(StatesGroup):
    name = State()
    age = State()
    description = State()
    confirm = State()

@router.message(Command("order"))
async def start_order(message: types.Message, state: FSMContext):
    await message.answer("Начинаем оформление заявки. Как вас зовут?")
    await state.set_state(OrderForm.name)

@router.message(OrderForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(user_name=message.text)

    await message.answer("Принято. Сколько вам полных лет?")
    await state.set_state(OrderForm.age)


@router.message(OrderForm.age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите возраст цифрами!")
        return

    await state.update_data(user_age=int(message.text))

    await message.answer("Опишите кратко суть вашей заявки:")
    await state.set_state(OrderForm.description)


@router.message(OrderForm.description)
async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(user_desc=message.text)

    data = await state.get_data()

    preview_text = (
        f"Проверьте ваши данные:\n\n"
        f"👤 Имя: {data.get('user_name')}\n"
        f"🔢 Возраст: {data.get('user_age')}\n"
        f"📝 Описание: {data.get('user_desc')}\n\n"
        f"Всё верно?"
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Да, отправить", callback_data="form_confirm")
    builder.button(text="❌ Отмена", callback_data="form_cancel")

    await message.answer(preview_text, reply_markup=builder.as_markup())
    await state.set_state(OrderForm.confirm)


@router.callback_query(OrderForm.confirm, F.data == "form_confirm")
async def form_confirmed(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()


    await callback.message.edit_text("🎉 Заявка успешно отправлена! Менеджер свяжется с вами.")
    await callback.answer()

    await state.clear()


@router.callback_query(F.data == "form_cancel")
async def form_cancelled(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Оформление заявки отменено.")
    await callback.answer()
    await state.clear()