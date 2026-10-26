import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiohttp import web

# 🔑 Bot tokeningizni kiriting
BOT_TOKEN = os.getenv("BOT_TOKEN", "SIZNING_BOT_TOKENINGIZ")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 📋 8 Ta Koordinator va ularning sinflari ko'rsatilgan ma'lumotlar
COORDINATORS_DATA = {
    "coord_talim": """
<b>🎓 TAʼLIM YOʻNALISHI</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>👤 Koordinator:</b> ABDURAZZAKOVA MUSLIMA
<b>🏫 Sinfi:</b> 11-“A” sinf
<b>📌 Sohasi:</b> Taʼlim koʻrsatkichlari, oʻquv-metodik jarayonlar va akadem yetakchilik

<b>📜 UMUMIY TAVSIF:</b>
<i>Abdurazzakova Muslima taʼlim jarayonini zamonaviy pedagogik texnologiyalar, raqamli vositalar hamda individual yondashuv asosida tashkil etuvchi mutaxassisdir.</i>

<b>🎯 ASOSIY VAZIFALARI:</b>
• <b>Sifatli taʼlim jarayoni:</b> Oʻquv dasturlari va metodik rejalarni zamonaviy talablar asosida shakllantirish.
• <b>Raqamli taʼlim:</b> Darslarda AKT va raqamli platformalar imkoniyatlaridan samarali foydalanish.
• <b>Monitoring:</b> Oʻquvchilarning oʻzlashtirish darajasini tahlil qilish va obyektiv baholash.
""",
    "coord_at": """
<b>💻 AXBOROT TEXNOLOGIYALARI (AT)</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>👤 Koordinator:</b> TURGANOV ABDURAUF
<b>🏫 Sinfi:</b> 9-“A” sinf
<b>📌 Sohasi:</b> Axborot texnologiyalari, texnik taʼminot va raqamli infratuzilma

<b>📜 UMUMIY TAVSIF:</b>
<i>Turganov Abdurauf zamonaviy axborot texnologiyalari infratuzilmasini boshqarish hamda raqamlashtirish jarayonlariga masʼul mutaxassisdir.</i>

<b>🎯 ASOSIY VAZIFALARI:</b>
• <b>Texnik ta'minot:</b> Kompyuterlar va periferik qurilmalarni soz holatda tutish.
• <b>Tarmoq va internet:</b> LAN, Wi-Fi va internet tarmogʻining uzluksiz hamda xavfsiz ishlashini taʼminlash.
• <b>Dasturiy xizmat:</b> Elektron kundaliklar va maxsus platformalarni sozlash.
""",
    "coord_lider": """
<b>🌟 KELAJAK LIDERI YOʻNALISHI</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>👤 Koordinator:</b> MAXMUTOVA FARANGIZ
<b>🏫 Sinfi:</b> 11-“A” sinf
<b>📌 Sohasi:</b> Yoshlar yetakchiligi, tashabbuskorlik va ijtimoiy loyihalar

<b>📜 UMUMIY TAVSIF:</b>
<i>Maxmutova Farangiz zamonaviy fikrlaydigan, tashabbuskor va jamoani ergashtira oladigan yoshlar yetakchisidir.</i>

<b>🎯 ASOSIY VAZIFALARI:</b>
• <b>Loyiha boshqaruvi:</b> Yangi gʻoyalarni ilgari surish, intellektual oʻyinlar va tanlovlar oʻtkazish.
• <b>Jamoaviy hamjihatlik:</b> Tengdoshlar oʻrtasida oʻzaro ishonch va samimiy muhitni shakllantirish.
• <b>Samarali muloqot:</b> Jamoat tashkilotlari hamda oʻquvchilar oʻrtasida koʻprik boʻlish.
""",
    "coord_sport": """
<b>⚽ SPORT VA SOGʻLOM TURMUSH TARZI</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>👤 Koordinator:</b> ABDURASULOV SARDOR
<b>🏫 Sinfi:</b> 9-“A” sinf
<b>📌 Sohasi:</b> Sport, jismoniy tarbiya va ommaviy tadbirlar

<b>📜 UMUMIY TAVSIF:</b>
<i>Abdurasulov Sardor jismoniy faollikni targʻib qiluvchi hamda sport musobaqalarini yuqori saviyada tashkil etuvchi mutaxassisdir.</i>

<b>🎯 ASOSIY VAZIFALARI:</b>
• <b>Musobaqalar:</b> Futbol, voleybol, basketbol va boshqa sport turlari boʻyicha bellashuvlar oʻtkazish.
• <b>Sogʻlom turmush:</b> Yoshlarni sportga jalb qilish va badantarbiya mashgʻulotlarini tashkil etish.
• <b>Iqtidorlarni saralash:</b> Musobaqalar uchun iqtidorli sportchilarni tayyorlash.
""",
    "coord_eko": """
<b>🌿 EKOLOGIYA VA ATROF-MUHIT</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>👤 Koordinator:</b> ABDUNIGMANOVA ZARINA
<b>🏫 Sinfi:</b> 11-“A” sinf
<b>📌 Sohasi:</b> Ekologiya, atrof-muhit barqarorligi va yashil tashabbuslar

<b>📜 UMUMIY TAVSIF:</b>
<i>Abdunigmanova Zarina atrof-muhitni muhofaza qilish hamda yashil loyihalarni tatbiq etishga masʼul mutaxassisdir.</i>

<b>🎯 ASOSIY VAZIFALARI:</b>
• <b>Eko-aksiyalar:</b> "Yashil makon" hamda obodonlashtirish ishlarini rejalashtirish.
• <b>Targʻibot:</b> Suv va elektr energiyasini tejash hamda tabiatni asrashni targʻib qilish.
• <b>Koʻkalamzorlashtirish:</b> Bino va hovli hududlarida yashil burchaklar barpo etish.
""",
    "coord_madaniyat": """
<b>🎭 MADANIYAT VA MAʼNAVIYAT</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>👤 Koordinator:</b> ZOKIROVA LAYLO
<b>🏫 Sinfi:</b> 9-“B” sinf
<b>📌 Sohasi:</b> Madaniyat, maʼnaviy-maʼrifiy ishlar va milliy qadriyatlar

<b>📜 UMUMIY TAVSIF:</b>
<i>Zokirova Laylo jamoada madaniyat va sanʼatga boʻlgan qiziqishni oshirishga masʼul mutaxassisdir.</i>

<b>🎯 ASOSIY VAZIFALARI:</b>
• <b>Bayramlar va kechalar:</b> Milliy va umumxalq bayramlariga bagʻishlangan badiiy tadbirlar oʻtkazish.
• <b>Ijodiy koʻmak:</b> Musiqa, teatr va sanʼatga qiziqqan yoshlarni qoʻllab-quvvatlash.
• <b>Kitobxonlik:</b> Adabiy kechalar va kitobxonlik tanlovlarini tashkil etish.
""",
    "coord_fan": """
<b>🔬 FAN VA TAʼLIM YOʻNALISHI</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>👤 Koordinator:</b> ODILOVA OYDIN
<b>🏫 Sinfi:</b> 11-“G” sinf
<b>📌 Sohasi:</b> Ilmiy-tadqiqot ishlari, fan olimpiadalari va intellektual salohiyat

<b>📜 UMUMIY TAVSIF:</b>
<i>Odilova Oydin oʻquvchilarning ilmiy va intellektual salohiyatini oshirishga masʼul mutaxassisdir.</i>

<b>🎯 ASOSIY VAZIFALARI:</b>
• <b>Olimpiadalar:</b> Fanlar boʻyicha maktab olimpiadalarini tashkil etish va iqtidorlarni saralash.
• <b>Intellektual klublar:</b> "Zakovat" va ilmiy toʻgaraklar faoliyatini yoʻlga qoʻyish.
• <b>Ilmiy loyihalar:</b> Yoshlarning startap va ilmiy izlanishlarini qoʻllab-quvvatlash.
""",
    "coord_media": """
<b>📸 MEDIA VA AXBOROT XIZMATI</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>👤 Koordinator:</b> NUSRATULLAEV SARDOR
<b>🏫 Sinfi:</b> 8-“V” sinf
<b>📌 Sohasi:</b> Media, axborot tarqatish, kontent yaratish va PR

<b>📜 UMUMIY TAVSIF:</b>
<i>Nusratullaev Sardor tashkilot va maktab hayotini keng jamoatchilikka sifatli yoritib boruvchi media mutaxassisdir.</i>

<b>🎯 ASOSIY VAZIFALARI:</b>
• <b>Foto va Video:</b> Barcha tadbirlarni yuqori sifatli foto va videolarga muhrlash.
• <b>Ijtimoiy tarmoqlar:</b> Telegram, Instagram va YouTube sahifalarini yuritish.
• <b>Kontent va Montaj:</b> Qiziqarli reels, videokliplar montaj qilish hamda dizaynlar tayyorlash.
""",
}


# 🔘 Xabar ostidagi Inline-tugmalar
def get_inline_keyboard():
  builder = InlineKeyboardBuilder()
  builder.button(text="🎓 TAʼLIM", callback_data="coord_talim")
  builder.button(text="💻 AT (IT)", callback_data="coord_at")
  builder.button(text="🌟 KELAJAK LIDERI", callback_data="coord_lider")
  builder.button(text="⚽ SPORT", callback_data="coord_sport")
  builder.button(text="🌿 EKOLOGIYA", callback_data="coord_eko")
  builder.button(text="🎭 MADANIYAT", callback_data="coord_madaniyat")
  builder.button(text="🔬 FAN", callback_data="coord_fan")
  builder.button(text="📸 MEDIA", callback_data="coord_media")
  builder.adjust(2, 2, 2, 2)
  return builder.as_markup()


# ⌨️ Pastdagi Reply-tugmalar
def get_reply_keyboard():
  builder = ReplyKeyboardBuilder()
  builder.button(text="📋 Koordinatorlar ro'yxati")
  builder.button(text="👤 Bot Egasi")
  builder.button(text="⚡ Tizim Holati")
  builder.adjust(2, 1)
  return builder.as_markup(resize_keyboard=True)


# 🚀 /start buyrug'i
@dp.message(Command("start"))
async def start_handler(message: types.Message):
  welcome_text = (
      "🛡 **MAKTAB TIZIMIGA XUSH KELIBSIZ!** ⚡\n\n"
      "Qurilmangiz va yoʻnalishlarni professional darajada boshqarish uchun "
      "quyidagi boʻlimlardan birini tanlang yoki pastdagi tugmalardan foydalaning: 👇"
  )
  await message.answer(
      welcome_text,
      parse_mode=ParseMode.HTML,
      reply_markup=get_reply_keyboard(),
  )
  await message.answer(
      "👇 **Koʻordinator yoʻnalishini tanlang:**",
      reply_markup=get_inline_keyboard(),
  )


# 👤 "Bot Egasi" tugmasi bosilganda
@dp.message(F.text == "👤 Bot Egasi")
async def owner_card_handler(message: types.Message):
  card_text = (
      "абдурауф 🖤👑\n"
      "👤 **BOT EGASI**\n\n"
      "👑 **RASMIY DASTURCHI KARTOCHKASI** ⚡\n\n"
      "👤 Bot Egasi & Creator: 🏆\n"
      "<b>abdurauf_7</b>\n"
      "🛠 <b>Tizim versiyasi:</b> Maktab Koordinator PRO v3.5\n"
      "🌐 <b>Status:</b> Online & Secure (24/7)\n"
      "🟢\n\n"
      "✨ **Xavfsizligingiz — bizning ustuvor vazifamiz!**"
  )
  await message.answer(card_text, parse_mode=ParseMode.HTML)


# 📋 "Koordinatorlar ro'yxati" tugmasi bosilganda
@dp.message(F.text == "📋 Koordinatorlar ro'yxati")
async def list_handler(message: types.Message):
  await message.answer(
      "👇 Kerakli yoʻnalishni tanlang:", reply_markup=get_inline_keyboard()
  )


# ⚡ "Tizim Holati" tugmasi bosilganda
@dp.message(F.text == "⚡ Tizim Holati")
async def status_handler(message: types.Message):
  await message.answer(
      "🟢 **Tizim holati:** Ayni paytda barcha 8 ta koordinator tizimi 24/7"
      " rejimida barqaror ishlamoqda!",
      parse_mode=ParseMode.HTML,
  )


# 👆 Inline tugmalar bosilganda koordinator ma'lumotini chiqarish
@dp.callback_query(F.data.startswith("coord_"))
async def coordinator_info_handler(callback: types.CallbackQuery):
  coord_key = callback.data
  if coord_key in COORDINATORS_DATA:
    info_text = COORDINATORS_DATA[coord_key]
    await callback.message.answer(info_text, parse_mode=ParseMode.HTML)
    await callback.answer()


# 🌐 Render 24/7 uchun mini web-server
async def handle_ping(request):
  return web.Response(text="Bot 24/7 active!")


async def main():
  app = web.Application()
  app.router.add_get("/", handle_ping)
  runner = web.AppRunner(app)
  await runner.setup()
  port = int(os.environ.get("PORT", 8080))
  site = web.TCPSite(runner, "0.0.0.0", port)
  await site.start()

  print("Bot 24/7 rejimida ishga tushdi...")
  await dp.start_polling(bot)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  asyncio.run(main())
