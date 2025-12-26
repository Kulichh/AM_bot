import asyncio
import logging
import random
# --- ІМПОРТ для планувальника ---
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.markdown import hbold, hitalic


# --- ⚙️ ГОЛОВНІ НАЛАШТУВАННЯ ---
BOT_TOKEN = "8355219437:AAH68-sozfjNbazl8PcY5Z1cwMhhHJe-12Y"
YOUR_CHAT_ID = "842908820"
GIRLFRIEND_CHAT_ID = "1201485155"


# --- 🎨 ВІЗУАЛЬНИЙ КОНТЕНТ ---
COMPLIMENTS = [
    "Твоя посмішка просто чарівна😊",
    "Ти неймовірна!!!✨",
    "Разом з тобою ппц як комфортно❤️",
    "Ти дууже добра та чуйна🥰",
    "У тебе самі самі самі красиииві очі😻",
    "ТИ МЕГАА СЛЕЕЕЙ✨",
    "Сама Афродіта заздрить тобі😉❤️",
    "Ти дуже фані і к'ют і аоаоаоаоаоаоа😫🥰",
    "Ти просто космос🚀💫",
    "Як можна бути ТАКОЮ милою?? 😭💖",
    "Естетика з Pinterest тобі заздрить 😍📸",
    "Ти ніби створена, щоб робити день кращим ☀️",
    "Без тебе якось… не то 😔",
    "Ти просто вау, без варіантів 😭",
    "Ти як затишок у людській формі 🫶",
    "Лиш одна думка про тебе викликає посмішку💗",
    "З тобою кожна мить - це хороший момент 💖",
    "Ти — найкрасивіший збіг обставин у моєму житті 💕",
    "Я не знаю, що саме у тобі таке — але ти просто аааааа 😭",
    "Кожне твоє повідомлення — як міні-свято 🎉",
    "Ти така неймовірна, що навіть дзеркало, кайфує від тебе 😭",
    "Ти виглядаєш як улюблений момент, який не хочеться закінчувати 🥹",
]

MEMORIES = [
    (" Мій улюбелний скріншот🥰☀️", "1.jpg"),
    (" Мега вайбова фотка😍", "2.jpg"),
    (" Самий неймовірний світанок, який я бачив🤗 ", "3.jpg"),
    (" Дуже люблю цю фотку😫", "4.jpg"),
    (" Вааайб✨", "5.jpg"),
    (" Випуск видався на славу 🐱", "6.jpg"),
    (" Кожне фото з тобою дуже вайбове☺️", "7.jpg"),
    (" Стратооон і ми☺️", "8.jpg"),
    (" Наша остння фотографія, поки що😸", "9.jpg"),
    (" Фотка в машиніі😋", "10.jpg"),
    (" Ще один веселий момент з випуску🤩", "11.jpg"),
]

SONGS = [
    "Вайб пісні, які асоціюються з тобою 1✨ -  https://open.spotify.com/track/5XtsfMFmpM401S6dbVaOQw?si=3b1e41a0c0854460",
    "Вайб пісні, які асоціюються з тобою 2😫 -  https://open.spotify.com/track/6lYY2HktYKpV1pUamfRlU1?si=3258f77fd3d04a14",
    "Вайб пісні, які асоціюються з тобою 3🥰 -  https://open.spotify.com/track/3dSIHREYh7yDmVrB5mX65j?si=66da79ca713a4ebf",
    "Вайб пісні, які асоціюються з тобою 4🤗 -  https://open.spotify.com/track/0R3QFfTXRPFQUoOXtqMt9S?si=07d1f25f0ecc4054",
    "Вайб пісні, які асоціюються з тобою 5😘 -  https://open.spotify.com/track/6dBUzqjtbnIa1TwYbyw5CM?si=e6744152a16a4c9f",
    "Вайб пісні, які асоціюються з тобою 6❤️ -  https://open.spotify.com/track/6RiiSy9GzSwiyDEJDiMuKe?si=9bbbd9178ca7471d",
    "Вайб пісні, які асоціюються з тобою 7❤️‍🔥 -  https://open.spotify.com/track/7h7DK2ZHIe4w0id8qkNqla?si=b317874738f649ac",
    "Вайб пісні, які асоціюються з тобою 8💞 -  https://open.spotify.com/track/3fuyYaLhZ2RoP9eWpvfP1H?si=e1721643da194ab2",
    "Вайб пісні, які асоціюються з тобою 9🥺 -  https://open.spotify.com/track/51Grh1RyUDcMBbpuyUIUHI?si=1e7bb3f8cd3145e7",
    "Вайб пісні, які асоціюються з тобою 10🐱 -  https://open.spotify.com/track/2naVfDXfwpMkftwrr6GV52?si=6844d20fd9b3476a",
    "Вайб пісні, які асоціюються з тобою 11😻 -  https://open.spotify.com/track/3JKyRgeXT4UnQms8b1bgoU?si=137da116a99a496b",
    "Вайб пісні, які асоціюються з тобою 12💗 -  https://open.spotify.com/track/1hbciWy4syeBJeWubluRoX?si=18fdffd595134a08",
    "Вайб пісні, які асоціюються з тобою 13🤯 -  https://open.spotify.com/track/3siwsiaEoU4Kuuc9WKMUy5?si=28971400581847c6",
    "Вайб пісні, які асоціюються з тобою 14🫣 -  https://open.spotify.com/track/6dOtVTDdiauQNBQEDOtlAB?si=41094bfe188f4af1",
    "Вайб пісні, які асоціюються з тобою 15💘 -  https://open.spotify.com/track/3QntMmPocNqnLoUGbVG5Jp?si=8b2875be01b4453c",
    "Вайб пісні, які асоціюються з тобою 16💝 -  https://open.spotify.com/track/0yljUudXzjVcGEoYmLB17X?si=2f099c1f35974b55",
    "Вайб пісні, які асоціюються з тобою 17💖 -  https://open.spotify.com/track/1RvUu2gyEx07HxyrNB8B3V?si=e07a2cb88de646b2",
]
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

# --- Покращене налаштування логування ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# --- Системна частина ---
session = AiohttpSession(proxy="http://proxy.server:3128")
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"), session=session)
dp = Dispatcher()

class UserState(StatesGroup):
    waiting_for_mood = State()
    waiting_for_wish = State()

# --- Middleware для логування команд ---
async def command_logger_middleware(handler, event, data):
    if isinstance(event, types.Message) and event.text:
        user_id = event.from_user.id
        user_name = event.from_user.first_name
        command_text = event.text
        try:
            is_girlfriend = (user_id == int(GIRLFRIEND_CHAT_ID))
            who = "Дівчина" if is_girlfriend else "Інший користувач"
        except (ValueError, TypeError):
            who = "Невідомий користувач"
        logging.info(f"Користувач '{who}' ({user_name}, ID: {user_id}) виконав команду: '{command_text}'")
    return await handler(event, data)

# --- Реєстрація Middleware ---
dp.message.middleware(command_logger_middleware)


# --- Щоденний комплімент ---
async def send_daily_compliment():
    try:
        compliment_text = random.choice(COMPLIMENTS)
        await bot.send_message(chat_id=GIRLFRIEND_CHAT_ID, text=compliment_text)
        await bot.send_message(chat_id=YOUR_CHAT_ID, text=f"✅ Щоденний комплімент успішно надіслано:\n\n_{compliment_text}_")
        logging.info(f"Sent daily compliment to {GIRLFRIEND_CHAT_ID}")
    except Exception as e:
        await bot.send_message(chat_id=YOUR_CHAT_ID, text=f"❌ Не вдалося надіслати щоденний комплімент. Помилка: {e}")
        logging.error(f"Failed to send daily compliment: {e}")

# --- СЦЕНАРІЙ РОБОТИ БОТА ---
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
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
        f"Привііт! ❤️\n\n"
        "Я твій особистий бот, створений, щоб дарувати тобі радість. "
        "Обирай будь-яку кнопочку нижче 👇",
        reply_markup=keyboard
    )

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
        logging.error(f"Error sending photo '{photo_path}': {e}")

@dp.message(F.text == "🎵 Вайб пісні")
async def send_song(message: types.Message):
    await message.answer(random.choice(SONGS), parse_mode=None)

@dp.message(F.text == "😊 Як у тебе настрій?")
async def ask_for_mood(message: types.Message, state: FSMContext):
    await message.answer("Звісно! Розкажи, як ти себе почуваєш? Що у тебе на душі?")
    await state.set_state(UserState.waiting_for_mood)

@dp.message(UserState.waiting_for_mood)
async def forward_mood_to_me(message: types.Message, state: FSMContext):
    await bot.send_message(YOUR_CHAT_ID, f"😊 {hbold('Настрій Алли:')}\n\n{hitalic(message.text)}")
    await message.answer("Дякую, що поділилася! ❤️ Я все передав 😉")
    await bot.send_sticker(message.chat.id, sticker=random.choice(THANK_YOU_STICKERS))
    await state.clear()

@dp.message(F.text == "💖 Розкажи про побажання, або передай мені послання")
async def ask_for_wish(message: types.Message, state: FSMContext):
    await message.answer("О, це цікаво! Чого б тобі зараз хотілося найбільше? Мрій сміливо! ✨")
    await state.set_state(UserState.waiting_for_wish)

@dp.message(UserState.waiting_for_wish)
async def forward_wish_to_me(message: types.Message, state: FSMContext):
    await bot.send_message(YOUR_CHAT_ID, f"💖 {hbold('Бажання Алли:')}\n\n{hitalic(message.text)}")
    await message.answer("Записав! Спробую натякнути кому треба 🤫✨")
    await bot.send_sticker(message.chat.id, sticker=random.choice(THANK_YOU_STICKERS))
    await state.clear()

# --- ТИМЧАСОВА ФУНКЦІЯ: Перегляд стікера по ID ---
@dp.message(F.text.startswith("CAAC"))
async def preview_sticker(message: types.Message):
    try:
        await message.answer_sticker(sticker=message.text)
    except Exception:
        await message.answer("❌ Це неправильний ID стікера.")

# --- Запуск бота разом з планувальником ---
async def main():
    scheduler = AsyncIOScheduler(timezone="Europe/Kiev")
    scheduler.add_job(send_daily_compliment, 'cron', hour=21, minute=40)
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
