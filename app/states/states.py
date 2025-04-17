from aiogram.fsm.state import State, StatesGroup

class Register(StatesGroup):
    web_auth = State()
    
    
class AddAccount(StatesGroup):
    name = State()
    account_id = State()
    token = State()
    time_check_statistic = State()
    
class EditAccount(StatesGroup):
    edit_token = State()
    edit_time_check_statistic = State()

