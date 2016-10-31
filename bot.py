from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, Job, ConversationHandler, RegexHandler, MessageHandler, Filters

import logging
import config
import datetime 


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

CHOOSING, GETTING_DATE_AND_TIME, GETTING_TASK_TEXT, GETTING_TARGET = range(4)

reply_keyboard = [['Task', 'Target'], ['Cancel']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

users = dict()
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi! Use /help to get help')


def help(bot, update):
    update.message.reply_text('---Help---\n /add - to add new Task or \n ')


def alarm(bot, job):
    """Function to send the alarm message"""
    bot.sendMessage(job.context, text='Beep!')


def add(bot, update):
    update.message.reply_text(
        "What do you want to add?",
        reply_markup=markup)

    return CHOOSING


def add_task(bot, update):
    update.message.reply_text(
        "Write date and time of Task in form DD.MM.YY HH:MM"
        "for example 12.12.16 4:20")

    return GETTING_DATE_AND_TIME    


def get_date_and_time(bot, update, user_data):
    # processing lines and memorization time if error return SOME_CONDITION
    update.message.reply_text("Write your task")
    return GETTING_TASK_TEXT
  
    
def get_task_text(bot, update, user_data):
    #get text from user? memoize it and add add job 
    update.message.reply_text("OK, i will remind you to do this task!")
    return ConversationHandler.END


def add_target(bot, update):
    update.message.reply_text(
        "Give me yout Target")   
    return GETTING_TARGET


def get_target_text(bot, update, user_data):
    #get text from user? memoize it and add add to user.targets  
    update.message.reply_text("OK, I will memorise it")
    return ConversationHandler.END

    
def cancel(bot, update):
    #some text for user 
    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater(config.TOKEN)
    
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add)],

        states={
            CHOOSING: [RegexHandler('^Task$',
                                    add_task, pass_user_data=False),
                       RegexHandler('^Target$',
                                    add_target, pass_user_data=False),
                       ],

            GETTING_DATE_AND_TIME: [MessageHandler(Filters.text,
                                           get_date_and_time,
                                           pass_user_data=True),
                            ],
                            
            GETTING_TASK_TEXT: [MessageHandler(Filters.text,
                                           get_task_text,
                                           pass_user_data=True),
                            ],
           

            GETTING_TARGET: [MessageHandler(Filters.text,
                                          get_target_text,
                                          pass_user_data=True),
                           ],
        },

        fallbacks=[RegexHandler('^Cancel$', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", start))  
    dp.add_handler(CommandHandler("help", help))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()