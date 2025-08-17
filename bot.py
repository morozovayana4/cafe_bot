# bot.py
# pip install -r requirements.txt
import os
from collections import defaultdict
from dataclasses import dataclass
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DEV_CHAT_ID = int(os.getenv("DEV_CHAT_ID", "0"))

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# ---- Каталог ----
@dataclass(frozen=True)
class Item:
    id: str
    title: str
    price: tuple[int, int, int]  # (поцелуи, слова, укусы)
    cook_time: str
    photo: str  # URL или file_id из Telegram


CATALOG: list[Item] = [
    Item("karbonara", "Карбонара", (5,2,0), "30 минут",
         "https://www.google.com/imgres?q=%D0%9A%D0%B0%D1%80%D0%B1%D0%BE%D0%BD%D0%B0%D1%80%D0%B0&imgurl=https%3A%2F%2Fs1.eda.ru%2FStaticContent%2FPhotos%2FUpscaled%2F150525210126%2F150601174518%2Fp_O.jpg&imgrefurl=https%3A%2F%2Feda.ru%2Frecepty%2Fpasta-picca%2Fpasta-karbonara-pasta-alla-carbonara-50865&docid=uRCBgyzGRFpRDM&tbnid=-DeFgzbx1JCe1M&vet=12ahUKEwig44LQoJKPAxV_FhAIHSyvPFgQM3oECB4QAA..i&w=2152&h=1432&hcb=2&itg=1&ved=2ahUKEwig44LQoJKPAxV_FhAIHSyvPFgQM3oECB4QAA"),
    Item("burda", "Бурда", (5,0,2), "15 минут", "https://www.google.com/imgres?q=%D1%82%D0%BE%D1%80%D1%82%D0%B8%D0%BB%D0%B8%D1%8F%20%D1%81%20%D1%8F%D0%B9%D1%86%D0%BE%D0%BC%20&imgurl=https%3A%2F%2Fimg.iamcook.ru%2F2021%2Fupl%2Frecipes%2Fcat%2Fu-49f57815779d96420b7e13365e6bf512.JPG&imgrefurl=https%3A%2F%2Fwww.iamcook.ru%2Fshowrecipe%2F26396&docid=JIonqg0SVF1bbM&tbnid=0hCaSCsiwsagvM&vet=12ahUKEwjjq43ioJKPAxXSFRAIHa0sMCkQM3oECB4QAA..i&w=600&h=450&hcb=2&ved=2ahUKEwjjq43ioJKPAxXSFRAIHa0sMCkQM3oECB4QAA"),
    Item("tea", "Чай", (1,1,1), "5 минут", "https://www.google.com/imgres?q=%D1%87%D0%B0%D0%B9&imgurl=https%3A%2F%2Fpasteria.com.ua%2Fimage%2Fcache%2Fcatalog%2Fblack-1500x1125.jpg&imgrefurl=https%3A%2F%2Fpasteria.com.ua%2Fchernyj-chaj&docid=3RNZ9LSGs2-CDM&tbnid=7ZRA-aa2PLs2YM&vet=12ahUKEwjNo6DtoJKPAxWNERAIHfDYPOIQM3oECBUQAA..i&w=1500&h=1125&hcb=2&ved=2ahUKEwjNo6DtoJKPAxWNERAIHfDYPOIQM3oECBUQAA"),
    Item("dumplings", "Пельмени жареные", (7,1,1), "25 минут",
         "https://www.google.com/imgres?q=%D0%9F%D0%B5%D0%BB%D1%8C%D0%BC%D0%B5%D0%BD%D0%B8%20%D0%B6%D0%B0%D1%80%D0%B5%D0%BD%D1%8B%D0%B5&imgurl=https%3A%2F%2Fi.ytimg.com%2Fvi%2F5N9pV2W9h6w%2Fmaxresdefault.jpg&imgrefurl=https%3A%2F%2Fwww.russianfood.com%2Frecipes%2Frecipe.php%3Frid%3D172763&docid=rtY77aZSRId27M&tbnid=Qa7zF81zic73BM&vet=12ahUKEwj3hb-RoZKPAxU0AhAIHV8fCvwQM3oECBYQAA..i&w=1280&h=720&hcb=2&ved=2ahUKEwj3hb-RoZKPAxU0AhAIHV8fCvwQM3oECBYQAA"),
    Item("wother", "Вода", (1,0,1),"1 минута","https://www.google.com/imgres?q=%D0%B2%D0%BE%D0%B4%D0%B0&imgurl=https%3A%2F%2Faqualife.ru%2Fupload%2Fiblock%2F230%2F230712de973388a811758eb2e6c61926.jpg&imgrefurl=https%3A%2F%2Faqualife.ru%2Fblog%2Fpitevaya_voda_pokupaem_pravilnuyu_vodu%2F%3Fsrsltid%3DAfmBOoorDOdtTLtmX3w-hMoH2xqjJ3JXxGqPVFfZ0ea4zsZRGaUCtyBl&docid=g5QbLN3EqkPuPM&tbnid=bsdbfdWzkzJyOM&vet=12ahUKEwjkp5OEoZKPAxWqGxAIHc7uJ8sQM3oECBgQAA..i&w=800&h=532&hcb=2&ved=2ahUKEwjkp5OEoZKPAxWqGxAIHc7uJ8sQM3oECBgQAA"),
    Item("Sweet and sour chicken", "Курочка в кисло-сладком", (10,5,5),"45 минут","https://www.google.com/imgres?q=%D0%9A%D1%83%D1%80%D0%BE%D1%87%D0%BA%D0%B0%20%D0%B2%20%D0%BA%D0%B8%D1%81%D0%BB%D0%BE-%D1%81%D0%BB%D0%B0%D0%B4%D0%BA%D0%BE%D0%BC&imgurl=https%3A%2F%2Fimg1.russianfood.com%2Fdycontent%2Fimages_upl%2F432%2Fbig_431020.jpg&imgrefurl=https%3A%2F%2Fwww.russianfood.com%2Frecipes%2Frecipe.php%3Frid%3D157262&docid=faNZcc-_nlZ0OM&tbnid=JN2Q5jqS-q11BM&vet=12ahUKEwj9hJehoZKPAxXVHBAIHbDYBFoQM3oECCAQAA..i&w=673&h=449&hcb=2&ved=2ahUKEwj9hJehoZKPAxXVHBAIHbDYBFoQM3oECCAQAA"),
    Item("pasta whith chicken and mushrooms", "Паста с грибами и курицей", (11,6,1),"45 минут","https://www.google.com/imgres?q=%D0%9F%D0%B0%D1%81%D1%82%D0%B0%20%D1%81%20%D0%B3%D1%80%D0%B8%D0%B1%D0%B0%D0%BC%D0%B8%20%D0%B8%20%D0%BA%D1%83%D1%80%D0%B8%D1%86%D0%B5%D0%B9&imgurl=https%3A%2F%2Fstatic.1000.menu%2Fimg%2Fcontent-v2%2F17%2Ffb%2F46067%2Fpasta-fetuchini-kurica-s-gribami-v-slivochnom-souse_1613924997_14_max.jpg&imgrefurl=https%3A%2F%2F1000.menu%2Fmeals%2F112-7896&docid=hloaAPgq8FeVJM&tbnid=L4QihozZHuOeOM&vet=12ahUKEwiYna2zoZKPAxVVFBAIHZlFJa0QM3oECCEQAA..i&w=1437&h=960&hcb=2&ved=2ahUKEwiYna2zoZKPAxVVFBAIHZlFJa0QM3oECCEQAA"),
    Item("lasagna", "лазанья", (12,3,4), "60 минут", "https://www.google.com/imgres?q=%D0%BB%D0%B0%D0%B7%D0%B0%D0%BD%D1%8C%D1%8F&imgurl=https%3A%2F%2Fswlife.ru%2Fimage%2Fcache%2Fcatalog%2Frecipe%2F63%2F00%2F6300efa9fa984bf41f87787934cb2bcd-0x0.webp&imgrefurl=https%3A%2F%2Fswlife.ru%2Frecipes%2Flazanya&docid=KyQAt_4ZGnDO-M&tbnid=mq-GE2t7PIxKSM&vet=12ahUKEwiqvIvFoJKPAxXrQlUIHYHuOpgQM3oECBYQAA..i&w=640&h=480&hcb=2&ved=2ahUKEwiqvIvFoJKPAxXrQlUIHYHuOpgQM3oECBYQAA"),
    Item("cannelloni", "канилони", (8,2,6),"60 минут","https://www.google.com/imgres?q=%D0%BA%D0%B0%D0%BD%D0%B8%D0%BB%D0%BE%D0%BD%D0%B8&imgurl=https%3A%2F%2Fwww.patee.ru%2Fr%2Fx6%2F16%2Fd9%2F60%2F960m.jpg&imgrefurl=https%3A%2F%2Fwww.patee.ru%2Frecipes%2Fpasta%2Fview%2F%3Fid%3D1497439&docid=t60jEgcxJzu1tM&tbnid=3jEfavocLPkWvM&vet=12ahUKEwif0LPBoZKPAxX4JxAIHU5qGv8QM3oECCoQAA..i&w=960&h=640&hcb=2&ved=2ahUKEwif0LPBoZKPAxX4JxAIHU5qGv8QM3oECCoQAA"),
    Item("vegetables", "нарезанне овощи", (2,0,2),"5 минут","https://www.google.com/imgres?q=%D0%BD%D0%B0%D1%80%D0%B5%D0%B7%D0%B0%D0%BD%D0%BD%D0%B5%20%D0%BE%D0%B2%D0%BE%D1%89%D0%B8&imgurl=https%3A%2F%2Fi.ytimg.com%2Fvi%2F0y5NuEamCew%2Fhq720.jpg%3Fsqp%3D-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD%26rs%3DAOn4CLBe7KOZjZRMnyLPso1TuyPq5b3H7g&imgrefurl=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D0y5NuEamCew&docid=P6Q5XvSOhz10SM&tbnid=P31evbpWh95dSM&vet=12ahUKEwj2qtXcoZKPAxXBKBAIHUCtAqEQM3oECBwQAA..i&w=686&h=386&hcb=2&ved=2ahUKEwj2qtXcoZKPAxXBKBAIHUCtAqEQM3oECBwQAA"),
]

ITEM_BY_ID = {i.id: i for i in CATALOG}

# ---- Корзины и последние сообщения ----
carts: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
last_message: dict[int, int] = {}  # user_id -> message_id

# ---- Кнопки ----
def menu_kb() -> InlineKeyboardMarkup:
    rows = []
    for it in CATALOG:
        rows.append([InlineKeyboardButton(text=it.title, callback_data=f"show:{it.id}")])
    rows.append([InlineKeyboardButton(text="🛒 Корзина", callback_data="cart:open")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def item_kb(item_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить", callback_data=f"add:{item_id}")],
        [InlineKeyboardButton(text="⬅️ Назад к меню", callback_data="menu")]
    ])

def cart_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить ещё", callback_data="menu")],
        [
            InlineKeyboardButton(text="🧹 Очистить", callback_data="cart:clear"),
            InlineKeyboardButton(text="✅ Оформить", callback_data="cart:checkout"),
        ],
    ])

# ---- Утилиты ----
def format_price(price: tuple[int, int, int]) -> str:
    kisses, words, bites = price
    parts = []
    if kisses: parts.append(f"{kisses} поцелуй(ев)")
    if words: parts.append(f"{words} хороших(ее) слов(о)")
    if bites: parts.append(f"{bites} укус(ов) дениса")
    return " + ".join(parts) if parts else "бесплатно"

def cart_summary(user_id: int) -> tuple[str, tuple[int, int, int]]:
    cart = carts[user_id]
    if not cart:
        return "Корзина пуста.", (0, 0, 0)
    lines = ["<b>Корзина:</b>"]
    total = [0, 0, 0]
    for item_id, qty in cart.items():
        it = ITEM_BY_ID[item_id]
        cost = tuple(p * qty for p in it.price)
        total = [a + b for a, b in zip(total, cost)]
        lines.append(f"• {it.title} × {qty} — {format_price(cost)}")
    lines.append(f"\n<b>Итого:</b> {format_price(tuple(total))}")
    return "\n".join(lines), tuple(total)

async def send_unique(user_id: int, text: str = None, photo: str = None, caption: str = None, reply_markup=None):
    """Удаляет предыдущее сообщение и отправляет новое"""
    # удалить прошлое сообщение
    if user_id in last_message:
        try:
            await bot.delete_message(user_id, last_message[user_id])
        except:
            pass
    # отправить новое
    if photo:
        msg = await bot.send_photo(user_id, photo, caption=caption, reply_markup=reply_markup)
    else:
        msg = await bot.send_message(user_id, text, reply_markup=reply_markup)
    last_message[user_id] = msg.message_id

# ---- Хэндлеры ----
@dp.message(Command("start"))
async def on_start(m: Message):
    await send_unique(
        m.from_user.id,
        text=("привет. выбирай что хочешь покушать сегодня ,но учти что это не бесплано "
              "и заказ будет выполнен только если дома есть нужные продукты, "
              "у яны морозовой время не занято дедлайнами и после оплаты😉 "
              "(если в блюде есть мясо/курица ,то мне нужна будет твоя помощь)"),
        reply_markup=menu_kb()
    )

@dp.callback_query(F.data == "menu")
async def on_menu(c: CallbackQuery):
    await send_unique(c.from_user.id, text="Выбирай блюдо:", reply_markup=menu_kb())
    await c.answer()

@dp.callback_query(F.data.startswith("show:"))
async def on_show(c: CallbackQuery):
    item_id = c.data.split(":", 1)[1]
    item = ITEM_BY_ID[item_id]
    caption = (f"<b>{item.title}</b>\n"
               f"Время готовки: {item.cook_time}\n"
               f"Цена: {format_price(item.price)}")
    await send_unique(c.from_user.id, photo=item.photo, caption=caption, reply_markup=item_kb(item_id))
    await c.answer()

@dp.callback_query(F.data.startswith("add:"))
async def on_add(c: CallbackQuery):
    item_id = c.data.split(":", 1)[1]
    item = ITEM_BY_ID.get(item_id)
    if not item:
        return await c.answer("Не найдено", show_alert=True)
    carts[c.from_user.id][item_id] += 1
    await c.answer(f"Добавлено: {item.title}")

@dp.callback_query(F.data == "cart:open")
async def open_cart(c: CallbackQuery):
    text, _ = cart_summary(c.from_user.id)
    await send_unique(c.from_user.id, text=text, reply_markup=cart_kb())
    await c.answer()

@dp.callback_query(F.data == "cart:clear")
async def cart_clear(c: CallbackQuery):
    carts[c.from_user.id].clear()
    await send_unique(c.from_user.id, text="Корзина очищена.", reply_markup=menu_kb())
    await c.answer("Корзина очищена")

@dp.callback_query(F.data == "cart:checkout")
async def cart_checkout(c: CallbackQuery):
    text, total = cart_summary(c.from_user.id)
    if sum(total) == 0:
        return await c.answer("Корзина пуста", show_alert=True)
    user = c.from_user
    order_header = (
        f"🧾 <b>Новый заказ</b>\n"
        f"От: {user.full_name} (@{user.username or '—'}) • id={user.id}\n\n"
    )
    if DEV_CHAT_ID:
        await bot.send_message(DEV_CHAT_ID, order_header + text)
    await send_unique(
        c.from_user.id,
        text=f"{text}\n\n<b>Заказ отправлен!</b> "
             f"С тебя {format_price(total)} 😘",
        reply_markup=menu_kb()
    )
    carts[c.from_user.id].clear()
    await c.answer("Заказ оформлен!")

@dp.message()
async def any_text(m: Message):
    await send_unique(m.from_user.id, text="Жми кнопки, чтобы выбрать блюдо 👇", reply_markup=menu_kb())

if __name__ == "__main__":
    import asyncio
    async def main():
        assert BOT_TOKEN, "BOT_TOKEN не задан"
        await dp.start_polling(bot)
    asyncio.run(main())
