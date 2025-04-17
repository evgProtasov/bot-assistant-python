from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import app.database.requests as rq
import app.keyboards.keyboards as kb
from app.states.states import Register
from app.commands.bot_commands import set_bot_commands
from app.bot.bot import bot

router = Router()

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    try:
        await set_bot_commands(bot)
        user_tg_id = message.from_user.id
        user = await rq.get_user(user_tg_id)
        
        if not user:
            await message.answer("Вы не авторизованы. Пожалуйста, авторизуйтесь.", reply_markup=kb.web_auth)
            await state.set_state(Register.web_auth)
        else:
            await message.answer("Вы уже авторизованы. Пожалуйста, выберите действие.", reply_markup=kb.main_menu)
            await state.clear()
    except Exception as e:
        print(e)