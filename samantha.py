#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import re, requests
import logging
import json
import random
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram import (Poll, ParseMode, KeyboardButton, KeyboardButtonPollType, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, PollAnswerHandler, PollHandler, MessageHandler, Filters, ConversationHandler)
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN_ID = '1363716020:AAFgLfvVz9YJ4DqhJBZ0-va6oPnpzxfiL_o'
URL = "https://api.telegram.org/bot{}/".format(TELEGRAM_TOKEN_ID)


def start(update, context):
    """Inform user about what this bot can do"""
    update.message.reply_text('Oi, estou aqui! O que você precisa? /dogo /gatineo /clima /piada /spotifyme')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def poll(update, context):
    """Sends a predefined poll"""
    questions = ["Ótimo", "Bom", "Normal", "Péssimo"]
    message = context.bot.send_poll(update.effective_chat.id, "Como vc tá?", questions,
                                    is_anonymous=False, allows_multiple_answers=True)
    # Save some info about the poll the bot_data for later use in receive_poll_answer
    payload = {message.poll.id: {"questions": questions, "message_id": message.message_id,
                                 "chat_id": update.effective_chat.id, "answers": 0}}
    context.bot_data.update(payload)

def receive_poll_answer(update, context):
    """Summarize a users poll vote"""
    answer = update.poll_answer
    poll_id = answer.poll_id
    try:
        questions = context.bot_data[poll_id]["questions"]
    # this means this poll answer update is from an old poll, we can't do our answering then
    except KeyError:
        return
    selected_options = answer.option_ids
    answer_string = ""
    for question_id in selected_options:
        if question_id != selected_options[-1]:
            answer_string += questions[question_id] + " and "
        else:
            answer_string += questions[question_id]
    context.bot.send_message(context.bot_data[poll_id]["chat_id"],
                             "{} feels {}!".format(update.effective_user.mention_html(),
                                                   answer_string),
                             parse_mode=ParseMode.HTML)
    context.bot_data[poll_id]["answers"] += 1
    # Close poll after three participants voted
    if context.bot_data[poll_id]["answers"] == 3:
        context.bot.stop_poll(context.bot_data[poll_id]["chat_id"],
                              context.bot_data[poll_id]["message_id"])

def quiz(update, context):
    """Send a predefined poll"""
    questions = ["1", "2", "4", "20"]
    message = update.effective_message.reply_poll("How many eggs do you need for a cake?",
                                                  questions, type=Poll.QUIZ, correct_option_id=2)
    # Save some info about the poll the bot_data for later use in receive_quiz_answer
    payload = {message.poll.id: {"chat_id": update.effective_chat.id,
                                 "message_id": message.message_id}}
    context.bot_data.update(payload)

def receive_quiz_answer(update, context):
    """Close quiz after three participants took it"""
    # the bot can receive closed poll updates we don't care about
    if update.poll.is_closed:
        return
    if update.poll.total_voter_count == 3:
        try:
            quiz_data = context.bot_data[update.poll.id]
        # this means this poll answer update is from an old poll, we can't stop it then
        except KeyError:
            return
        context.bot.stop_poll(quiz_data["chat_id"], quiz_data["message_id"])

def preview(update, context):
    """Ask user to create a poll and display a preview of it"""
    # using this without a type lets the user chooses what he wants (quiz or poll)
    button = [[KeyboardButton("Press me!", request_poll=KeyboardButtonPollType())]]
    message = "Press the button to let the bot generate a preview for your poll"
    # using one_time_keyboard to hide the keyboard
    update.effective_message.reply_text(message,
                                        reply_markup=ReplyKeyboardMarkup(button,
                                                                         one_time_keyboard=True))

def receive_poll(update, context):
    """On receiving polls, reply to it by a closed poll copying the received poll"""
    actual_poll = update.effective_message.poll
    # Only need to set the question and options, since all other parameters don't matter for
    # a closed poll
    update.effective_message.reply_poll(
        question=actual_poll.question,
        options=[o.text for o in actual_poll.options],
        # with is_closed true, the poll/quiz is immediately closed
        is_closed=True,
        reply_markup=ReplyKeyboardRemove()
    )

def help_handler(update, context):
    """Display a help message"""
    update.message.reply_text("Use /quiz, /poll ou /preview para acessar meus talentos.")

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('até logo.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def receive_quiz_answer(update, context):
    """Close quiz after three participants took it"""
    # the bot can receive closed poll updates we don't care about
    if update.poll.is_closed:
        return
    if update.poll.total_voter_count == 3:
        try:
            quiz_data = context.bot_data[update.poll.id]
        # this means this poll answer update is from an old poll, we can't stop it then
        except KeyError:
            return
        context.bot.stop_poll(quiz_data["chat_id"], quiz_data["message_id"])

def dogo(update, context):
    '''
    '''
    import randonDogo as rd
    count = 0
    while(count<3):
        url = rd.get_onedogo()
        context.bot.send_photo(chat_id=update.effective_chat.id, photo = url)
        count=count+1

def gatineo(update, context):
    '''
    '''

    import randonCat as rc
    count = 0
    while(count<3):
        url = rc.get_onecat()
        context.bot.send_photo(chat_id=update.effective_chat.id, photo = url)
        count=count+1

def piada(update, context):
    '''
    '''
    import pyjokes
    update.message.reply_text(pyjokes.get_joke())

def voice_handler(update, context):
    
    update.download_file(msg['photo'][-1]['file_id'], './file.png')

def detect_text():
    """Detects text in the file."""
    from google.cloud import vision
    import io

    image_uri = '/Users/Andrade/Downloads/tropical-glass-4q-inox-9-scaled.jpg'

    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

def get_weather(update, context):
    '''
    Inform user about the weather
    '''
    
    import weather
    myCity = "Pato Branco"
    temperature, temperature_feelslike, humidity, skyCondition, uvi = weather.get_weather(myCity)

    if skyCondition == "Clear":
        skyCondition = "limpo"
    
    if uvi<5.9:
        msg = "Temperatura: " + '{:02.2f}'.format(temperature) + "ºC\nEstado do Céu: " + skyCondition + '\nRaios UV estão seguros!\nUmidade: ' + str(humidity)

    elif (uvi>5.9) and (uvi<=7.9):
        msg = "Temperatura: " + '{:02.2f}'.format(temperature) + "ºC\nEstado do Céu: " + skyCondition + '\nRaios UV estão no nível Laranja (' + str(uvi) + '), ou seja, muito altos!\nUmidade: ' + str(humidity)
    
    elif uvi>7.9:
        msg = "Temperatura: " + '{:02.2f}'.format(temperature) + "ºC\nEstado do Céu: " + skyCondition + "! " + '\nRaios UV estão no nível Vermelho (' + str(uvi) + '), então não saia no sol\nUmidade: ' + str(humidity)


    update.message.reply_text(msg)

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def spotify(update, context):
    '''
    '''

    # Imports
    import sys
    sys.path.append('../spotify_analyzer/')
    import spotify_code as sc

    num_tracks = 20

    chat_id=update.effective_chat.id
    
    # -------- GET SEED/GENRE -------- #
    genres = sc.get_genres()
    num_genres = len(genres)
    genre_choice = random.randint(0,(num_genres-1))
    
    update.message.reply_text("Escolhendo músicas e adicionando na playlist...")
    
    # -------- CREATE NEW PLAYLIST -------- #
    username = 'guilherme_andrade_' 
    scope = 'playlist-modify-public'
    newplaylist_id,playlist_link = sc.set_playlist(username,"Fuck off, I'm Samantha! " + str(genres[genre_choice]).capitalize(),"As músicas dessa playlist foram escolhidas pela Samantha, uma assistente pessoal baseada em inteligência artificial.")

    # -------- CLASSIFIER -------- #
    import neural_network
    num_tracks,tracks_analysis = sc.get_new_tracks(num_tracks,str(genres[genre_choice]))

    id_list = []
    i=0
    while(i<num_tracks):

        if(neural_network.NN(tracks_analysis.loc[i,'popularity'],tracks_analysis.loc[i,'danceability'],tracks_analysis.loc[i,'energy'],tracks_analysis.loc[i,'key'],tracks_analysis.loc[i,'loudness'],tracks_analysis.loc[i,'mode'],tracks_analysis.loc[i,'speechiness'],tracks_analysis.loc[i,'acousticness'],tracks_analysis.loc[i,'instrumentalness'],tracks_analysis.loc[i,'liveness'],tracks_analysis.loc[i,'valence'],tracks_analysis.loc[i,'tempo']))==1:
            print(tracks_analysis.loc[i,'spotify_link'],tracks_analysis.loc[i,'name_track'],tracks_analysis.loc[i,'id_track'])
            id_list.append(tracks_analysis.loc[i,'id_track'])

        i = i + 1


    # -------- PUT SELECTED TRACKS IN THE NEW PLAYLIST -------- #
    sc.insert_tracks_playlist(newplaylist_id,id_list)
    update.message.reply_text("Sua playlist tá quentinha!")
    update.message.reply_text(playlist_link)

def main():

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    updater = Updater('1363716020:AAFgLfvVz9YJ4DqhJBZ0-va6oPnpzxfiL_o', use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler
    """
    dp.add_handler(CommandHandler('poll', poll))
    dp.add_handler(PollAnswerHandler(receive_poll_answer))
    dp.add_handler(CommandHandler('quiz', quiz))
    dp.add_handler(PollHandler(receive_quiz_answer))
    dp.add_handler(CommandHandler('preview', preview))
    dp.add_handler(MessageHandler(Filters.poll, receive_poll))
    dp.add_handler(CommandHandler('help', help_handler))
    """

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('dogo',dogo))
    dp.add_handler(CommandHandler('gatineo',gatineo))
    dp.add_handler(CommandHandler('clima',get_weather))
    dp.add_handler(CommandHandler('piada',piada))
    dp.add_handler(CommandHandler('spotifyme',spotify))
    #dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()