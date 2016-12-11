#MyTaskBot
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, Job, ConversationHandler, RegexHandler, MessageHandler, Filters

import logging
import datetime
from functools import wraps
from db import *

# our files
import config
from classes import *


logging.basicConfig(format='all [%(name)s] %(levelname)s: %(asctime)s - %(message)s',
                    level=logging.NOTSET)

logger = logging.getLogger('bot_API')

log = logging.getLogger('Core')

lite_handler = logging.StreamHandler()
lite_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('lite [%(name)s] %(levelname)s: %(asctime)s - %(message)s')
lite_handler.setFormatter(formatter)

heavy_handler = logging.StreamHandler()
heavy_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('heavy [%(name)s] %(levelname)s: %(asctime)s - %(message)s')
heavy_handler.setFormatter(formatter)

info_file_handler = logging.FileHandler('MyTaskBot.log', 'a')
info_file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('info [%(name)s] %(levelname)s: %(asctime)s - %(message)s')
info_file_handler.setFormatter(formatter)

heavy_file_handler = logging.FileHandler('MyTaskBot.log', 'a')
heavy_file_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('heavy [%(name)s] %(levelname)s: %(asctime)s - %(message)s')
heavy_file_handler.setFormatter(formatter)


log.addHandler(lite_handler)
log.addHandler(heavy_handler)
log.addHandler(info_file_handler)
log.addHandler(heavy_file_handler)


def logger_decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        log.debug('function: {function} started'.format(function=func.__name__))
        return func(self, *args, **kwargs)
    return wrapper


def user_input_logging(input_type, text):
    log.info("user input {type}: {text}".format(type=input_type, text=text))


def end_conversation():
    log.info("Exiting conversation handler")
    return ConversationHandler.END


CHOOSING, GETTING_DATE_AND_TIME, GETTING_TASK_TEXT, GETTING_TARGET = range(1, 5)

add_reply_keyboard = [['Task', 'Target'], ['Cancel']]
add_markup = ReplyKeyboardMarkup(add_reply_keyboard, one_time_keyboard=True)

show_reply_keyboard = [['Show Tasks', 'Show Targets'], ['Cancel']]
show_markup = ReplyKeyboardMarkup(show_reply_keyboard, one_time_keyboard=True)


db = Database()
users = dict()


@logger_decorator
def start_cmd(bot, update):
    log.info("user input command: " + "/start")
    user_id = update.message.from_user.id
    if not db.get_user(user_id):
        db.register_user(user_id, update.message.from_user.first_name)
    if user_id not in users:
        users[user_id] = User(update.message.from_user.first_name, update.message.chat_id)
    update.message.reply_text('Hi! Use /help to get help')


@logger_decorator
def help_cmd(bot, update):
    log.info("user input command: " + "/help")
    update.message.reply_text('---Help---\n /add - to add new Task or Target\n /show - to see your Tasks or Targets\n')


@logger_decorator
def alarm(bot, job):
    bot.sendMessage(job.context[0], text=job.context[2] + ", remind you about your task:\n" + job.context[1])


@logger_decorator
def add_cmd(bot, update):
    log.info("user input command: " + "/add")
    log.info("Start conversation handler")
    update.message.reply_text(
        "What do you want to add?",
        reply_markup=add_markup)

    return CHOOSING


@logger_decorator
def show_cmd(bot, update):
    log.info("user input command: " + "/show")
    log.info("Start conversation handler")
    update.message.reply_text(
        "What do you want me to show?",
        reply_markup=show_markup)

    return CHOOSING


@logger_decorator
def add_task(bot, update):
    log.info("user input text: " + update.message.text)
    update.message.reply_text(
        "Write date and time of Task in form DD.MM.YY HH:MM\n"
        "for example 12.12.16 4:20"
    )
    return GETTING_DATE_AND_TIME


@logger_decorator
def get_date_and_time(bot, update, user_data):
    task = Task()
    log.info("user input text: " + update.message.text)
    if update.message.text == 'Cancel':
        return end_conversation()
    try:
        task.set_date_and_time(update.message.text)
    except NameError:
        log.info("User make a mistake")
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


@logger_decorator
def get_task_text(bot, update, user_data, job_queue):
    log.info("user input text: " + update.message.text)
    task = user_data['task']
    task.set_text(update.message.text)

    user_id = update.message.from_user.id

    if not db.get_user(user_id):
        user = User(update.message.from_user.first_name, update.message.chat_id)
        db.register_user(user)

    if user_id not in users:
        user = User(update.message.from_user.first_name, update.message.chat_id)
        users[user_id] = user
    else:
        user = users[user_id]

    db.add_task(user_id, task)

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
        log.error("Index or Value error in adding new Job")
        update.message.reply_text('Sorry, we have an error')
    return end_conversation()


@logger_decorator
def add_target(bot, update):
    log.info("user input text: " + update.message.text)
    assert bot is not None, "bot is None!"
    update.message.reply_text(
        "Give me yout Target"
    )
    return GETTING_TARGET


@logger_decorator
def get_target_text(bot, update):
    assert bot is not None, "bot is None!"
    log.info("user input text: " + update.message.text)
    user_id = update.message.from_user.id

    if not db.get_user(user_id):
        user = User(update.message.from_user.first_name, update.message.chat_id)
        db.register_user(user_id, user.name)
    if user_id not in users:
        user = User(update.message.from_user.first_name, update.message.chat_id)
        users[user_id] = user
    else:
        user = users[user_id]
    target = Target(update.message.text)
    db.add_target(user_id, target)
    user.add_target(target)
    update.message.reply_text("OK, I will memorise it")
    return end_conversation()


@logger_decorator
def show_task(bot, update):
    assert bot is not None, "bot is None!"
    log.info("user input text: " + update.message.text)
    msg = '{icon} You tasks, {user_name} {last_name}!'.format(
        icon='\U000023F0',
        user_name=update.message.from_user.first_name,
        last_name=update.message.from_user.last_name
    )
    user_id = update.message.from_user.id
    user = db.get_user(user_id)
    if user:
        tasks = db.get_tasks(user_id)
        if len(tasks) == 0:
            msg += '\n You haven\'t got Tasks!'
        else:
            i = 0
            for task in tasks:
                i += 1
                msg += '\n {ind}: {data} - {text}'.format(
                    ind=i,
                    data=task.datetime,
                    text=task.text
                )
    else:
        log.error("user with id:" + user_id + "is not found")
        msg += "\n FATAL ERROR, admin not found "


    update.message.reply_text(msg)
    return end_conversation()


@logger_decorator
def show_target(bot, update):
    assert bot is not None, "bot is None!"
    log.info("user input text: " + update.message.text)
    msg = '{icon} You targets, {user_name} {last_name}!'.format(
        icon='\U000023F3',
        user_name=update.message.from_user.first_name,
        last_name=update.message.from_user.last_name
    )
    user_id = update.message.from_user.id

    user = db.get_user(user_id)
    if user:
        targets = db.get_target(user_id)
        if len(targets) == 0:
            msg += '\n You haven\'t got Targets!'
        else:
            i = 0
            for target in targets:
                i += 1
                msg += '\n {ind}: {text}'.format(
                    ind=i,
                    text=target.text
                )

    else:
        log.error("user with id:" + user_id + "is not found")
        msg += "\n FATAL ERROR, admin not found "


    """
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
        log.error("user with id: {id}is not found".format(id=user_id))
        msg += "\n FATAL ERROR, admin not found "
    """
    update.message.reply_text(msg)
    return end_conversation()


@logger_decorator
def cancel(bot, update):
    assert bot is not None, "bot is None!"
    assert update is not None, "update is not None!"
    # some text for user
    log.info("user input text: " + update.message.text)
    return end_conversation()


@logger_decorator
def error(bot, update, err):
    logger.warn('Update "%s" caused error "%s"' % (update, err))


@logger_decorator
def error_message(bot, update):
    update.message.reply_text(
        "ERROR INPUT!!!"
    )
    return end_conversation()


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
                                            pass_user_data=False
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