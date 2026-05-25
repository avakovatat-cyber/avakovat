import telebot
from telebot import types
import os

# Ваши данные
TOKEN = "8099979681:AAGnyA98CziAWiabc-klfuFrjHx73giQ3Mc"
CHANNEL_ID = -1003945323384
GUIDE_LINK = "https://docs.google.com/document/d/1-AeXsaAjhx8VO7wtieSrT8kUtimRREF2_lpLeUo9tAU/edit?tab=t.0"
CHANNEL_LINK = "https://t.me/nabase_money"

bot = telebot.TeleBot(TOKEN)

# Проверка подписки
def check_subscription(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Ошибка проверки подписки: {e}")
        return False

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    subscribe_btn = types.InlineKeyboardButton("📢 Подписаться на канал", url=CHANNEL_LINK)
    check_btn = types.InlineKeyboardButton("✅ Проверить подписку", callback_data="check")
    keyboard.add(subscribe_btn)
    keyboard.add(check_btn)
    
    bot.send_message(
        message.chat.id,
        "👋 Привет!\n\n"
        "Чтобы получить бесплатный гайд, подпишись на наш канал и нажми кнопку проверки:",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: call.data == "check")
def check_sub(call):
    if check_subscription(call.from_user.id):
        bot.send_message(
            call.message.chat.id,
            f"🎉 Отлично! Ты подписан!\n\n"
            f"Вот твой гайд:\n{GUIDE_LINK}\n\n"
            f"Приятного чтения! 📚"
        )
        bot.answer_callback_query(call.id, "✅ Доступ получен!")
    else:
        bot.answer_callback_query(
            call.id, 
            "❌ Ты ещё не подписан на канал! Подпишись и нажми кнопку снова.", 
            show_alert=True
        )

print("✅ Бот успешно запущен!")
bot.polling(none_stop=True)
