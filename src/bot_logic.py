import telebot
import curse_word_filter
import toxicity
import setting

my_setting = setting.settings()
logger_chat = my_setting.logger_chat
special_chat = my_setting.special_chat
token = my_setting.token
toxicity_threshold = my_setting.toxicity_threshold

bot=telebot.TeleBot(token)

def check_for_ban(message):
   bot.send_message(logger_chat,validate(message))


def validate(message):
   toxicity_level = toxicity.get_toxicity_probability(message.text)
   toxicity_level_check = "Нет"

   if toxicity_level>=toxicity_threshold:
      toxicity_level_check = "Да"  
  
   profanity = "Нет"
   if curse_word_filter.check_profanity(message.text):
      profanity = "Да"  
   return "Наличие мата: " + profanity +"\nНаличие грубости: " + profanity +"\nТоксичность: " + str(round(toxicity_level*100, 2)) + "%"


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