import asyncio
import logging
import config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook
from aiogram.types.message import ContentType
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import requests
import pickle
import feedparser

# webhook settings
WEBHOOK_PATH = '/'
WEBHOOK_URL = "https://www.uchenikoff.ru/AAAA/"

# webserver settings
WEBAPP_HOST = '127.0.0.1'  # or ip
WEBAPP_PORT = 7772

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(config.token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

feed_list =["https://schzg719.mskobr.ru/data/rss", "https://www.youtube.com/feeds/videos.xml?channel_id=UCv9aT7dS9XEN1N7qU0gWNOA",
            ]
last_feeds = pickle.load(open("db.p", 'rb'))
fee_links = []
users=[]
admin=91440724
c=()

class ZadStatus(StatesGroup):
	vzad = State()
	zad = State()
	pereslat = State()

def get_users():
	global users
	f = open('users', 'r')
	m=(f.read())
	users=m.split(' ')
	f.close()
	users.pop()
		
get_users()
		
@dp.message_handler(commands=["start"])
async def start(message):
	global users
	global c
	global admin
	username=message.from_user.first_name #запоминаем имя пользователя
	f = open('users', 'a') #открываем доступ к файлу на дозапись значений
	if str(message.chat.id) not in users: #проверяем чтобы не было повторов
			f.write(str(message.chat.id)+ ' ') #записать тех кто нажал старт
			await bot.send_message(admin, "Новый пользователь " + str(message.chat.id) + ' ' + message.from_user.first_name)
	f.close()
	get_users()
	if message.chat.id==admin:
		c=ad_mainmenu
	else:
		c=mainmenu
	await bot.send_chat_action(message.chat.id, 'typing')
	await asyncio.sleep(1)
	await bot.send_sticker(message.chat.id, 'CAADAgADa1kAAp7OCwABtPtscVkaOGoWBA')
	await bot.send_message(message.chat.id, "Рады приветсвовать " + username + " в нашем боте помошнике. \n Вы автоматически подписаны на обновления новостей нашего сайта и некоторых соц.сетей. ДЛя остановки подписки используйте команду /stop, для повтора подписки используйте команду /start. А еще нашего бота можно добавить в группу, сделать администратором и он будет посылать новости в группу.", reply_markup=c)

#@bot.message_handler(commands=["stop"])
#def stop(message):
#	global users
#	global c
#	username=message.from_user.first_name #запоминаем имя пользователя
#	f = open('users', 'r')
#	m=(f.read())
#	m=m.replace(str(message.chat.id) + ' ', '')
#	f.close()
#	f = open('users', 'w') #открываем доступ к файлу на запись
#	f.writelines(m)
#	f.close()
#	bot.send_message(admin, "Пользователь отписался " + str(message.chat.id) + ' ' + message.from_user.first_name)
#	get_users()
		
@dp.message_handler(commands=['pereslat'], state="*") #реакция на команду pereslat
async def pereslat(message: types.Message):
	global admin
	if message.chat.id == admin:
		await bot.send_message(message.chat.id, text="Готов принять послание", reply_markup=keyboard3)
		await ZadStatus.pereslat.set()
    
@dp.message_handler(state=ZadStatus.pereslat, content_types=types.ContentTypes.ANY)
async def pereslat2(message: types.Message, state: FSMContext):
	global users
  	if message.chat.id==admin:
		c=ad_mainmenu
	else:
		c=mainmenu
	if message.text=="❌ОТМЕНА":
		await message.answer("ОХРАНА! ОТМЕНА!", reply_markup=c)
		await state.finish()
	else:
		get_users()
		for i in users: #перебираем пользователей по массиву
			await bot.forward_message(i, admin, message.message_id) #форвордим послание
			await asyncio.sleep(1)
		await message.reply("Послание отправлено.", reply_markup=c)
		await state.finish()
	
@dp.message_handler(content_types=['text'], state="*")
async def main(message: types.Messag):  # главное меню
	global c
	cousers=0
	cugrup=0
	global users
	if message.text == "Привет" or message.text == "🏫Главное меню" or message.text == "/main" or message.text == "/start":
		await start(message)
	elif message.text == "🗓Расписание":
		await bot.send_chat_action(message.chat.id, 'typing')
		await asyncio.sleep(1)
		await bot.send_sticker(message.chat.id, 'CAADAgADglkAAp7OCwABF1LyypVAYq0WBA')
		await bot.send_message(message.chat.id, text="Расписание \n [Ссылка](https://t.me/iv?url=https%3A%2F%2Fschzg719.mskobr.ru%2Finfo_add%2Fraspisanie-urokov&rhash=b48987ea0be3c5)", reply_markup=mainmenu, parse_mode='Markdown')
	elif message.text == "🖋Записаться на кружок":
		await bot.send_chat_action(message.chat.id, 'typing')
		await asyncio.sleep(1)
		await bot.send_message(message.chat.id, text="Записаться на кружок \n [Ссылка](https://www.mos.ru/pgu/ru/application/dogm/077060701/#step_1)", reply_markup=mainmenu, parse_mode='Markdown')
	elif message.text == "📲Подключить школьный WiFi":
		await bot.send_chat_action(message.chat.id, 'typing')
		await asyncio.sleep(1)
		await bot.send_sticker(message.chat.id, 'CAADAgADc1kAAp7OCwABUikOpbNvciIWBA')
		await bot.send_message(message.chat.id, text="Подключить школьный WiFi \n 	Шаг первый на Портале госулуг надо иметь свою учетную запись, а не родителей. \n Шаг второй, передать данные классному руководителю. Что бы у тебя был доступ в Дневник. \n	Шаг третий в Дневнике справа вверху шестеренка. Входим в личный кабинет и уже там будет логин и пароль для приложения МЭШ и школьного WiFi\n Шаг последний, настроить телефон или планшет на подключение к школьной вафле, это уже по ссылке ниже \n	[Ссылка](https://t.me/iv?url=https%3A%2F%2Fuchebnik.mos.ru%2Fhelp%2Fstats%2Fwifi%2Fopenwifi&rhash=f33defb321a418)", reply_markup=mainmenu, parse_mode='Markdown')
	elif message.text == "📚Библиотека":
		await bot.send_chat_action(message.chat.id, 'typing')
		await asyncio.sleep(1)
		await bot.send_sticker(message.chat.id, 'CAADAgADdFkAAp7OCwABOKfFBU7BxRQWBA')
		await bot.send_message(message.chat.id, text="Наша библиотека", reply_markup=bibliomenu, parse_mode='Markdown')
	elif message.text == "☎️Контакты":
		await bot.send_chat_action(message.chat.id, 'typing')
		await asyncio.sleep(1)
		await bot.send_sticker(message.chat.id, 'CAADAgADelkAAp7OCwABYMZXStSxz9YWBA')
		await bot.send_message(message.chat.id, text="Контакты", reply_markup=contaktsmenu) 
	elif message.text == "📢Новости":
		await bot.send_chat_action(message.chat.id, 'typing')
		await asyncio.sleep(1)
		await bot.send_message(message.chat.id, text="Новости школьного сайта: \n [Ссылка](https://t.me/iv?url=https%3A%2F%2Fschzg719.mskobr.ru%2Fnovosti&rhash=b48987ea0be3c5)", reply_markup=mainmenu, parse_mode='Markdown')
	elif message.text == "📖Книги и учебники":
		await bot.send_chat_action(message.chat.id, 'typing')
		await asyncio.sleep(1)
		await bot.send_message(message.chat.id, text="Книги и учебники \n [Ссылка](https://schzg719.mskobr.ru/info_add/uchebniki_i_uchebnye_posobiya)", reply_markup=bibliomenu, parse_mode='Markdown')
	elif message.text == "🧾Журнал 8 А":
		await bot.send_chat_action(message.chat.id, 'typing')
		await asyncio.sleep(1)
		await bot.send_message(message.chat.id, text="Журнал класса \n [Ссылка](https://t.me/iv?url=https%3A%2F%2Fschzg719.mskobr.ru%2Fedu-news%2F2401&rhash=b48987ea0be3c5)", reply_markup=bibliomenu, parse_mode='Markdown')
	elif message.text == "👁‍🗨Школьный сайт":
		await bot.send_chat_action(message.chat.id, 'typing')
		await asyncio.sleep(1)
		await bot.send_message(message.chat.id, text="Школьный сайт: \n [Ссылка](https://schzg719.mskobr.ru/)", reply_markup=contaktsmenu, parse_mode='Markdown')
	elif message.text == "🗣Соцсети":
		await bot.send_chat_action(message.chat.id, 'typing')
		await asyncio.sleep(1)
		await bot.send_sticker(message.chat.id, 'CAADAgADfFkAAp7OCwABXIP9BynOq5UWBA', reply_markup=contaktsmenu)
		await bot.send_message(message.chat.id, text="Youtube: \n [Ссылка](https://www.youtube.com/channel/UCv9aT7dS9XEN1N7qU0gWNOA/)", reply_markup=contaktsmenu, parse_mode='Markdown')
		await bot.send_message(message.chat.id, text="Instagram: \n [Ссылка](https://www.instagram.com/s719zelao/)", reply_markup=contaktsmenu, parse_mode='Markdown')
		await bot.send_message(message.chat.id, text="VK: \n [Ссылка](https://vk.com/s719zelao)", reply_markup=contaktsmenu, parse_mode='Markdown')
	elif message.text == "📨Написать пиьсмо":
		await bot.send_chat_action(message.chat.id, 'typing')
		await asyncio.sleep(1)
		await bot.send_sticker(message.chat.id, 'CAADAgADcVkAAp7OCwABOa0ndWVQ9koWBA')
		await bot.send_message(message.chat.id, text="Написать пиьсмо в администрацию? \n 719@edu.mos.ru", reply_markup=contaktsmenu, parse_mode='Markdown')
	elif message.text == "🏫Главное меню":
		await bot.send_chat_action(message.chat.id, 'typing')
		await asyncio.sleep(1)
		await bot.send_message(message.chat.id, "Чем помочь?", reply_markup=mainmenu)
	elif message.text == "Админка":
		if message.chat.id==admin:
			c=ad_pere
		else:
			c=mainmenu
		await bot.send_message(message.chat.id, text="С большой силой приходит большая отвественность!", reply_markup=c, parse_mode='Markdown')
	elif message.text == "🗣Написать всем":
		if message.chat.id==admin:
			c=ad_pere
		else:
			c=mainmenu
		await pereslat(message)
		
	elif message.text == "🗣Публикация из rss":
		if message.chat.id==admin:
			c=ad_pere
		else:
			c=mainmenu
		await bot.send_message(message.chat.id, text="Начинаем отправку новостей", reply_markup=c, parse_mode='Markdown')
		await feederek()
	elif message.text == "Статистика":
		if message.chat.id==admin:
			c=ad_pere
		else:
			c=mainmenu
		get_users()
		for user in users:
			if int(user)<0:
				cugrup+=1
		cousers=len(users)-cugrup
		await bot.send_message(message.chat.id, text="В боте подписаны на рассылку " + str(cousers) + " человек и " + str(cugrup) + " групп", reply_markup=c, parse_mode='Markdown')
		cousers=0
		cogrup=0
		

@bot.message_handler(content_types=['voice'])
def voice_mess(message):  # ненавижу голосовухи
	bot.send_chat_action(message.chat.id, 'typing')
	await asyncio.sleep(1)
	bot.send_sticker(message.chat.id, 'CAADAgADlVkAAp7OCwABfWS6BUi0NtUWBA')
	bot.send_message(message.chat.id, text='Никто не любит голосовухи.')
  
	

# объявление менюшек
ad_mainmenu = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
ad_pere = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
mainmenu = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
newsmenu = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
bibliomenu = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
contaktsmenu = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)

# общие для всех меню кнопки
btn_tomain = types.KeyboardButton("🏫Главное меню")

# кнопки для отдельных менюшек
admin_btn = types.KeyboardButton("Админка")
btn_news_lnk = types.KeyboardButton("Новости школьного сайта")
btn_rasp = types.KeyboardButton("🗓Расписание")
btn_news_rss = types.KeyboardButton("Присылать новости в личку Вкл.\Выкл.")
btn_biblio_books = types.KeyboardButton("📖Книги и учебники")
btn_biblio_jurnal = types.KeyboardButton("🧾Журнал 8 А")
btn_cont_link = types.KeyboardButton("👁‍🗨Школьный сайт")
btn_cont_soc = types.KeyboardButton("🗣Соцсети")
btn_cont_email = types.KeyboardButton("📨Написать пиьсмо")
btn_news = types.KeyboardButton("📢Новости")
btn_kruz = types.KeyboardButton("🖋Записаться на кружок")
btn_wifi = types.KeyboardButton("📲Подключить школьный WiFi")
btn_biblio = types.KeyboardButton("📚Библиотека")
btn_contacts = types.KeyboardButton("☎️Контакты")
btn_pereslat = types.KeyboardButton("🗣Написать всем")
btn_feed = types.KeyboardButton("🗣Публикация из rss")
btn_stat = types.KeyboardButton("Статистика")

# добавление кнопок в меню
ad_mainmenu.add(btn_news, btn_rasp, btn_biblio, btn_kruz, btn_wifi, btn_contacts, admin_btn)
ad_pere.add(btn_tomain, btn_pereslat, btn_feed, btn_stat)
mainmenu.add(btn_news, btn_rasp, btn_biblio, btn_kruz, btn_wifi, btn_contacts)
newsmenu.add(btn_tomain, btn_news_lnk, btn_news_rss)
bibliomenu.add(btn_tomain, btn_biblio_books, btn_biblio_jurnal)
contaktsmenu.add(btn_tomain, btn_cont_link, btn_cont_soc, btn_cont_email)
keyboard3 = ReplyKeyboardMarkup(True, True)
keyboard3.row("❌ОТМЕНА")

asinc def feederek():
		for i in feed_list:
			fee = feedparser.parse(i)
			fee_title = fee.feed.title
			for x in range(2):
				fee_links.append(fee['entries'][x]['id'])
				if fee['entries'][x]['id'] in last_feeds:
					entry_title = fee['entries'][x]['title']
					entry_id = fee['entries'][x]['id']
					entry_link = fee['entries'][x]['link']
					await bot.send_message(admin, "Nothing new - " + entry_title)
				else:
					await asyncio.sleep(4)
					entry_title = fee['entries'][x]['title']
					entry_id = fee['entries'][x]['id']
					entry_link = fee['entries'][x]['link']
					await bot.send_message(admin, "Updated - " + entry_title)
					message = str(entry_title +"\n" + str(entry_link))
					for i in users:
						await asyncio.sleep(4)
						try:
							await bot.send_message(i, text=message)
						except:
							print('Bolt')
			pickle.dump(fee_links, open("db.p", 'wb'))
		return

#schedule.every().day.at('09:00').do(feederek) #запуск функции проверки рсс по времени
#schedule.every().day.at('15:00').do(feederek)
#while True:
#	schedule.run_pending()



async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bye!')

if __name__ == '__main__':
    schedule.run_pending()
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
