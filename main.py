import time

import telebot

# Ваш DSN

from apscheduler.schedulers.background import BackgroundScheduler
from telebot.types import Message

from config import BOT_TOKEN, USER_ID, YOUTUBE_RSS_URL, BOT_DEBUG
from database import update_new_obj
from utils import validate_channel, extract_channel_id, get_all_urls_from_rss, get_all_new_links

# Создание объекта бота
bot = telebot.TeleBot(BOT_TOKEN)


def my_interval_job():
    links = get_all_new_links()
    for link in links:
        bot.send_message(USER_ID, link)
        time.sleep(1)


@bot.message_handler()
def handle_specific_user_message(message: Message):
    try:
        if message.from_user.id == int(USER_ID):
            if message.text == "/start":
                bot.send_message(message.from_user.id, "Я активно работаю :)")
            else:
                text = message.text
                exists, channel_name = validate_channel(text)
                if exists:
                    channel_id, _username = extract_channel_id(text)
                    movie_urls: list = get_all_urls_from_rss(YOUTUBE_RSS_URL + channel_id)
                    update_new_obj({channel_id: movie_urls})
                    bot.send_message(message.from_user.id, "Канал успешно добавлен: " + channel_name)
                else:
                    bot.send_message(message.from_user.id,
                                     "Что-то неправильно отправили. \n"
                                     "Пример ссылки: https://www.youtube.com/channel/UCTgEgW843fSrCe_vPo4DHIA",
                                     disable_web_page_preview=True)
    except Exception as e:
        # Отправляем ошибку на Sentry
        if BOT_DEBUG is False:
            import sentry_sdk
            sentry_sdk.capture_exception(e)
        else:
            print("Ошибка: ", e)


# Создание планировщика
sched = BackgroundScheduler()

# Добавление задачи в планировщик (выполнение каждые 6 секунд)
sched.add_job(my_interval_job, trigger="interval", minutes=30)
sched.start()


def start_bot_polling():
    try:
        bot.polling()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        bot.stop_polling()


start_bot_polling()
