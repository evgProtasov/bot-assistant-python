from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import app.database.requests as rq
import app.keyboards.keyboards as kb
from app.states.states import AddAccount
from app.commands.go_to_main_menu import go_to_main_menu

router = Router()

@router.message(Command("add_account"))
async def add_account_command_handler(message: Message, state: FSMContext):
    await add_account_logic(message, state)

@router.message(F.text == "Добавить аккаунт")
async def add_account_button_handler(message: Message, state: FSMContext):
    await add_account_logic(message, state)

async def add_account_logic(message: Message, state: FSMContext):
    await state.set_state(AddAccount.name)
    await message.answer("Введите название аккаунта", reply_markup=kb.to_main_menu)

@router.message(AddAccount.name)
async def process_name(message: Message, state: FSMContext):
    if message.text == "В главное меню":
        await go_to_main_menu(message, state)
        return
    await state.update_data(name=message.text)
    await state.set_state(AddAccount.account_id)
    await message.answer("Введите ID аккаунта", reply_markup=kb.back_button)
    
@router.message(AddAccount.account_id)
async def process_account_id(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.set_state(AddAccount.name)
        await message.answer("Введите название кампании", reply_markup=kb.to_main_menu)
    else:
        await state.update_data(account_id=message.text)
        await state.set_state(AddAccount.token)
        await message.answer("Введите токен", reply_markup=kb.back_button)
    
@router.message(AddAccount.token)
async def process_token(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.set_state(AddAccount.account_id)
        await message.answer("Введите ID аккаунта")
    else:
        await state.update_data(token=message.text)
        await state.set_state(AddAccount.time_check_statistic)
        await message.answer("Введите время проверки статистики (30 или 60)", reply_markup=kb.back_button)
    
@router.message(AddAccount.time_check_statistic)
async def process_time_check_statistic(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.set_state(AddAccount.token)
        await message.answer("Введите токен")
    else:
        try:
            await state.update_data(time_check_statistic=message.text)
            data = await state.get_data()
            user_tg_id = message.from_user.id
            user = await rq.get_user(user_tg_id)  # Получаем пользователя по его Telegram ID
            if user is None:
                raise ValueError("User does not exist")
            user_id = user.id  # Получаем user_id
            await rq.add_account(data["name"], int(data["account_id"]), data["token"], int(data["time_check_statistic"]), user_id)
            await state.clear()
            await message.answer("Аккаунт успешно добавлен")
            await message.answer("Выберите действие", reply_markup=kb.main_menu)
        except Exception as e:
            await message.answer("Ошибка при добавлении аккаунта")
            print(e)
    
    
    
