from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import app.database.requests as rq
import app.keyboards.keyboards as kb
from app.states.states import Register

router = Router()

@router.message(F.text == "В главное меню")
async def go_to_main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите действие", reply_markup=kb.main_menu)

