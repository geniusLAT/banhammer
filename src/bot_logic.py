import telebot
import conclusion
import setting
from ban_time_manager import UserTracker
from datetime import datetime, timedelta
import time

my_setting = setting.settings()
logger_chat = my_setting.logger_chat
special_chat = my_setting.special_chat
token = my_setting.token
toxicity_threshold = my_setting.toxicity_threshold



tracker = UserTracker(f"{special_chat}_ban_time.json")

days = tracker.get_user_days(463234260)
print(days)

bot=telebot.TeleBot(token)

bot_name = bot.get_me().username
bot_tag = f"@{bot_name}"

def check_status(message):
    user_status = bot.get_chat_member(message.chat.id, message.from_user.id).status
    return user_status == 'administrator' or user_status == 'creator'

def next_midnight():
    now = datetime.now()
    midnight_today = datetime(now.year, now.month, now.day)
    if now >= midnight_today:
        midnight_today += timedelta(days=1)
    
    return midnight_today

def mute_user_for(message, duration_in_days=1):
    user_status = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if user_status == 'administrator' or user_status == 'creator':
        bot.reply_to(message, "Невозможно замутить администратора.")
        return

    
    bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=next_midnight()+timedelta(days=duration_in_days))

def mute_user(message):
    ban_time = choose_ban_time(message)
    mute_user_for(message, ban_time)
    tracker.update_user(message.from_user.id, ban_time)
    return ban_time

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

    reply_message = get_conclusion_message(my_conclusion)
    if not status:
        ban_time = mute_user(message)
        reply_message += f"\nМьют выдан на {ban_time} дней"
        
    else:
        return
        reply_message += f"\n Приговор не может быть приведён в исполнение, так как пользователь имунен к стандартной санкции"
        
    bot.reply_to(message, reply_message)


def validate(message):
   my_conclusion = conclusion.conclusion(message, my_setting)
   return str(my_conclusion)

def choose_ban_time(message) ->int:
    last_ban_time = tracker.get_user_days(message.from_user.id)
    if last_ban_time == 0:
        return 1
    return last_ban_time*2

def get_conclusion_message(my_conclusion: conclusion.conclusion ):
    return str(my_conclusion)

@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id,"Привет ✌️ ")

def check_for_command(message):
    status = check_status(message)
    if message.reply_to_message == None:
        return
    if not status:
        return
    
    if message.text.startswith('/ban'):
        ban_time = mute_user( message.reply_to_message)
        bot.reply_to(message.reply_to_message, f"Забанен администратором на {ban_time} дней")
        return
    if message.text.startswith('/set_ban'):
        words = message.text.split(" ")
        days=0
        if len(words) <2:
            bot.reply_to(message, f"Неверный синтаксис. \nПример: /set_ban 10")
            return
        try:
            days = int(words[1])
        except:
            bot.reply_to(message, f"Неверный синтаксис. \n {words[1]} не является целым числом \nПример: /set_ban 10")
            return
        tracker.update_user(message.reply_to_message.from_user.id,days)
        bot.reply_to(message, f"Время последнего бана перезаписано для {message.reply_to_message.from_user.username} на {days} дней")
        return
    if message.text.startswith('/unban'):
        chat_id = special_chat
        user_id = message.reply_to_message.from_user.id
        bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
        bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} реабилитирован.")
        days  = tracker.get_user_days(user_id)
        tracker.update_user(user_id,int(days/2))
       


@bot.message_handler(content_types='text')
def message_reply(message):
    print("msg :", message.chat.id)
    if message.chat.id == special_chat:
       check_for_ban(message)
    else:
        try:    bot.send_message(message.chat.id,validate(message),reply_to_message_id=message.id)
        except Exception as e: print(e)
    try:
        check_for_command(message)
    except Exception as e: print(e)
bot.infinity_polling()