import telegram.ext
import imdb
import urllib
import urllib.request
import json
import random

import ssl



ssl._create_default_https_context = ssl._create_unverified_context

with open('telegram_api_key.txt', 'r') as f:
    API_KEY = f.read()
with open('OMDB_API_KEY.txt', 'r') as f:
    OMDB_API_KEY = f.read()
with open('imdbapi_key.txt', 'r') as f:
    IMDB_API_KEY = f.read()



def start(update, context):
    update.message.reply_text("Hello! Welcome to lookupshows bot!\nType /help to view available commands")


def help(update, context):
    update.message.reply_text("""
    The following commands are available:

    /start -> Starts bot
    /help -> Lists available commands
    /recommendmovies -> Recommend a random popular movie
    /recommendseries -> Recommend a random popular series
    /top5movies -> Lists top 5 movies at the moment
    /top5series -> Lists top 5 series at the moment
    /searchbyname <insert name> -> Search actors/director shows (still building)

    For a detailed description of show:
    Just type in any show title!
    
    *Database from IMDb*
    """)


ia = imdb.IMDb()


def title(update, context):
    movie = update.message.text
    search = ia.search_movie(movie)

    id = 'tt' + search[0].movieID

    url = 'http://www.omdbapi.com/?i=' + id + '&apikey=' + OMDB_API_KEY

    x = urllib.request.urlopen(url)

    for line in x:
        x = line.decode()

    data = json.loads(x)

    ans = ''
    ans += '*' + data['Title'] + '* (' + data['Year'] + ')' + '\n\n'
    ans += '*Director*: ' + data['Director'] + '\n'
    ans += '*Cast*: ' + data['Actors'] + '\n'
    ans += '*Genre*: ' + data['Genre'] + '\n\n'
    ans += '*Runtime*: ' + data['Runtime'] + '\n\n'
    ans += '*Plot*: ' + data['Plot'] + '\n\n'
    ans += '*IMDb Rating*: ' + data['imdbRating'] + ' \n'
    #ans += '*Rotten Tomatoes Rating(Critic)*: ' + data['Ratings'][1]['Value'] + ' \n' (cannot run if its a series)
    ans += '[.](' + data['Poster'] + ')'
    update.message.reply_text(ans, parse_mode='markdown')


def recommendseries(update, context):
    url = 'https://imdb-api.com/en/API/MostPopularTVs/' + IMDB_API_KEY

    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urllib.request.urlopen(req).read()
    x = web_byte.decode('utf-8')

    data = json.loads(x)

    rand = random.randrange(1, 100)
    ans = ''
    ans += '*Rank*: ' + data['items'][rand]['rank'] + '\n'
    ans += '*Title*: ' + data['items'][rand]['title'] + ' (' + data['items'][rand]['year'] + ')' + '\n\n'
    ans += '*Crew*: ' + data['items'][rand]['crew'] + '\n'
    ans += '*IMDb Rating*: ' + data['items'][rand]['imDbRating'] + ' \n'
    ans += '[.](' + data['items'][rand]['image'] + ')'
    update.message.reply_text(ans, parse_mode='markdown')
    update.message.reply_text('*Retrieve show plot just by typing show title*', parse_mode='markdown')


def recommendmovies(update, context):
    url = 'https://imdb-api.com/en/API/MostPopularMovies/' + IMDB_API_KEY
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urllib.request.urlopen(req).read()
    x = web_byte.decode('utf-8')

    data = json.loads(x)

    rand = random.randrange(1, 100)
    ans = ''
    ans += '*Rank*: ' + data['items'][rand]['rank'] + '\n'
    ans += '*Title*: ' + data['items'][rand]['title'] + ' (' + data['items'][rand]['year'] + ')' + '\n\n'
    ans += '*Crew*: ' + data['items'][rand]['crew'] + '\n'
    ans += '*IMDb Rating*: ' + data['items'][rand]['imDbRating'] + ' \n'
    ans += '[.](' + data['items'][rand]['image'] + ')\n'
    update.message.reply_text(ans, parse_mode='markdown')
    update.message.reply_text('*Retrieve show plot just by typing show title*', parse_mode='markdown')

def top5movies(update, context):
    url = 'https://imdb-api.com/en/API/MostPopularMovies/' + IMDB_API_KEY
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urllib.request.urlopen(req).read()
    x = web_byte.decode('utf-8')

    data = json.loads(x)

    ans = ''
    for i in range(5):
        ans += '*Rank*:' + data['items'][i]['rank'] + '\n'
        ans += '* Title*:' + data['items'][i]['title'] + ' (' + data['items'][i]['year'] + ')' + '\n\n'
        ans += '*Crew*: ' + data['items'][i]['crew'] + '\n'
        ans += '*IMDb Rating*: ' + data['items'][i]['imDbRating'] + ' \n'
        ans += '[.](' + data['items'][i]['image'] + ')\n'
        update.message.reply_text(ans, parse_mode='markdown')
        ans =''
    update.message.reply_text('*Retrieve show plot just by typing show title*', parse_mode='markdown')

def top5series(update, context):
    url = 'https://imdb-api.com/en/API/MostPopularTVs/' + IMDB_API_KEY
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urllib.request.urlopen(req).read()
    x = web_byte.decode('utf-8')

    data = json.loads(x)

    ans = ''
    for i in range(5):
        ans += '*Rank*:' + data['items'][i]['rank'] + '\n'
        ans += '* Title*:' + data['items'][i]['title'] + ' (' + data['items'][i]['year'] + ')' + '\n\n'
        ans += '*Crew*: ' + data['items'][i]['crew'] + '\n'
        ans += '*IMDb Rating*: ' + data['items'][i]['imDbRating'] + ' \n'
        ans += '[.](' + data['items'][i]['image'] + ')\n'
        update.message.reply_text(ans, parse_mode='markdown')
        ans =''
    update.message.reply_text('*Retrieve show plot just by typing show title*', parse_mode='markdown')

#def searchbyname(update, context):
#    update.message.reply_text('Input name of director/actor to search')
#    name = update.message.text
#    url = 'https://imdb-api.com/en/API/SearchName/' + IMDB_API_KEY + name
#    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
#    web_byte = urllib.request.urlopen(req).read()
#    x = web_byte.decode('utf-8')

#    data = json.loads(x)
#    ans = ''
#    for i in range(10):
#        ans += '*' + data['results'][i]['title'] + '*\n'
#        ans += data['results'][i]['title'] + '*\n'
#        ans += '[.](' + data['results'][i]['image'] + ')'
#        ans = ''
#    update.message.reply_text(ans, parse_mode='markdown')

updater = telegram.ext.Updater(API_KEY, use_context=True)

disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler("start", start))
disp.add_handler(telegram.ext.CommandHandler("help", help))
disp.add_handler(telegram.ext.CommandHandler("recommendmovies", recommendmovies))
disp.add_handler(telegram.ext.CommandHandler("recommendseries", recommendseries))
disp.add_handler(telegram.ext.CommandHandler("top5movies", top5movies))
disp.add_handler(telegram.ext.CommandHandler("top5series", top5series))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, title))
#disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, searchbyname), group=1)


updater.start_polling()
updater.idle()
