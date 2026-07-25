from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


class MenuCallback(CallbackData, prefix="menu"):
    action: str
    category_id: int
    item_id: int

class BuyCallback(CallbackData, prefix="buy"):
    action: str
    product_code: str

@router.message(Command("menu"))
async def show_menu(message: types.Message):
    builder = InlineKeyboardBuilder()

    categories = [
        {"id": 1, "name": "📸 Камеры"},
        {"id": 2, "name": "🔭 Объективы"}
    ]

    for cat in categories:
        builder.button(
            text=cat["name"],
            callback_data=MenuCallback(action="open_cat", category_id=cat["id"], item_id=0)
        )

    builder.adjust(1)

    await message.answer("Выберите категорию товаров:", reply_markup=builder.as_markup())


@router.callback_query(MenuCallback.filter(F.action == "open_cat"))
async def process_category_click(callback: types.CallbackQuery, callback_data: MenuCallback):
    category_id = callback_data.category_id
    builder = InlineKeyboardBuilder()

    if category_id == 1:
        text = "Вы выбрали Камеры. В наличии:\n1. Sony A7 IV - 200к\n2. Canon R6 - 180к"
        builder.button(text="Купить Sony", callback_data=BuyCallback(action="buy_camera", product_code="sony"))
        builder.button(text="Купить Canon", callback_data=BuyCallback(action="buy_camera", product_code="canon"))
        builder.adjust(2, 1)
    else:
        text = "Вы выбрали Объективы. В наличии:\n1. Sigma 35mm f/1.4 - 70к\n2. Sony 85mm f/1.4 - 120к"

    builder.button(
        text="⬅️ Назад в меню",
        callback_data=MenuCallback(action="main_menu", category_id=0, item_id=0)
    )

    await callback.message.edit_text(text=text, reply_markup=builder.as_markup())
    await callback.answer(text="Каталог обновлен", show_alert=False)


@router.callback_query(BuyCallback.filter(F.action == "buy_camera"))
async def process_buy_camera(callback: types.CallbackQuery, callback_data: BuyCallback):
    code = callback_data.product_code

    if code == "sony":
        alert_text = "Камера Sony успешно добавлена в корзину!"
    elif code == "canon":
        alert_text = "Камера Canon успешно добавлена в корзину!"
    else:
        alert_text = "Товар добавлен в корзину"

    await callback.answer(text=alert_text, show_alert=True)

@router.callback_query(MenuCallback.filter(F.action == "main_menu"))
async def return_to_main_menu(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="📸 Камеры", callback_data=MenuCallback(action="open_cat", category_id=1, item_id=0))
    builder.button(text="🔭 Объективы", callback_data=MenuCallback(action="open_cat", category_id=2, item_id=0))
    builder.adjust(1)

    await callback.message.edit_text("Выберите категорию товаров:", reply_markup=builder.as_markup())
    await callback.answer()