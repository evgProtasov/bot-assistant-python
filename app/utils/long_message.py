from aiogram.types import CallbackQuery

async def send_long_message(message_text: str, callback: CallbackQuery, max_length: int = 4096, parse_mode: str = "HTML"):
    """
    Разделяет длинное сообщение на части и отправляет их последовательно
    """
    # Делим сообщение по переносам строк, чтобы не разрывать строки посередине
    lines = message_text.split('\n')
    current_message = ""
    
    for line in lines:
        # Если добавление новой строки превысит лимит
        if len(current_message + line + '\n') > max_length:
            # Отправляем накопленное сообщение
            if current_message:
                await callback.message.answer(current_message, parse_mode=parse_mode)
            current_message = line + '\n'
        else:
            current_message += line + '\n'
    
    # Отправляем последнее сообщение, если оно есть
    if current_message:
        await callback.message.answer(current_message, parse_mode=parse_mode)