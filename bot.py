

import telebot
from telebot import types
import random
import time

# ТВОЙ НОВЫЙ ТОКЕН
TOKEN = '8738377976:AAEm9BXaD2JDTao_0oJ1y6C30UD7ZYflhDo'
bot = telebot.TeleBot(TOKEN)

# НАСТРОЙКИ АДМИНА
ADMIN_ID = 5765628946  
CARD_NUMBER = "414949753764" 
ADMIN_USER = "@KFGOFFICIAL" 

paid_users = [] 
user_modes = {}

# БАЗА ПРИНИЖЕНИЙ
ZLOY_BASE = [
    "Че надо, отброс? Слышь, ты зачем мои транзисторы своим тупизмом напрягаешь?",
    "Твой интеллект — это ошибка природы. Иди умойся.",
    "Ти настільки тупий, що навіть гугл тебе ігнорує, тварина.",
    "Твій мозок — як світло в Одесі: постійно вирубається."
]

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🤬 Злой (БЕСПЛАТНО)", "📱 ТикТок (VIP)", "🤖 Помощник (VIP)", "🧠 ChatGPT (VIP)")
    bot.send_message(message.chat.id, "💰 **Нейрохам UA 24/7**\n\nЗлой режим — бесплатно.\nVIP режимы — 50 грн.", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['pay'])
def activate_user(message):
    if message.from_user.id == ADMIN_ID:
        try:
            # Исправлено: берем ID после команды /pay
            target_id = int(message.text.split()[1])
            paid_users.append(target_id)
            bot.send_message(target_id, "💎 **VIP АКТИВОВАНО!** Теперь тебе всё доступно.")
            bot.reply_to(message, f"✅ Юзер {target_id} оплатил.")
        except:
            bot.reply_to(message, "Пиши: /pay 12345678")

@bot.message_handler(func=lambda message: True)
def main_logic(message):
    uid = message.from_user.id
    text = message.text

    # Проверка VIP кнопок
    if text in ["📱 ТикТок (VIP)", "🤖 Помощник (VIP)", "🧠 ChatGPT (VIP)"]:
        if uid == ADMIN_ID or uid in paid_users:
            user_modes[uid] = text
            bot.reply_to(message, f"✅ Режим змінено на {text}")
        else:
            markup = types.InlineKeyboardMarkup()
            pay_url = f"https://privat24.ua{CARD_NUMBER}%22%7D"
            markup.add(types.InlineKeyboardButton(text="💳 ОПЛАТИТИ 50 ГРН", url=pay_url))
            markup.add(types.InlineKeyboardButton(text="📩 ВІДПРАВИТИ ЧЕК", url=f"https://t.me{ADMIN_USER.replace('@', '')}"))
            
            pay_msg = f"🛑 **ДОСТУП ОБМЕЖЕНО!**\n\nКарта: `{CARD_NUMBER}`\nТвій ID: `{uid}`"
            bot.send_message(message.chat.id, pay_msg, reply_markup=markup, parse_mode="Markdown")
            return

    if text == "🤬 Злой (БЕСПЛАТНО)":
        user_modes[uid] = text
        bot.reply_to(message, "✅ Включено режим принижень.")
        return

    # Ответы по режимам
    mode = user_modes.get(uid, "🤬 Злой (БЕСПЛАТНО)")
    if "Злой" in mode:
        bot.reply_to(message, random.choice(ZLOY_BASE))
    else:
        bot.reply_to(message, f"Ти в VIP-режимі ({mode}).")

if __name__ == '__main__':
    bot.infinity_polling()
          
