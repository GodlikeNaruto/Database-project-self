import config
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from random import randint
import sqlite3 

bot = telebot.TeleBot(config.API_TOKEN)

def senf_info(bot, message, row):
        
    info = f"""
📍Title:          {row[0]}
📍Type:           {row[1]}
📍Genres:         {row[12]}
📍Rating:         {row[15]}
📍# of Episodes:  {row[2]}
📍Description:    {row[19]}
🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻
"""
    bot.send_message(message.chat.id, info)


def senf_10(bot, chat_id, row):
        
    info = ''
    for i in row:
        s = f'📍Title: {i[0]}  📍Score: {i[1]}'
        s.center(66, ' ')
        info += s + '\n'
    
    info += '🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻'
    bot.send_message(chat_id, info)


def main_markup():
  markup = ReplyKeyboardMarkup()
  markup.add(KeyboardButton('/random'))
  markup.add(KeyboardButton('/top'))
  markup.add(KeyboardButton('/genres'))
  return markup


def gen_markup(chat_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Action", callback_data=f"Action:{chat_id}"),
                               InlineKeyboardButton("Adventure", callback_data=f"Adventure:{chat_id}"),
                               InlineKeyboardButton("Comedy", callback_data=f"Comedy:{chat_id}"),
                               InlineKeyboardButton("Demons", callback_data=f"Demons:{chat_id}"),
                               InlineKeyboardButton("Shounen", callback_data=f"Shounen:{chat_id}"),
                               InlineKeyboardButton("Supernatural", callback_data=f"Supernatural:{chat_id}"),
                               InlineKeyboardButton("Drama", callback_data=f"Drama:{chat_id}"),
                               InlineKeyboardButton("Fantasy", callback_data=f"Fantasy:{chat_id}"),
                               InlineKeyboardButton("Josei", callback_data=f"Josei:{chat_id}"),
                               InlineKeyboardButton("Kids", callback_data=f"Kids:{chat_id}"),
                               InlineKeyboardButton("Military", callback_data=f"Military:{chat_id}"),
                               InlineKeyboardButton("Magic", callback_data=f"Magic:{chat_id}"),
                               InlineKeyboardButton("Super Power", callback_data=f"Super Power:{chat_id}"),
                               InlineKeyboardButton("Romance", callback_data=f"Romance:{chat_id}"),
                               InlineKeyboardButton("Historical", callback_data=f"Historical:{chat_id}"),
                               InlineKeyboardButton("Space", callback_data="fSpace:{chat_id}"),
                               InlineKeyboardButton("Sci-Fi", callback_data=f"Sci-Fi:{chat_id}"),
                               InlineKeyboardButton("Seinen", callback_data=f"Seinen:{chat_id}"),
                               InlineKeyboardButton("Martial Arts", callback_data=f"Martial Arts:{chat_id}"),
                               InlineKeyboardButton("Samurai", callback_data=f"Samurai:{chat_id}"),
                               InlineKeyboardButton("School", callback_data=f"School:{chat_id}"),
                               InlineKeyboardButton("Parody", callback_data=f"Parody:{chat_id}"),
                               InlineKeyboardButton("Mecha", callback_data=f"Mecha:{chat_id}"),
                               InlineKeyboardButton("Police", callback_data=f"Police:{chat_id}"),
                               InlineKeyboardButton("Sports", callback_data=f"Sports:{chat_id}"),
                               InlineKeyboardButton("Shoujo", callback_data=f"Shoujo:{chat_id}"),
                               InlineKeyboardButton("Horror", callback_data=f"Horror:{chat_id}"),
                               InlineKeyboardButton("Vampire", callback_data=f"Vampire:{chat_id}"),
                               InlineKeyboardButton("Psychological", callback_data=f"Psychological:{chat_id}"),
                               InlineKeyboardButton("Mystery", callback_data=f"Mystery:{chat_id}"),
                               InlineKeyboardButton("Game", callback_data=f"Game:{chat_id}"),
                               InlineKeyboardButton("Thriller", callback_data=f"Thriller:{chat_id}"),
                               InlineKeyboardButton("Slice of Life", callback_data=f"Slice of Life:{chat_id}"),
                               InlineKeyboardButton("Shoujo", callback_data=f"Shoujo:{chat_id}"),
                               InlineKeyboardButton("Music", callback_data=f"Music:{chat_id}"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    name = call.data
    name = name.split(':')

    con = sqlite3.connect("animes.db")
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT Title, Score FROM animes WHERE Genres LIKE '%{name[0]}%' ORDER BY Score LIMIT 10")
        row = cur.fetchall()
        cur.close()
    senf_10(bot, name[1], row)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """Hello! You're welcome to the best Anime-Chat-Bot🎥!
Here you can find 1000+ animes 🔥
Click /random to get random anime
Click /top to get top 10 best anime
Click /genres to get top anime with desired genre
Or write the title of anime and I will try to find it! 🎬 """, reply_markup=main_markup())

@bot.message_handler(commands=['random'])
def random_anime(message):
    con = sqlite3.connect("animes.db")
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM animes ORDER BY RANDOM() LIMIT 1")
        row = cur.fetchall()[0]
        cur.close()
    senf_info(bot, message, row)


@bot.message_handler(commands=['genres'])
def find_by_genre(message):
    bot.send_message(message.chat.id, 'Select the desired genre', reply_markup=gen_markup(message.chat.id))


@bot.message_handler(commands=['top'])
def top_anime(message):
    con = sqlite3.connect("animes.db")
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT Title, Score FROM animes ORDER BY Score DESC LIMIT 10")
        row = cur.fetchall()
        cur.close()
    senf_10(bot, message.chat.id, row)

    
@bot.message_handler(func=lambda message: True)
def echo_message(message):

    con = sqlite3.connect("animes.db")
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM animes WHERE title LIKE '%{message.text.lower()}%'")
        row = cur.fetchall()
        if row:
            row = row[0]
            bot.send_message(message.chat.id,"Of course! I know this anime😌")
            senf_info(bot, message, row)
        else:
            bot.send_message(message.chat.id,"I don't know this anime ")

        cur.close()



bot.infinity_polling()