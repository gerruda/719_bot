import telebot
import requests
from telebot import types
import pickle
import feedparser
import time
from time import sleep
import cherrypy
import config
#from telebot import apihelper #метод работы с проксями pip3 install python-telegram-bot[socks] pip3 install -U requests[socks]
#apihelper.proxy = {'https': 'socks5h://91440724:ginbvXfh@grsst.s5.opennetwork.cc:999'}
#apihelper.proxy = {	'https': 'mtproto://7nJrbiBodXkgc29zaXRlOilnb29nbGUuY29t:mtprxz.duckdns.org:443'}
#}  #настройки прокси

#bot=telebot.TeleBot('591612755:AAGLQyZkmNUHNcqvcI1qsSE1KFez7J0qsjg')

feed_list =["https://schzg719.mskobr.ru/data/rss",
            ]
last_feeds = pickle.load(open("db.p", 'rb'))
fee_links = []
users=[]


#import os
#token = os.getenv("TOKEN")
#bot = telebot.TeleBot(token)
def get_users():
	global users
	f = open('users', 'r')
	m=(f.read())
	users=m.split(' ') #добавить в список значение и пробел
	f.close()
	users.pop() #удалить последний пробел
		
get_users() #вызов функций для подготовки переменных из файлов
		
@bot.message_handler(commands=["start"])
def start(message):
	global users
	username=message.from_user.first_name #запоминаем имя пользователя
	f = open('users', 'a') #открываем доступ к файлу на дозапись значений
	if str(message.chat.id) not in users: #проверяем чтобы не было повторов
			f.write(str(message.chat.id)+ ' ') #записать тех кто нажал старт
			print("Новый пользователь " + str(message.chat.id) + ' ' + message.from_user.first_name)
	f.close()
	get_users()
	bot.send_chat_action(message.chat.id, 'typing')
	time.sleep(2)
	bot.send_sticker(message.chat.id, 'CAADAgADa1kAAp7OCwABtPtscVkaOGoWBA')
	bot.send_message(message.chat.id, "Рады приветсвовать " + username + " в нашем боте помошнике.", reply_markup=mainmenu)

	
@bot.message_handler(commands=['pereslat']) #реакция на команду pereslat
def pereslat(message):
	bot.send_chat_action(message.chat.id, 'typing')
	time.sleep(2)
	bot.send_message(message.chat.id, text="Готов принять послание миру")
	bot.register_next_step_handler(message, get_pereslat) #вызываем функцию
	
@bot.message_handler(content_types=['text'])
def main(message):  # главное меню
#	if message.chat.id == 91440724:
#		mainmenu.add(admin_btn)
#       bot.send_message(message.chat.id, text="Рады приветсвовать Вас в нашем боте помошнике.", reply_markup=ad_mainmenu)
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
		bot.send_message(message.chat.id, text="Записаться на кружок \n [Ссылка](https://schzg719.mskobr.ru/edu-news/598)", reply_markup=mainmenu, parse_mode='Markdown')
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
		bot.send_message(message.chat.id, text="Книги и учебники \n [Ссылка](https://schzg719.mskobr.ru/ads_edu/22)", reply_markup=bibliomenu, parse_mode='Markdown')
	elif message.text == "🧾Журнал 8 А":
		bot.send_chat_action(message.chat.id, 'typing')
		time.sleep(2)
		bot.send_message(message.chat.id, text="Журнал класса", reply_markup=bibliomenu, parse_mode='Markdown')
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
		if message.chat.id == 91440724:
			mainmenu.add(admin_btn)
			bot.send_chat_action(message.chat.id, 'typing')
			time.sleep(2)
			bot.send_message(message.chat.id, text="Что отправляем?)", reply_markup=mainmenu, parse_mode='Markdown')

@bot.message_handler(content_types=['voice'])
def voice_mess(message):  # ненавижу голосовухи
	bot.send_chat_action(message.chat.id, 'typing')
	time.sleep(2)
	bot.send_sticker(message.chat.id, 'CAADAgADlVkAAp7OCwABfWS6BUi0NtUWBA')
	bot.send_message(message.chat.id, text='Никто не любит голосовухи.')
    
def get_pereslat(message): #её вызывали
	global users
	get_users
	if message.media_group_id==None:
		m=message.message_id
	else:
		m=message.message_id
	for i in users: #перебираем пользователей по массиву
		time.sleep(2)
		bot.forward_message(i, message.chat.id, m) #форвордим послание

# объявление менюшек
ad_mainmenu = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
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

# добавление кнопок в меню
ad_mainmenu.add(admin_btn, btn_news, btn_rasp, btn_biblio, btn_kruz, btn_wifi, btn_contacts)
mainmenu.add(btn_news, btn_rasp, btn_biblio, btn_kruz, btn_wifi, btn_contacts)
newsmenu.add(btn_tomain, btn_news_lnk, btn_news_rss)
bibliomenu.add(btn_tomain, btn_biblio_books, btn_biblio_jurnal)
contaktsmenu.add(btn_tomain, btn_cont_link, btn_cont_soc, btn_cont_email)

def feederek():
		for i in feed_list:
			fee = feedparser.parse(i)
			fee_title = fee.feed.title
			for x in range(3):
				fee_links.append(fee['entries'][x]['id'])
				if fee['entries'][x]['id'] in last_feeds:
					print("Nothing new - " + fee_title)
				else:
					sleep(10)
					entry_title = fee['entries'][x]['title']
					entry_id = fee['entries'][x]['id']
					print("Updated - " + fee_title)
					message = str(entry_title +"\n" + entry_id)
					for i in users:
						time.sleep(10)
						bot.send_message(i, text=message)
		pickle.dump(fee_links, open("db.p", 'wb'))
		return


#feederek()
#bot.polling(none_stop=True)
#while True:
#	try:
#		bot.polling(none_stop=True)
#	except: 
#		print('BOLT')
#		logging.error('error: {}'.format(sys.exc_info()[0]))
#		time.sleep(5)
class WebhookServer(object):
    # index равнозначно /, т.к. отсутствию части после ip-адреса (грубо говоря)
    @cherrypy.expose
    def index(self):
        length = int(cherrypy.request.headers['content-length'])
        json_string = cherrypy.request.body.read(length).decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 7772,
        'engine.autoreload.on': False
    })
    cherrypy.quickstart(WebhookServer(), '/', {'/': {}})
