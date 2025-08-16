from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from downloader import download_twitter_video
from config import TOKEN
import os

# إنشاء التطبيق
app = ApplicationBuilder().token(TOKEN).build()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    # التحقق من صحة الرابط
    if not ("twitter.com" in url or "t.co" in url or "x.com" in url):
        await update.message.reply_text(
            "هذا الرابط غير صالح، يرجى إرسال رابط تويتر أو X صالح فقط."
        )
        return

    await update.message.reply_text("جاري تحميل الفيديو من تويتر/X... ⏳")
    
    try:
        video_file = download_twitter_video(url)
        with open(video_file, 'rb') as f:
            await update.message.reply_video(f)
        os.remove(video_file)
    except Exception as e:
        await update.message.reply_text(f"حصل خطأ أثناء التحميل: {e}")

# إضافة الهاندلر
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

# تشغيل البوت
app.run_polling()
