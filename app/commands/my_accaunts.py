from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import app.database.requests as rq
import app.keyboards.keyboards as kb
from app.states.states import EditAccount
from app.utils.facebook.get_statistic import get_facebook_campaign_statistics
# from app.utils.facebook.get_ad_name_accounts import get_ad_name_campaigns_by_account
from app.utils.facebook.get_account_currency import get_account_currency
# from app.utils.facebook.fetch_ads_and_statistics import fetch_ads_and_statistics
# from app.utils.long_message import send_long_message

router = Router()

@router.message(Command("my_accounts"))
async def my_accounts_command_handler(message: Message, state: FSMContext):
    await my_accounts_logic(message, state)

@router.message(F.text == "Мои аккаунты")
async def my_accounts_button_handler(message: Message, state: FSMContext):
    await my_accounts_logic(message, state)

async def my_accounts_logic(message: Message, state: FSMContext):
    # Общая логика для обработки команды и кнопки
    user_id = await rq.get_user_id_by_tg_id(message.from_user.id)
    await message.answer("Список ваших аккаунтов:", reply_markup=await kb.accounts_keyboard(user_id))
    
@router.callback_query(F.data.startswith("account_"))
async def account_callback_handler(callback: CallbackQuery, state: FSMContext):
    account_id = int(callback.data.split("_")[1])
    account_name = await rq.get_account_by_id(account_id)
    await state.update_data(account_id=account_id)
    if account_name:
        await callback.message.answer(f"Выберите действие для аккаунта {account_name}:", reply_markup=await kb.account_actions_keyboard())
    else:
        await callback.message.answer("Аккаунт не найден.")

@router.callback_query(F.data == "edit_account")
async def edit_account_callback_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    account_name = await rq.get_account_by_id(int(data["account_id"]))
    await callback.message.answer(f"Редактирование аккаунта {account_name}:", reply_markup=await kb.edit_account_keyboard())

@router.callback_query(F.data == "edit_token")
async def edit_token_callback_handler(callback: CallbackQuery, state: FSMContext):
    print("edit_token_callback_handler")
    await state.set_state(EditAccount.edit_token)
    await callback.message.answer("Введите новый токен аккаунта:")

# Измените обработчик process_edit_token
@router.message(EditAccount.edit_token)
async def process_edit_token(message: Message, state: FSMContext):
    print("process_edit_token")
    await state.update_data(token=message.text)
    data = await state.get_data()
    await rq.update_campaign_token(int(data["campaign_id"]), data["token"])
    await state.clear()
    await message.answer("Токен успешно изменен.", reply_markup=kb.main_menu)

# Измените обработчик edit_time_check_statistic
@router.callback_query(F.data == 'edit_time_check_statistic')
async def edit_time_check_statistic_callback_handler(callback: CallbackQuery, state: FSMContext):
    print("edit_time_check_statistic")
    await state.set_state(EditAccount.edit_time_check_statistic)
    await callback.message.answer("Введите новое время проверки статистики:")

# Измените обработчик process_edit_time_check_statistic
@router.message(EditAccount.edit_time_check_statistic)
async def process_edit_time_check_statistic(message: Message, state: FSMContext):
    print("process_edit_time_check_statistic")
    try:
        time_value = int(message.text)
        if time_value not in [30, 60]:
            await message.answer("Пожалуйста, введите 30 или 60.")
            return
            
        await state.update_data(time_check_statistic=time_value)
        data = await state.get_data()
        print(data)
        await rq.update_campaign_time_check_statistic(int(data["campaign_id"]), time_value)
        await state.clear()
        await message.answer("Время проверки статистики успешно изменено.", reply_markup=kb.main_menu)
    except ValueError:
        await message.answer("Ошибка: введите корректное значение времени (30 или 60).")

@router.callback_query(F.data == 'back_to_accounts')
async def back_to_accounts_callback_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    account_name = await rq.get_account_by_id(int(data["account_id"]))
    await callback.message.answer(f"Выберите действие для аккаунта {account_name}:", reply_markup=await kb.account_actions_keyboard())

@router.callback_query(F.data == 'back_to_all_accounts')
async def back_to_all_accounts_callback_handler(callback: CallbackQuery, state: FSMContext):
    user_id = await rq.get_user_id_by_tg_id(callback.from_user.id)
    await callback.message.answer("Список ваших аккаунтов:", reply_markup=await kb.accounts_keyboard(user_id))

@router.callback_query(F.data == 'delete_campaign')
async def delete_campaign_callback_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    account_name = await rq.get_account_by_id(int(data["account_id"]))
    await rq.delete_account(int(data["account_id"]))
    await callback.message.answer(f"Аккаунт {account_name} удален.", reply_markup=kb.main_menu)

@router.callback_query(F.data == 'check_statistic')
async def check_statistic_callback_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    info_account = await rq.get_info_account_by_id(int(data["account_id"]))
    await callback.message.answer(f"Статистика аккаунта {info_account.name}:")
    response = await get_facebook_campaign_statistics(info_account.token, info_account.account_id)
    currency = await get_account_currency(info_account.token, info_account.account_id)
    message = ""
    print(response)
    
    if response:
        for campaign in response:
            message += (
                f"Название кампании: {campaign['campaign_name']}\n"
                f"Показы: {campaign['impressions']}\n"
                f"Клики: {campaign['clicks']}\n"
                f"Расходы: {campaign['spend']} {currency['currency']}\n"
                f"CTR: {campaign['ctr']}\n"
                f"CPM: {campaign['cpm']}\n"
                f"CPC: {campaign['cpc']}\n"
                f"Уникальные пользователи: {campaign['reach']}\n"
                f"Дата начала: {campaign['date_start']}\n"
                f"Дата окончания: {campaign['date_stop']}\n"
                f"{'-' * 30}\n"  # Разделитель между кампаниями
            )
    else:
        message = "Нет доступной статистики для этого аккаунта."

    # Отправляем одно сообщение
    await callback.message.answer(message)
    # data = await state.get_data()
    # info_account = await rq.get_info_account_by_id(int(data["account_id"]))
    
    # campaigns_response = await get_facebook_campaign_statistics(info_account.token, info_account.account_id)
    # currency = await get_account_currency(info_account.token, info_account.account_id)
    
    # if 'data' not in campaigns_response or not campaigns_response['data']:
    #     await callback.message.answer("Нет доступной статистики для этого аккаунта.", parse_mode="HTML")
    #     return

    # for campaign in campaigns_response['data']:
    #     # Получаем данные о группах объявлений и статистику
    #     ads_and_stats = await fetch_ads_and_statistics(info_account.token, info_account.account_id, campaign['campaign_id'])
        
    #     # Формируем сообщение для кампании
    #     message = f"<b>{campaign['campaign_name']}</b>\n"  # Название кампании выделено жирным
        
    #     # Добавляем информацию о группах объявлений
    #     if ads_and_stats['adsets']:
    #         for i, adset in enumerate(ads_and_stats['adsets'], 1):
    #             message += f"{i}. <b>{adset['name']}</b> - {adset['status']}\n"  # Название группы объявлений выделено жирным
                
    #             # Находим статистику для объявлений этой группы
    #             if ads_and_stats['statistics']:
    #                 for stat in ads_and_stats['statistics']:
    #                     message += (
    #                         f"  - <b>{stat.get('ad_name', f'ad_{stat['ad_id']}')}</b>:\n"  # Название объявления выделено жирным
    #                         f"    Показы: <b>{stat['impressions']}</b>; "
    #                         f"Клики: <b>{stat['clicks']}</b>; "
    #                         f"Расходы: <b>{stat['spend']}</b> {currency['currency']}; "
    #                         f"CTR: <b>{stat['ctr']}</b>; "
    #                         f"CPM: <b>{stat['cpm']}</b>; "
    #                         f"CPC: <b>{stat['cpc']}</b>\n"  # Значения показателей выделены жирным
    #                     )
    #             else:
    #                 message += "  Нет доступной статистики для объявлений.\n"
    #     else:
    #         message += "Нет доступных групп объявлений.\n"
        
    #     # Отправляем сообщение, разделяя его при необходимости
    #     await send_long_message(message, callback, parse_mode="HTML")
    #     # Разделитель между кампаниями
    #     await callback.message.answer("-" * 30, parse_mode="HTML")


