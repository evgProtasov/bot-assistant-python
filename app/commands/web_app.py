# app/handlers/web_app.py
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.utils.web_app_data import handle_web_app_data
from app.states.states import Register
import app.database.requests as rq
import app.keyboards.keyboards as kb

router = Router()

@router.message(F.web_app_data)
async def web_app_handler(message: Message, state: FSMContext):    
    try:
        current_state = await state.get_state()
        
        if current_state != Register.web_auth.state:
            return
                
        success, response = await handle_web_app_data(message)
        
        if success:
            await state.clear()
            checkUser = await rq.get_user(message.from_user.id)
            
            if checkUser:
                await message.answer(response, reply_markup=kb.main_menu)
            
        else:
            await state.set_state(Register.web_auth)
            await message.answer(response, reply_markup=kb.web_auth)
    except Exception as e:
        print(f"Error in web_app_handler: {e}")
        await message.answer("Произошла ошибка при обработке данных", reply_markup=kb.auth)