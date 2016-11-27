from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, Job, ConversationHandler, RegexHandler, MessageHandler, Filters

import logging
import datetime
import sys
from functools import wraps

# our files
import config
from classes import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

CHOOSING, GETTING_DATE_AND_TIME, GETTING_TASK_TEXT, GETTING_TARGET = range(1, 5)

add_reply_keyboard = [['Task', 'Target'], ['Cancel']]
add_markup = ReplyKeyboardMarkup(add_reply_keyboard, one_time_keyboard=True)

show_reply_keyboard = [['Show Tasks', 'Show Targets'], ['Cancel']]
show_markup = ReplyKeyboardMarkup(show_reply_keyboard, one_time_keyboard=True)

users = dict()


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.


def start_cmd(bot, update):
    user_id = update.message.from_user.id
    if user_id not in users:
        users[user_id] = User(update.message.from_user.first_name, update.message.chat_id)
    update.message.reply_text('Hi! Use /help to get help')


def help_cmd(bot, update):
    update.message.reply_text('---Help---\n /add - to add new Task or Target\n /show - to see your Tasks or Targets\n')


def alarm(bot, job):
    bot.sendMessage(job.context[0], text=job.context[2] + ", remind you about your task:\n" + job.context[1])


def add_cmd(bot, update):
    update.message.reply_text(
        "What do you want to add?",
        reply_markup=add_markup)

    return CHOOSING


def show_cmd(bot, update):
    update.message.reply_text(
        "What do you want me to show?",
        reply_markup=show_markup)

    return CHOOSING


def add_task(bot, update):
    update.message.reply_text(
        "Write date and time of Task in form DD.MM.YY HH:MM\n"
        "for example 12.12.16 4:20"
    )
    return GETTING_DATE_AND_TIME


def get_date_and_time(bot, update, user_data):
    task = Task()
    print('\n' + update.message.text + '\n')
    print(type(update.message.text))
    if update.message.text == 'Cancel':
        print("CANCEL")
        return ConversationHandler.END
    try:
        task.set_date_and_time(update.message.text)
    except NameError:
        update.message.reply_text(
            "You made a mistake, please try again\n\n"
            "Write date and time of Task in form DD.MM.YY HH:MM\n"
            "for example 12.12.16 4:20"
        )
        del task
        return GETTING_DATE_AND_TIME
    if (task.datetime - datetime.datetime.now()).days < 0:
        update.message.reply_text(
            'Sorry we can not go back to future!\n\n'
            'Write date and time of Task in form DD.MM.YY HH:MM\n'
            'for example 12.12.16 4:20'
        )
        del task
        return GETTING_DATE_AND_TIME
    user_data['task'] = task
    update.message.reply_text("Write your task:")
    del task
    return GETTING_TASK_TEXT


def get_task_text(bot, update, user_data, job_queue):
    task = user_data['task']
    task.set_text(update.message.text)

    user_id = update.message.from_user.id

    if user_id not in users:
        user = User(update.message.from_user.first_name, update.message.chat_id)
        users[user_id] = user
    else:
        user = users[user_id]
    user.add_task(task)
    user_data.clear()
    try:
        dt = (task.datetime - datetime.datetime.now())
        delta = dt.days * 24 * 60 * 60 + dt.seconds
        job = Job(alarm,
                  delta,
                  repeat=False,
                  context=(user.chat_id, task.text, user.name)
                  )
        job_queue.put(job)
        update.message.reply_text("OK, i will remind you to do this task!")
    except (IndexError, ValueError):
        update.message.reply_text('Sorry, we have an error')
    return ConversationHandler.END


def add_target(bot, update):
    assert bot is not None, "bot is None!"
    update.message.reply_text(
        "Give me yout Target"
    )
    return GETTING_TARGET


def get_target_text(bot, update):
    assert bot is not None, "bot is None!"
    user_id = update.message.from_user.id

    if user_id not in users:
        user = User(update.message.from_user.first_name, update.message.chat_id)
    else:
        user = users[user_id]
    target = Target(update.message.text)
    user.add_target(target)
    update.message.reply_text("OK, I will memorise it")
    return ConversationHandler.END


def show_task(bot, update):
    assert bot is not None, "bot is None!"
    msg = '{icon} You tasks, {user_name} {last_name}!'.format(
        icon='\U000023F0',
        user_name=update.message.from_user.first_name,
        last_name=update.message.from_user.last_name
    )
    user_id = update.message.from_user.id
    if user_id in users:
        user = users[user_id]
        if len(user.tasks) == 0:
            msg += '\n You haven\'t got Tasks!'
        else:
            i = 0
            for task in user.tasks:
                i += 1
                msg += '\n {ind}: {data} - {text}'.format(
                    ind=i,
                    data=task.datetime,
                    text=task.text
                )

    else:
        # этот код пока никогда не выполняется
        # Не смотрите сюда, мы были не в себе
        msg += "\n FATAL ERROR, admin not found "
    update.message.reply_text(msg)
    return ConversationHandler.END


def show_target(bot, update):
    assert bot is not None, "bot is None!"
    msg = '{icon} You targets, {user_name} {last_name}!'.format(
        icon='\U000023F3',
        user_name=update.message.from_user.first_name,
        last_name=update.message.from_user.last_name
    )
    user_id = update.message.from_user.id
    if user_id in users:
        user = users[user_id]
        if len(user.targets) == 0:
            msg += '\n You haven\'t got Tasks!'
        else:
            i = 0
            for target in user.targets:
                i += 1
                msg += '\n {ind}: {text}'.format(
                    ind=i,
                    text=target.text
                )

    else:
        # этот код пока никогда не выполняется
        # Не смотрите сюда, мы были не в себе
        msg += "\n FATAL ERROR, admin not found "
    update.message.reply_text(msg)
    return ConversationHandler.END


def cancel(bot, update):
    assert bot is not None, "bot is None!"
    assert update is not None, "update is not None!"
    # some text for user
    return ConversationHandler.END


def error(bot, update, err):
    logger.warn('Update "%s" caused error "%s"' % (update, err))


def error_message(bot, update):
    update.message.reply_text(
        "ERROR INPUT!!!"
    )
    return ConversationHandler.END

def main():
    updater = Updater(config.TOKEN)

    dp = updater.dispatcher
    add_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add_cmd)],

        states={
            CHOOSING: [RegexHandler('^Task$',
                                    add_task, pass_user_data=False),
                       RegexHandler('^Target$',
                                    add_target, pass_user_data=False),
                       RegexHandler('^Cancel$',
                                    cancel, pass_user_data=False),
                       MessageHandler(Filters.text,
                                      error_message,
                                      pass_user_data=False
                                      ),
                       ],
            GETTING_DATE_AND_TIME: [MessageHandler(Filters.text,
                                                   get_date_and_time,
                                                   pass_user_data=True
                                                   ),
                                    ],
            GETTING_TASK_TEXT: [MessageHandler(Filters.text,
                                               get_task_text,
                                               pass_user_data=True,
                                               pass_job_queue=True
                                               ),
                                ],
            GETTING_TARGET: [MessageHandler(Filters.text,
                                            get_target_text,
                                            pass_user_data=True
                                            ),
                             ],
        },

        fallbacks=[RegexHandler('^Cancel$', cancel)]
    )
    show_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('show', show_cmd)],

        states={
            CHOOSING: [RegexHandler('^Show Tasks$',
                                    show_task, pass_user_data=False),
                       RegexHandler('^Show Targets$',
                                    show_target, pass_user_data=False),
                       ],

        },

        fallbacks=[RegexHandler('^Cancel$', cancel)]
    )

    dp.add_handler(show_conv_handler)
    dp.add_handler(add_conv_handler)
    dp.add_handler(CommandHandler("start", start_cmd))
    dp.add_handler(CommandHandler("help", help_cmd))

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