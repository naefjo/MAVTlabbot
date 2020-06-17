import telegram


def telegram_send(msg, mychat_id, mytoken):
    bot = telegram.Bot(token=mytoken)
    bot.sendMessage(chat_id=mychat_id, text=msg)
