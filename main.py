import telebot
from telebot import types
import google.generativeai as genai

# --- ТВОЇ ДАНІ (ВСТАВ ТУТ) ---
TOKEN = "8550952945:AAE4Dp2qqL-Atwag-B4I7DUDNSL2Eub2MQc"
GEMINI_KEY = "AIzaSyBCmXCposxwTnDci9SRNeztcGZHGr4xM8M"

# Налаштування ШІ з твоєю роллю
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="Ти — Senior Python Developer та топовий аналітик PUBG Mobile. Твоя база — 50+ про-гравців (OldBoy, Tizak, Paraboy тощо). Ти не видаєш стандартні значення. Кожну цифру ти вираховуєш математично як 'Золоту середину' під конкретний девайс та режим. Твоя відповідь — це закон для гравця."
)

bot = telebot.TeleBot(TOKEN)
user_selections = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_selections[message.chat.id] = {"device": "iPhone 14 Pro Max", "fingers": "5", "mode": "БЕЗ ВІДДАЧІ"}
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📱 Змінити пристрій", callback_data="change_dev"),
        types.InlineKeyboardButton("🎯 Режим: БЕЗ ВІДДАЧІ", callback_data="change_mode"),
        types.InlineKeyboardButton("🔥 РОЗРАХУВАТИ (OLD BOY LOGIC)", callback_data="calc")
    )
    bot.send_message(message.chat.id, "💎 **PUBG AI ANALYST v2.0**\nНалаштовано за твоїм промтом. Готовий до розрахунку.", parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "calc":
        bot.answer_callback_query(call.id, "🧠 Математичний розрахунок запущено...")
        data = user_selections[call.message.chat.id]
        
        # Твій промт, який іде прямо в мозок ШІ
        final_prompt = f"""
        АНАЛІЗУЙ:
        Пристрій: {data['device']}
        Пальці: {data['fingers']}
        Режим: {data['mode']}
        
        ЗАВДАННЯ:
        - Використовуй базу 50+ гравців.
        - Зроби розрахунок 'Без віддачі' (пріоритет на вертикальну стабільність).
        - Видай: Чутливість камери, ADS, Гіроскоп та Просунуті налаштування (M416/AKM).
        - БЕЗ СТАНДАРТНИХ ПАРАМЕТРІВ. Тільки вирахувана середня.
        """
        
        response = model.generate_content(final_prompt)
        bot.send_message(call.message.chat.id, response.text, parse_mode="Markdown")

bot.polling(none_stop=True)
