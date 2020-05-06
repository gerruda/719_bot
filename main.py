
import telebot
import requests
from telebot import types
import pickle
import feedparser
import time
from time import sleep
import cherrypy
import config
import schedule

WEBHOOK_HOST = 'uchenikoff.ru'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = '/etc/letsencrypt/live/www.uchenikoff.ru/fullchain.pem'
WEBHOOK_SSL_PRIV = '/etc/letsencrypt/live/www.uchenikoff.ru/privkey.pem'

WEBHOOK_URL_BASE = "https://www.uchenikoff.ru/ZZZZ/"
WEBHOOK_URL_PATH = "/"

bot=telebot.TeleBot(config.token)

feed_list =["https://schzg719.mskobr.ru/data/rss", "https://www.youtube.com/feeds/videos.xml?channel_id=UCv9aT7dS9XEN1N7qU0gWNOA",
            ]
last_feeds = pickle.load(open("db.p", 'rb'))
fee_links = []
users=[]
admin=91440724
c=()

def get_users():
	global users
	f = open('users', 'r')
	m=(f.read())
	users=m.split(' ') #добавить в список значение и пробел
	f.close()
	users.pop()#удалить последний пробел
		
get_users() #вызов функций для подготовки переменных из файлов
		
@bot.message_handler(commands=["start"])
def start(message):
	global users
	global c
	username=message.from_user.first_name #запоминаем имя пользователя
	f = open('users', 'a') #открываем доступ к файлу на дозапись значений
	if str(message.chat.id) not in users: #проверяем чтобы не было повторов
			f.write(str(message.chat.id)+ ' ') #записать тех кто нажал старт
			bot.send_message(admin, "Новый пользователь " + str(message.chat.id) + ' ' + message.from_user.first_name)
	f.close()
	get_users()
	if message.chat.id==admin:
		c=ad_mainmenu
	else:
		c=mainmenu
	bot.send_chat_action(message.chat.id, 'typing')
	time.sleep(2)
	bot.send_sticker(message.chat.id, 'CAADAgADa1kAAp7OCwABtPtscVkaOGoWBA')
	bot.send_message(message.chat.id, "Рады приветсвовать " + username + " в нашем боте помошнике. \n Вы автоматически подписаны на обновления новостей нашего сайта и некоторых соц.сетей. ДЛя остановки подписки используйте команду /stop, для повтора подписки используйте команду /start. А еще нашего бота можно добавить в группу, сделать администратором и он будет посылать новости в группу.", reply_markup=c)

@bot.message_handler(commands=["stop"])
def stop(message):
	global users
	global c
	username=message.from_user.first_name #запоминаем имя пользователя
	f = open('users', 'r')
	m=(f.read())
	m=m.replace(str(message.chat.id) + ' ', '')
	f.close()
	f = open('users', 'w') #открываем доступ к файлу на запись
	f.writelines(m)
	f.close()
	bot.send_message(admin, "Пользователь отписался " + str(message.chat.id) + ' ' + message.from_user.first_name)
	get_users()
		
@bot.message_handler(commands=['pereslat']) #реакция на команду pereslat
def pereslat(message):
	bot.send_message(message.chat.id, text="Готов принять послание миру")
	bot.register_next_step_handler(message, get_pereslat) #вызываем функцию
	
def get_pereslat(message): #её вызывали
	global users
	get_users
	print(message.media_group_id, users)
#	bot.forward_message(i, message.chat.id, message.message_id) #форвордим послание
#	try:
#		print(message)
#	try:
#		print(message.json)
#	except:
#		print(message.photo)
#	if message.media_group_id==None:
#		for i in users: #перебираем пользователей по массиву
#			time.sleep(2)
#			try:
#				bot.forward_message(i, message.chat.id, message.message_id) #форвордим послание
#			except:
#				print('bolt')
#	else:
#		print(2)
#		print(message.media_group_id)
#		for i in users: #перебираем пользователей по массиву
#			time.sleep(2)
#			try:
#				bot.sendMediaGroup(i, message.photo.file_id)
#			except:
#				print('bolt')
	for i in users: #перебираем пользователей по массиву
		time.sleep(2)
		try:
			bot.forward_message(i, message.chat.id, message.message_id) #форвордим послание
		except:
			print('bolt')
	
@bot.message_handler(content_types=['text'])
def main(message):  # главное меню
	global c
	cousers=0
	cugrup=0
	global users
	if message.text == "Привет" or message.text == "🏫Главное меню" or message.text == "/main" or message.text == "/start":
		start(message)
	elif message.text == "🗓Расписание":
		bot.send_chat_action(message.chat.id, 'typing')
		time.sleep(2)
		bot.send_sticker(message.chat.id, 'CAADAgADglkAAp7OCwABF1LyypVAYq0WBA')
		bot.send_message(message.chat.id, text="Расписание \n [Ссылка](https://t.me/iv?url=https%3A%2F%2Fschzg719.mskobr.ru%2Finfo_add%2Fraspisanie-urokov&rhash=b48987ea0be3c5)", reply_markup=mainmenu, parse_mode='Markdown')
	elif message.text == "🖋Записаться на кружок":
		bot.send_chat_action(message.chat.id, 'typing')
		time.sleep(2)
		bot.send_message(message.chat.id, text="Записаться на кружок \n [Ссылка](https://www.mos.ru/pgu/ru/application/dogm/077060701/#step_1)", reply_markup=mainmenu, parse_mode='Markdown')
	elif message.text == "📲Подключить школьный WiFi":
		bot.send_chat_action(message.chat.id, 'typing')
		time.sleep(2)
		bot.send_sticker(message.chat.id, 'CAADAgADc1kAAp7OCwABUikOpbNvciIWBA')
		bot.send_message(message.chat.id, text="Подключить школьный WiFi \n 	Шаг первый на Портале госулуг надо иметь свою учетную запись, а не родителей. \n Шаг второй, передать данные классному руководителю. Что бы у тебя был доступ в Дневник. \n	Шаг третий в Дневнике справа вверху шестеренка. Входим в личный кабинет и уже там будет логин и пароль для приложения МЭШ и школьного WiFi\n Шаг последний, настроить телефон или планшет на подключение к школьной вафле, это уже по ссылке ниже \n	[Ссылка](https://t.me/iv?url=https%3A%2F%2Fuchebnik.mos.ru%2Fhelp%2Fstats%2Fwifi%2Fopenwifi&rhash=f33defb321a418)", reply_markup=mainmenu, parse_mode='Markdown')
	elif message.text == "📚Библиотека":
		bot.send_chat_action(message.chat.id, 'typing')
		time.sleep(2)
		bot.send_sticker(message.chat.id, 'CAADAgADdFkAAp7OCwABOKfFBU7BxRQWBA')
		bot.send_message(message.chat.id, text="Наша библиотека", reply_markup=bibliomenu, parse_mode='Markdown')
	elif message.text == "☎️Контакты":
		bot.send_chat_action(message.chat.id, 'typing')
		time.sleep(2)
		bot.send_sticker(message.chat.id, 'CAADAgADelkAAp7OCwABYMZXStSxz9YWBA')
		bot.send_message(message.chat.id, text="Контакты", reply_markup=contaktsmenu) 
	elif message.text == "📢Новости":
		bot.send_chat_action(message.chat.id, 'typing')
		time.sleep(2)
		bot.send_message(message.chat.id, text="Новости школьного сайта: \n [Ссылка](https://t.me/iv?url=https%3A%2F%2Fschzg719.mskobr.ru%2Fnovosti&rhash=b48987ea0be3c5)", reply_markup=mainmenu, parse_mode='Markdown')
	elif message.text == "📖Книги и учебники":
		bot.send_chat_action(message.chat.id, 'typing')
		time.sleep(2)
		bot.send_message(message.chat.id, text="Книги и учебники \n [Ссылка](https://schzg719.mskobr.ru/info_add/uchebniki_i_uchebnye_posobiya)", reply_markup=bibliomenu, parse_mode='Markdown')
	elif message.text == "🧾Журнал 8 А":
		bot.send_chat_action(message.chat.id, 'typing')
		time.sleep(2)
		bot.send_message(message.chat.id, text="Журнал класса \n [Ссылка](https://t.me/iv?url=https%3A%2F%2Fschzg719.mskobr.ru%2Fedu-news%2F2401&rhash=b48987ea0be3c5)", reply_markup=bibliomenu, parse_mode='Markdown')
	elif message.text == "👁‍🗨Школьный сайт":
		bot.send_chat_action(message.chat.id, 'typing')
		time.sleep(2)
		bot.send_message(message.chat.id, text="Школьный сайт: \n [Ссылка](https://schzg719.mskobr.ru/)", reply_markup=contaktsmenu, parse_mode='Markdown')
	elif message.text == "🗣Соцсети":
		bot.send_chat_action(message.chat.id, 'typing')
		time.sleep(2)
		bot.send_sticker(message.chat.id, 'CAADAgADfFkAAp7OCwABXIP9BynOq5UWBA', reply_markup=contaktsmenu)
		bot.send_message(message.chat.id, text="Youtube: \n [Ссылка](https://www.youtube.com/channel/UCv9aT7dS9XEN1N7qU0gWNOA/)", reply_markup=contaktsmenu, parse_mode='Markdown')
		bot.send_message(message.chat.id, text="Instagram: \n [Ссылка](https://www.instagram.com/s719zelao/)", reply_markup=contaktsmenu, parse_mode='Markdown')
		bot.send_message(message.chat.id, text="VK: \n [Ссылка](https://vk.com/s719zelao)", reply_markup=contaktsmenu, parse_mode='Markdown')
	elif message.text == "📨Написать пиьсмо":
		bot.send_chat_action(message.chat.id, 'typing')
		time.sleep(2)
		bot.send_sticker(message.chat.id, 'CAADAgADcVkAAp7OCwABOa0ndWVQ9koWBA')
		bot.send_message(message.chat.id, text="Написать пиьсмо в администрацию? \n 719@edu.mos.ru", reply_markup=contaktsmenu, parse_mode='Markdown')
	elif message.text == "🏫Главное меню":
		bot.send_chat_action(message.chat.id, 'typing')
		time.sleep(2)
		bot.send_message(message.chat.id, "Чем помочь?", reply_markup=mainmenu)
	elif message.text == "Админка":
		if message.chat.id==admin:
			c=ad_pere
		else:
			c=mainmenu
		bot.send_message(message.chat.id, text="С большой силой приходит большая отвественность!", reply_markup=c, parse_mode='Markdown')
	elif message.text == "🗣Написать всем":
		if message.chat.id==admin:
			c=ad_pere
		else:
			c=mainmenu
		bot.send_chat_action(message.chat.id, 'typing')
		time.sleep(2)
		pereslat(message)
		
	elif message.text == "🗣Публикация из rss":
		if message.chat.id==admin:
			c=ad_pere
		else:
			c=mainmenu
		bot.send_chat_action(message.chat.id, 'typing')
		time.sleep(2)
		bot.send_message(message.chat.id, text="Начинаем отправку новостей", reply_markup=c, parse_mode='Markdown')
		feederek()
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
		bot.send_message(message.chat.id, text="В боте подписаны на рассылку " + str(cousers) + " человек и " + str(cugrup) + " групп", reply_markup=c, parse_mode='Markdown')
		cousers=0
		cogrup=0
		

@bot.message_handler(content_types=['voice'])
def voice_mess(message):  # ненавижу голосовухи
	bot.send_chat_action(message.chat.id, 'typing')
	time.sleep(2)
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

def feederek():
		for i in feed_list:
			fee = feedparser.parse(i)
			fee_title = fee.feed.title
			for x in range(2):
				fee_links.append(fee['entries'][x]['id'])
				if fee['entries'][x]['id'] in last_feeds:
					entry_title = fee['entries'][x]['title']
					entry_id = fee['entries'][x]['id']
					entry_link = fee['entries'][x]['link']
					bot.send_message(admin, "Nothing new - " + entry_title)
				else:
					sleep(4)
					entry_title = fee['entries'][x]['title']
					entry_id = fee['entries'][x]['id']
					entry_link = fee['entries'][x]['link']
					bot.send_message(admin, "Updated - " + entry_title)
					message = str(entry_title +"\n" + str(entry_link))
					for i in users:
						time.sleep(4)
						try:
							bot.send_message(i, text=message)
						except:
							print('Bolt')
			pickle.dump(fee_links, open("db.p", 'wb'))
		return

schedule.every().day.at('09:00').do(feederek) #запуск функции проверки рсс по времени
schedule.every().day.at('15:00').do(feederek)
#while True:
#	schedule.run_pending()

# Наш вебхук-сервер
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)

# Снимаем вебхук перед повторной установкой (избавляет от некоторых проблем)
#bot.remove_webhook()

# Ставим заново вебхук
#bot.set_webhook(url=WEBHOOK_URL_BASE)

#bot.set_webhook(url=WEBHOOK_URL_BASE, certificate=open(WEBHOOK_SSL_CERT, 'r'))


if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL_BASE)
    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 7772,
        'engine.autoreload.on': False
    })
    cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})

# Указываем настройки сервера CherryPy
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})
