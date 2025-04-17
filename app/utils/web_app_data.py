import json
from aiogram.types import Message
import app.database.requests as rq

async def handle_web_app_data(message: Message) -> tuple[bool, str]:
    """
    Обрабатывает данные, полученные от веб-приложения
    """
    try:
        web_app_data = message.web_app_data.data
        user_data = json.loads(web_app_data)
        print("Received web app data:", user_data)
        
        # Проверяем наличие необходимых полей
        if 'token' not in user_data or 'user' not in user_data:
            print("Missing required fields in user_data")
            return False, 'Получены неполные данные от сервера авторизации.'
        
        # Сохраняем данные пользователя
        await rq.set_user(
            tg_id=message.from_user.id,
            username=user_data['user']['name'],
            user_role=user_data['user']['role']
        )
        print(f"User data saved successfully for user {message.from_user.id}")
        
        # Устанавливаем команды в зависимости от роли
        return True, 'Авторизация успешна! Теперь вы можете использовать бота.'
            
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return False, 'Получены некорректные данные от сервера авторизации.'
    except Exception as e:
        print(f"Error in handle_web_app_data: {e}")
        return False, 'Произошла ошибка при авторизации. Попробуйте еще раз.'