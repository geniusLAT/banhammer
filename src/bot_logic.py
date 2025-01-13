import telebot
import conclusion
import setting
from datetime import datetime

my_setting = setting.settings()
logger_chat = my_setting.logger_chat
special_chat = my_setting.special_chat
token = my_setting.token
toxicity_threshold = my_setting.toxicity_threshold

bot=telebot.TeleBot(token)

def check_for_ban(message):
    my_conclusion = conclusion.conclusion(message, my_setting)

    user_info = f"Пользователь: {message.from_user.first_name} {message.from_user.last_name} (ID: {message.from_user.id})\n"
    user_info += f"Чат: {message.chat.title if message.chat.title else 'Личный чат'} (ID: {message.chat.id})\n"
    user_info += f"Текст сообщения: {message.text}\n"
    user_info += f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    user_info += str(my_conclusion)
    bot.send_message(logger_chat,user_info)


def validate(message):
   my_conclusion = conclusion.conclusion(message, my_setting)
   return str(my_conclusion)

@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id,"Привет ✌️ ")


@bot.message_handler(content_types='text')
def message_reply(message):
    print("msg :", message.chat.id)
    if message.chat.id == special_chat:
       check_for_ban(message)
    else:
        try:    bot.send_message(message.chat.id,validate(message),reply_to_message_id=message.id)
        except Exception as e: print(e)
bot.infinity_polling()