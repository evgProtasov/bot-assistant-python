from aiogram import Router
from app.commands.start import router as start_router
from app.commands.web_app import router as web_app_router
from app.commands.add_account import router as add_account_router
from app.commands.go_to_main_menu import router as go_to_main_menu_router
from app.commands.my_accaunts import router as my_accaunts_router

router = Router()

router.include_routers(
    start_router,
    web_app_router,
    add_account_router,
    go_to_main_menu_router,
    my_accaunts_router
)

