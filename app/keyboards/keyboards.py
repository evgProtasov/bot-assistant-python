from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.database.requests import get_accounts

web_auth = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(
        text="Авторизоваться",
        web_app=WebAppInfo(url="https://systems-geeks.com/Auth")
        )]], 
        resize_keyboard=True,
        input_field_placeholder='Нажмите для авторизации'
)

main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Мои аккаунты")],
    [KeyboardButton(text="Добавить аккаунт")],
    [KeyboardButton(text="Настройки")]
], resize_keyboard=True)

back_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Назад")]
], resize_keyboard=True)

to_main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="В главное меню")]
], resize_keyboard=True)

# Кнопки для аккаунтов
async def accounts_keyboard(user_id: int):
    accounts = await get_accounts(user_id)
    
    buttons = [[InlineKeyboardButton(text=account.name, callback_data=f"account_{account.id}")] for account in accounts]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

# Кнопки для действий с аккаунтом
async def account_actions_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Посмотреть статистику", callback_data="check_statistic")],
        [InlineKeyboardButton(text="Редактировать", callback_data="edit_account")],
        [InlineKeyboardButton(text="Удалить", callback_data="delete_account")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_all_accounts")] 
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

# Кнопки для редактирования аккаунта
async def edit_account_keyboard():
    
    buttons = [
        [InlineKeyboardButton(text="Изменить токен аккаунта", callback_data="edit_token")],
        [InlineKeyboardButton(text="Изменить время проверки статистики", callback_data="edit_time_check_statistic")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_accounts")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard










