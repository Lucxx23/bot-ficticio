import os
import replicate
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
REPLICATE_TOKEN = os.environ.get("REPLICATE_API_TOKEN")
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot listo. Usa /soy_mayor y luego /generar tu idea")

async def soy_mayor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mayor"] = True
    await update.message.reply_text("Verificado. Ya puedes usar /generar")

async def generar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("mayor"):
        await update.message.reply_text("Primero /soy_mayor")
        return
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("Escribe algo. Ej: /generar chica ficticia adulta en cafeteria")
        return
    await update.message.reply_text("Generando...")
    try:
        output = replicate.run("stability-ai/sdxl:7762fd07cf82c948538e41f9549336b25d9b23", input={"prompt": prompt + ", adult fictional character"})
        await update.message.reply_photo(photo=output[0])
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("soy_mayor", soy_mayor))
app.add_handler(CommandHandler("generar", generar))
app.run_polling()
