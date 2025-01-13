import telebot
import conclusion
import setting
from datetime import datetime
import time

my_setting = setting.settings()
logger_chat = my_setting.logger_chat
special_chat = my_setting.special_chat
token = my_setting.token
toxicity_threshold = my_setting.toxicity_threshold

bot=telebot.TeleBot(token)

def check_status(message):
    user_status = bot.get_chat_member(message.chat.id, message.from_user.id).status
    return user_status == 'administrator' or user_status == 'creator'


def mute_user_for(message, duration=24*60):
    user_status = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if user_status == 'administrator' or user_status == 'creator':
        bot.reply_to(message, "Невозможно замутить администратора.")
        return
    bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=time.time()+duration*60)


def check_for_ban(message):
    my_conclusion = conclusion.conclusion(message, my_setting)

    if not my_conclusion.warning:
       print("Не о чем волноваться")
       return
    
    status = check_status(message)
    user_info = f"Пользователь: {message.from_user.first_name} {message.from_user.last_name} (ID: {message.from_user.id})\n"
    user_info += f"Чат: {message.chat.title if message.chat.title else 'Личный чат'} (ID: {message.chat.id})\n"
    user_info += f"Текст сообщения: {message.text}\n"
    user_info += f"Имунитет: { 'Да'  if status else 'Нет'}\n"
    user_info += f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    user_info += str(my_conclusion)
    bot.send_message(logger_chat,user_info)

    if not status:
        mute_user_for(message)
    else:
        bot.reply_to(message, "Приговор не может быть приведён в исполнение, так как пользователь имунен к стандартной санкции")


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