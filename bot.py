from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters, CommandHandler
import yt_dlp

# ضع التوكن في ملف config.py في نفس المجلد
# config.py يجب أن يحتوي:
# TOKEN = "ضع التوكن هنا"
from config import TOKEN  

# إنشاء التطبيق
app = ApplicationBuilder().token(TOKEN).build()

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً! أرسل لي رابط تويتر/X وسأرسل لك الفيديو مباشرة."
    )

# التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if not ("twitter.com" in url or "x.com" in url):
        await update.message.reply_text("❌ هذا الرابط غير صالح.")
        return

    await update.message.reply_text("⏳ جاري تحميل الفيديو...")

    ydl_opts = {
        "format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "skip_download": True,  # مهم: لا يحفظ الفيديو على الجهاز
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info['url']

        # إرسال الفيديو مباشرة من الرابط
        await update.message.reply_video(video_url)
    except Exception as e:
        await update.message.reply_text(f"⚠️ حدث خطأ أثناء التحميل: {e}")

# إضافة الهاندلرات
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

# إعداد أمر البوت
async def set_commands():
    await app.bot.set_my_commands([
        BotCommand("start", "بدء الاستخدام وشرح عمل البوت")
    ])

# تشغيل البوت
if __name__ == "__main__":
    import asyncio
    asyncio.get_event_loop().run_until_complete(set_commands())
    print("🚀 Bot is running...")
    app.run_polling()
