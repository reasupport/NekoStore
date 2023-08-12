from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pricelist import pricelist_data
import config
from cachetools import TTLCache

app = Client("my_bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)
cache = TTLCache(maxsize=100, ttl=600)  # Cache with max 100 items and 10 minutes TTL

def is_owner(user_id):
    return user_id in config.OWNERS

@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Selamat datang! Silakan gunakan perintah /pricelist untuk melihat daftar harga jasa.")

@app.on_message(filters.command("pricelist"))
def pricelist_command(client, message):
    pricelist_message = "Berikut adalah daftar harga jasa:\n\n"
    for service, details in pricelist_data.items():
        label = details.get("label", "Tanpa Label")
        price = details["harga"]
        pricelist_message += f"🔹 {label}: {price}\n"

    if is_owner(message.from_user.id):
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Tambah Harga", callback_data="add_price")]]
        )
    else:
        reply_markup = None

    bot_photo = "https://example.com/path/to/bot_photo.jpg"  # Ganti dengan URL foto bot
    message.reply_photo(bot_photo, caption=pricelist_message, reply_markup=reply_markup)

@app.on_callback_query(filters.regex("add_price"))
def add_price_button(client, callback_query):
    if is_owner(callback_query.from_user.id):
        client.edit_message_text(
            callback_query.message.chat.id,
            callback_query.message.message_id,
            "Kirim format: Nama Jasa - Harga (contoh: Jasa Baru - Rp250.000)",
        )

@app.on_message(filters.text & ~filters.command("pricelist"))
def add_price(client, message):
    if is_owner(message.from_user.id) and "-" in message.text:
        service, price = message.text.split("-", 1)
        pricelist_data[service.strip()] = {"harga": price.strip()}
        cache.clear()  # Clear cache to reflect the updated pricelist
        message.reply_text(f"Jasa '{service}' telah ditambahkan dengan harga '{price}'.")
        print(pricelist_data)  # Untuk debugging, bisa dihapus di produksi

@app.on_message(filters.command("sambungkan"))
def sambungkan(client, message):
    if not is_owner(message.from_user.id):
        client.send_message(config.OWNERS[0], f"Pesan dari pengguna:\n\n{message.text}")

@app.on_message(filters.text & filters.command("id"))
def get_id(client, message):
    if message.chat.type == "private":
        message.reply_text(f"ID pengguna Anda: {message.from_user.id}")
    elif message.chat.type in ["group", "supergroup"]:
        message.reply_text(f"ID grup ini: {message.chat.id}")

app.run()
