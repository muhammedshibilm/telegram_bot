from telegram import  Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes , MessageHandler , filters
from collections import defaultdict
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
app = ApplicationBuilder().token(BOT_TOKEN).build()
bad_words = {
    "idiot", "fool", "dumb", "stupid", "moron", "loser", "nonsense", "shut up",
    "trash", "garbage", "suck", "hate you", "dumbass", "freak", "bastard", "jerk",
    "noob", "scum", "lame", "screw you", "retard", "ugly", "kill yourself", "fat",
    "worthless", "asshole", "shit", "damn", "hell", "bitch", "crap", "fuck", "suck",
    "piss", "dick", "cock", "whore", "slut", "cunt", "nigger", "nigga", "gay", "lesbian",
    "terrorist", "islamist", "homo", "tranny", "faggot", "retarded"
}

#track warning per user
user_warning = defaultdict(int)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👮 I will monitor this group for bad language and take action!")

async def handle_message(update: Update,context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(f"Your said {user_message}")

async def moderation_handler(update: Update,context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.lower()
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    print(user_warning)
    if any(bad_word in message for bad_word in bad_words):
        try:
            await update.message.delete()
        except Exception as e:
            print(e)
        
        user_warning[user_id] += 1
        print(user_warning)

        if user_warning[user_id] == 1 :
            await context.bot.send_message(chat_id,f"⚠️ Warning to {update.message.from_user.first_name}: Inappropriate language is not allowed!")
        if user_warning[user_id] >= 2 :
            try:
                await context.bot.ban_chat_member(chat_id=chat_id,user_id=user_id)
                await context.bot.send_message(chat_id, f"🚫 {update.message.from_user.first_name} has been banned for repeated violations.")
            except Exception as e:
                print(e)

async def warnings(update: Update,context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user = message.from_user
    count = user_warning.get(user.id,0)
    await message.reply_text(f"⚠️ You currently have {count} warning(s).")

app.add_handler(CommandHandler("start",start))
app.add_handler(MessageHandler(
    filters.TEXT & ~filters.COMMAND ,  moderation_handler
))
app.add_handler(CommandHandler("warnings",warnings))


app.run_polling()