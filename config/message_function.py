from config.bot_config import bot


async def delete_and_send_message(
    chat_id_message,
    message_id_message,
    text_message,
    reply_markup
):
    await bot.delete_message(chat_id=chat_id_message,
                             message_id=message_id_message)
    await bot.send_message(chat_id=chat_id_message,
                           text=text_message,
                           reply_markup=reply_markup)


# async def delete_and_send_photo():
