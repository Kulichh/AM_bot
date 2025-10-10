import asyncio
import logging
import random

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties # <-- ВИПРАВЛЕННЯ 2 (додано імпорт)
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.markdown import hbold, hitalic

# --- ⚙️ ГОЛОВНІ НАЛАШТУВАННЯ ---
# Вставте сюди токен вашого бота
BOT_TOKEN = "8184834829:AAEojo2VZKkMMSQUC8-FEi9sbepWlsIsxq4"
# Вставте сюди ваш Chat ID, який ви отримали від @userinfobot
YOUR_CHAT_ID = "842908820"


# --- 🎨 ВІЗУАЛЬНИЙ КОНТЕНТ (тут можна все змінювати) ---

# Список компліментів
COMPLIMENTS = [
    "Твоя посмішка просто чарівна😊",
    "Ти неймовірна!!!✨",
    "Разом з тобою ппц як комфортно❤️",
    "Ти дууже добра та чуйна🥰",
    "У тебе самі самі самі красиииві очі😻",
    "ТИ МЕГАА СЛЕЕЕЙ✨",
    "Сама Афродіта заздрить тобі😉❤️",
    "Ти дуже фані і к'ют і аоаоаоаоаоаоа😫🥰"
]
# Список спогадів (текст + шлях до фото)
MEMORIES = [
    (" Ти тоді приїхала до мене на роботу🥰☀️", r"C:\Users\24art\OneDrive\Рабочий стол\telegram bot\images\1.jpg"),
    (" Ліпший перекур, який був на роботі. Бо ти тоді була зі мною😍", r"C:\Users\24art\OneDrive\Рабочий стол\telegram bot\images\2.jpg"),
    (" Наша перша спільна фотка, очінь міла🤗 ", r"C:\Users\24art\OneDrive\Рабочий стол\telegram bot\images\3.jpg"),
    (" Шашличкіі. Ну реал мілі фото😫", r"C:\Users\24art\OneDrive\Рабочий стол\telegram bot\images\4.jpg"),
    (" Перша фотка в моїй кімнаті пхпхпхха", r"C:\Users\24art\OneDrive\Рабочий стол\telegram bot\images\5.jpg"),
    (" Очінь вайб фотка, ми тоді їхали з прогулки дамой🐱🐷", r"C:\Users\24art\OneDrive\Рабочий стол\telegram bot\images\6.jpg"),
    (" Мілі рижі кіт🐱. І ти дуже мілі☺️", r"C:\Users\24art\OneDrive\Рабочий стол\telegram bot\images\7.jpg"),
    (" Свінкіі акружилі🐷", r"C:\Users\24art\OneDrive\Рабочий стол\telegram bot\images\8.jpg"),
    (" Свінкі нападают🐷🐷🐷", r"C:\Users\24art\OneDrive\Рабочий стол\telegram bot\images\9.jpg"),
    (" СОО К'ЮЮТ АООАОА💞", r"C:\Users\24art\OneDrive\Рабочий стол\telegram bot\images\10.jpg"),
    (" Наша перша повноцінна прогулка💘🌇", r"C:\Users\24art\OneDrive\Рабочий стол\telegram bot\images\11.jpg"),
    (" Красіві закат і немовірна ти, ну багіня✨", r"C:\Users\24art\OneDrive\Рабочий стол\telegram bot\images\12.jpg")
]
# Список пісень (просто текст з посиланням)
# ВИПРАВЛЕННЯ 1: Додано коми в кінці кожного рядка
SONGS = [
    "Вайб пісні, які асоціюються з тобою 1✨ -  https://open.spotify.com/track/3kUv3tKhdDP32S3p9tIEXT?si=735cf91d9d7045fa",
    "Вайб пісні, які асоціюються з тобою 2😫 -  https://open.spotify.com/track/0WtMfb2f3lsdY2fB5A5w23?si=08c2d765507e4d8e",
    "Вайб пісні, які асоціюються з тобою 3🥰 -  https://open.spotify.com/track/25Syi9wn6yR2el22t8d6v1?si=063f26de6d1544a4",
    "Вайб пісні, які асоціюються з тобою 4🤗 -  https://open.spotify.com/track/683hR7i10a1oK3a830Kq8y?si=63a7d40e947141ad",
    "Вайб пісні, які асоціюються з тобою 5😘 -  https://open.spotify.com/track/3eekarcy7kvN4yt5XYzCMi?si=aa5855f463324fec",
    "Вайб пісні, які асоціюються з тобою 6❤️ -  https://open.spotify.com/track/5NEoGoS2M2Wp2ll9e0vUaG?si=0cd43c5b81de4bb5",
    "Вайб пісні, які асоціюються з тобою 7❤️‍🔥 -  https://open.spotify.com/track/303CfhtG5IibX2i8d5P56L?si=f4841c2c36664e52",
    "Вайб пісні, які асоціюються з тобою 8💞 -  https://open.spotify.com/track/5rurgg3iS9ZRNlYk47n5C7?si=269389288e7343c9",
    "Вайб пісні, які асоціюються з тобою 9🥺 -  https://open.spotify.com/track/6aMoa0kMv9JDbI2UDdK3wz?si=c14e0475877c4441",
    "Вайб пісні, які асоціюються з тобою 10🐱 -  https://open.spotify.com/track/0WSEwT5A082j8zWbt26uHc?si=54c9d5d8866144e5",
    "Вайб пісні, які асоціюються з тобою 11😻 -  https://open.spotify.com/track/0WSEwT5A082j8zWbt26uHc?si=20e1d0f592d346ff",
    "Вайб пісні, які асоціюються з тобою 12💗 -  https://open.spotify.com/track/2tHqaT72hGn43wJ6yVR2Dr?si=0eb363914a1c430e",
    "Вайб пісні, які асоціюються з тобою 13🤯 -  https://open.spotify.com/track/3qFTడు0E8pPS6k7L9yK1g?si=6d9ec4826b52470f",
    "Вайб пісні, які асоціюються з тобою 14🫣 -  https://open.spotify.com/track/7pDaYaS3y2A2y2Su6223zT?si=ab846b0a88aa488b",
    "Вайб пісні, які асоціюються з тобою 15💘 -  https://open.spotify.com/track/25Syi9wn6yR2el22t8d6v1?si=063f26de6d1544a4",
    "Вайб пісні, які асоціюються з тобою 16💝 -  https://open.spotify.com/track/7iEx163hAXJ3z6DBh61N6K?si=867f70b7937d45d3",
    "Вайб пісні, які асоціюються з тобою 17💖 -  https://open.spotify.com/track/1a2iFwN4mv7I6i23S6bXp7?si=712f56f4d01b4c95",
]
# Список ID стікерів для подяки
THANK_YOU_STICKERS = [
    "CAACAgIAAxkBAAETBb1o6XhXdjPRlZj1pX0eBEY675j0_wAC-SUAAiH3oEjXJ5mupRpc8jYE",
    "CAACAgIAAxkBAAETBb9o6XhZbunFWWx-xMLAzEUTnV8OewACaykAAoa6oUjdta3jKo99EjYE",
    "CAACAgIAAxkBAAETBcFo6XhdqJa85OiGzSicUl_8vyDXtwACuCwAAk5GmEj8ZZrYYF7J2zYE",
    "CAACAgIAAxkBAAETBcNo6XhfESbvLlQAAd5n71TuQLg2uk8AAoIpAAJhJglJzIDT2gOARPA2BA",
    "CAACAgIAAxkBAAETBcVo6XhgV7Fd0Q0aJTa0bswnLg6fgQACBS4AAukvEEnwvH79w_7aTTYE",
    "CAACAgIAAxkBAAETBcdo6Xhi5-H59Es7Hm_BRBru0lU6YgACdSUAAk8nCUnOE4lXDm-KKzYE",
    "CAACAgIAAxkBAAETBclo6XhkL5hE5fYo3xWjRz_EYnq4AgAC9SgAAsp4eEmF44I5r2yMujYE",
    "CAACAgIAAxkBAAETBcto6XhnaXjppgABQKrTgqDSIsEMhlcAAh8qAAIo-qFJgcUCcRFDN_g2BA",
    "CAACAgIAAxkBAAETBc1o6XhzYhOOpkVJ8hBWoYEzE_HXVwACj20AAm9myUoH81D5cMm2MzYE",
    "CAACAgIAAxkBAAETBc9o6Xh0IiHNPUusPB6I_1wZWH8gkAAC-W4AAlxw-Eo_6Bsn9L_70TYE",
    "CAACAgIAAxkBAAETBdFo6Xh2tkNB1AYWLr3UiipcFTY4kwACM24AAqWf-UoDY_UaMVqHbTYE",
    "CAACAgIAAxkBAAETBdNo6Xh3gnQjdrzMUlgFx674czyhxQACM2kAAp2z-Uog10ai4V1L2jYE",
    "CAACAgIAAxkBAAETBdVo6Xh7ovrAcH3O6ZeYWSuoulBG1QACcQADPIpXGo_yzPS-YYiQNgQ",
    "CAACAgIAAxkBAAETBddo6Xh8c3KE1NxX85t6u_yYLBkxzAACPQEAAjyKVxqaoSqM3npsuzYE",
    "CAACAgIAAxkBAAETBddo6Xh8c3KE1NxX85t6u_yYLBkxzAACPQEAAjyKVxqaoSqM3npsuzYE",
    "CAACAgIAAxkBAAETBdto6XiOrbSBabEL2IQGrfFrhiHT1QAC6iAAAvPBEEisuuIWzbl9YzYE",
    "CAACAgIAAxkBAAETBd1o6XiP31nBw-qhG6yCQA9c01KUSQACizQAAotluUkzU7skPwXNATYE",
    "CAACAgIAAxkBAAETBd9o6XiV97XYLGBZl9gwMUy6uBN73QACwi8AAlEIwEkSeMh3ggABCr82BA",
    "CAACAgIAAxkBAAETBeFo6XibZdD9G-i0877JawtJCVRYKwACXzEAAmGguUkSbFAhsFIOrjYE",
    "CAACAgIAAxkBAAETBeNo6Xic4Raqp9UXx5zFyaqYsEOnqwACpjQAAocVuUkRARY4MXC2ljYE",
]

# --- Системна частина (краще не змінювати) ---
logging.basicConfig(level=logging.INFO)
# ВИПРАВЛЕННЯ 2: Змінено ініціалізацію бота на новий синтаксис
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

class UserState(StatesGroup):
    waiting_for_mood = State()
    waiting_for_wish = State()

# --- 🎬 СЦЕНАРІЙ РОБОТИ БОТА ---

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    # Створюємо красиву клавіатуру 2х2 + 1
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="😊 Як у тебе настрій?"),
                types.KeyboardButton(text="💖 Розкажи про побажання, або передай мені послання")
            ],
            [
                types.KeyboardButton(text="💌 Комплімент для тебе"),
                types.KeyboardButton(text="🖼️ Наші спільні моменти")
            ],
            [types.KeyboardButton(text="🎵 Вайб пісні")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Обирай, що тобі до душі ✨"
    )
    await message.answer(
        f"Прівєєт Анюют! ❤️\n\n"
        "Я твій особистий бот, створений, щоб дарувати тобі радість. "
        "Обирай будь-яку кнопочку нижче 👇",
        reply_markup=keyboard
    )
#
# Обробники кнопок з контентом
@dp.message(F.text == "💌 Комплімент для тебе")
async def send_compliment(message: types.Message):
    await message.answer(random.choice(COMPLIMENTS), parse_mode=None)

@dp.message(F.text == "🖼️ Наші спільні моменти")
async def send_memory(message: types.Message):
    text, photo_path = random.choice(MEMORIES)
    try:
        photo = types.FSInputFile(photo_path)
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text)
    except Exception as e:
        await message.answer("Ой, здається, я не можу знайти це фото... Але спогад все одно теплий! 🥰")
        logging.error(f"Error sending photo: {e}")

@dp.message(F.text == "🎵 Вайб пісні")
async def send_song(message: types.Message):
    await message.answer(random.choice(SONGS), parse_mode=None)

# Обробка настрою
@dp.message(F.text == "😊 Як у тебе настрій?")
async def ask_for_mood(message: types.Message, state: FSMContext):
    await message.answer("Звісно! Розкажи, як ти себе почуваєш? Що у тебе на душі?")
    await state.set_state(UserState.waiting_for_mood)

@dp.message(UserState.waiting_for_mood)
async def forward_mood_to_me(message: types.Message, state: FSMContext):
    await bot.send_message(
        YOUR_CHAT_ID,
        f"😊 {hbold('Настрій твоєї Анюти:')}\n\n"
        f"{hitalic(message.text)}"
    )
    await message.answer("Дякую, що поділилася! ❤️ Я все передав 😉")
    await bot.send_sticker(message.chat.id, sticker=random.choice(THANK_YOU_STICKERS))
    await state.clear()

# Обробка бажань
@dp.message(F.text == "💖 Розкажи про побажання, або передай мені послання")
async def ask_for_wish(message: types.Message, state: FSMContext):
    await message.answer("О, це цікаво! Чого б тобі зараз хотілося найбільше? Мрій сміливо! ✨")
    await state.set_state(UserState.waiting_for_wish)

@dp.message(UserState.waiting_for_wish)
async def forward_wish_to_me(message: types.Message, state: FSMContext):
    await bot.send_message(
        YOUR_CHAT_ID,
        f"💖 {hbold('Бажання Анюти:')}\n\n"
        f"{hitalic(message.text)}"
    )
    await message.answer("Записав! Спробую натякнути кому треба 🤫✨")
    await bot.send_sticker(message.chat.id, sticker=random.choice(THANK_YOU_STICKERS))
    await state.clear()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())