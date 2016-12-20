#MyTaskBot
from telegram import ReplyKeyboardMarkup
from telegram.ext import JobQueue
from telegram.ext import Updater, CommandHandler, Job, ConversationHandler, RegexHandler, MessageHandler, Filters

import logging
from datetime import *
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


def end_conversation():
    log.info("Exiting conversation handler")
    return ConversationHandler.END

#Constants
CHOOSING = 1
GETTING_DATE_AND_TIME = 2
GETTING_TASK_TEXT = 3
GETTING_TARGET = 4
CHANGE = 5
GETTING_TIME = 6
CHOOSING_TASK_ACTION = 7
CHOOSING_TARGET_ACTION = 8
TASK_TO_DELETE = 9
TASK_TO_DONE = 10
TARGET_TO_DELETE = 11
TARGET_TO_DONE = 12

show_choose_reply_keyboard = [['Delete', 'Make done'], ['Exit']]
show_choose_markup = ReplyKeyboardMarkup(show_choose_reply_keyboard, one_time_keyboard=True)

task_reply_keyboard = [["Today", "Tomorrow"], ["Custom"], ['Cancel']]
task_markup = ReplyKeyboardMarkup(task_reply_keyboard, one_time_keyboard=True)

show_reply_keyboard = [['Show Tasks', 'Show Targets'], ['Cancel']]
show_markup = ReplyKeyboardMarkup(show_reply_keyboard, one_time_keyboard=True)

gmt_reply_keyboard = [['Change','Cancel']]
gmt_markup = ReplyKeyboardMarkup(gmt_reply_keyboard, one_time_keyboard=True)


db = Database()
users = dict()


def check_user(update, user_id):
    if not db.is_user(user_id):
        user = User(
            name=update.message.from_user.first_name,
            chat_id=update.message.chat_id,
            user_id=update.message.from_user.id
        )
        db.register_user(user)
    if user_id not in users:
        user = User(
            name=update.message.from_user.first_name,
            chat_id=update.message.chat_id,
            user_id=update.message.from_user.id
        )
        users[user_id] = user


@logger_decorator
def start_cmd(bot, update):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input command: " + "/start")
    check_user(update, user_id)
    update.message.reply_text('Hi! Use /help to get help')


@logger_decorator
def help_cmd(bot, update):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input command: " + "/help")
    update.message.reply_text('---Help---\n'
                              '/task - to add new Task\n'
                              '/target - to add new Target\n'
                              '/show - to see your Tasks or Targets and do operations with them(done del)\n'
                              '/GMT - to change your time zone\n'
                              )


@logger_decorator
def alarm(bot, job):
    bot.sendMessage(job.context[0], text=job.context[2] + ", remind you about your task:\n" + job.context[1])


@logger_decorator
def show_cmd(bot, update):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input command: " + "/show")
    log.info("user with id: " + str(user_id) + " Starting conversation handler")
    update.message.reply_text(
        "What do you want me to show?",
        reply_markup=show_markup
    )
    return CHOOSING


def gmt_to_str(gmt):
    if gmt > 0:
        return "+" + str(gmt)
    else:
        return str(gmt)


@logger_decorator
def change_gmt_cmd(bot, update):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input command: " + "/GMT")
    log.info("user with id: " + str(user_id) + " Starting conversation handler")
    check_user(update, user_id)
    update.message.reply_text(
        'Now, your time zone is GMT ' + gmt_to_str(users[user_id].gmt) + "\n",
        reply_markup=gmt_markup
    )
    return CHOOSING


@logger_decorator
def change_gmt(bot, update):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    try:
        new_gmt = int(update.message.text)
    except:
        update.message.reply_text(
            'Invalid input, please try again',
        )
        return CHANGE
    if new_gmt > 12 or new_gmt < -11:
        update.message.reply_text(
            'Invalid GMT (it must be in [-11,+12]), please try again',
        )
        return CHANGE

    users[user_id].gmt = new_gmt
    # Записать в базу, что юзер изменил часововй пояс
    update.message.reply_text(
        'Ok, your new time zone is GMT' + gmt_to_str(new_gmt)
    )
    return end_conversation()


@logger_decorator
def get_new_gmt(bot, update):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    update.message.reply_text(
        'Write new GMT(it must be in [-11,+12])',
    )
    return CHANGE



@logger_decorator
def add_task(bot, update):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    update.message.reply_text(
        "Choose",
        reply_markup=task_markup,
    )
    return CHOOSING


@logger_decorator
def add_custom_task(bot, update):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    update.message.reply_text(
        "Write date and time of Task in form DD.MM.YY HH:MM\n"
        "for example 12.12.16 4:20"
    )
    return GETTING_DATE_AND_TIME


@logger_decorator
def add_today_task(bot, update, user_data):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    update.message.reply_text(
        "Write time of Task in form HH:MM\n"
        "for example 14:20"
    )
    user_data["data"] = datetime.date.today()
    return GETTING_TIME


@logger_decorator
def add_tomorrow_task(bot, update, user_data):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    update.message.reply_text(
        "Write time of Task in form HH:MM\n"
        "for example 14:20"
    )
    user_data["data"] = datetime.date.today() + datetime.timedelta(days=1)
    print(user_data["data"])
    return GETTING_TIME


@logger_decorator
def get_time(bot, update, user_data):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    try:
        t = datetime.datetime.strptime(update.message.text, '%H:%M').time()
        print(t)
    except ValueError:
        log.info("user with id: " + str(user_id) + " make a mistake")
        update.message.reply_text(
            "You made a mistake, please try again\n\n"
            "Write time of Task in form HH:MM\n"
            "for example 14:20"
        )
        return GETTING_TIME
    data_time = datetime.datetime.combine(user_data["data"], t)
    user_data["dtime"] = data_time
    update.message.reply_text("Write your task:")
    return GETTING_TASK_TEXT


@logger_decorator
def get_date_and_time(bot, update, user_data):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    if update.message.text == 'Cancel':
        return end_conversation()
    try:
        date_time = datetime.datetime.strptime(update.message.text, '%d.%m.%y %H:%M')
    except ValueError:
        log.info("user with id: " + str(user_id) + " make a mistake")
        update.message.reply_text(
            "You made a mistake, please try again\n\n"
            "Write date and time of Task in form DD.MM.YY HH:MM\n"
            "for example 12.12.16 4:20"
        )
        return GETTING_DATE_AND_TIME
    if date_time < datetime.datetime.now():
        update.message.reply_text(
            'Sorry we can not go back to future!\n\n'
            'Write date and time of Task in form DD.MM.YY HH:MM\n'
            'for example 12.12.16 4:20'
        )
        return GETTING_DATE_AND_TIME
    user_data['dtime'] = date_time
    update.message.reply_text("Write your task:")
    return GETTING_TASK_TEXT


def to_gmt0(date_time, gmt):
    return date_time - datetime.timedelta(seconds=gmt*60*60) + datetime.timedelta(seconds=config.SERVER_GMT*60*60)


def from_gmt0(date_time, gmt):
    return date_time + datetime.timedelta(seconds=gmt*60*60) - datetime.timedelta(seconds=config.SERVER_GMT*60*60)


@logger_decorator
def get_task_text(bot, update, user_data):
    user_id = update.message.from_user.id
    check_user(update, user_id)
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)

    date_time = user_data['dtime']
    if date_time < datetime.datetime.now():
        update.message.reply_text(
            'Sorry we can not go back to future!\n\n'
            'Write date and time of Task in form DD.MM.YY HH:MM\n'
            'for example 12.12.16 4:20'
        )
        return GETTING_DATE_AND_TIME
    task = Task(
        user_id=user_id,
        text=update.message.text,
        dtime=to_gmt0(date_time, users[user_id].gmt)
    )
    db.add_task(user_id, task)
    user_data.clear()
    update.message.reply_text("OK, I will memorise it")
    return end_conversation()


@logger_decorator
def add_target(bot, update):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    update.message.reply_text(
        "Give me your Target"
    )
    return GETTING_TARGET


@logger_decorator
def get_target_text(bot, update):
    assert bot is not None, "bot is None!"
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    check_user(update, user_id)
    target = Target(user_id=user_id, text=update.message.text)
    db.add_target(user_id, target)
    update.message.reply_text("OK, I will memorise it")
    return end_conversation()


@logger_decorator
def show_task(bot, update, user_data):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    msg = '{icon} You tasks, {user_name} {last_name}!'.format(
        icon='\U000023F0',
        user_name=update.message.from_user.first_name,
        last_name=update.message.from_user.last_name
    )
    check_user(update, user_id)
    tasks = db.get_tasks(user_id)
    user_data["list"] = list()
    if len(tasks) == 0:
        msg += '\n You haven\'t got Tasks!'
        update.message.reply_text(msg)
        return end_conversation()
    else:
        i = 0
        for task in tasks:
            user_data["list"].append(task)
            i += 1
            msg += '\n {ind}: {data} - {text}'.format(
                ind=i,
                data=from_gmt0(task.datetime, users[user_id].gmt).strftime('%d.%m.%y  %H:%M'),
                text=task.text
            )
        update.message.reply_text(msg, reply_markup=show_choose_markup)
    return CHOOSING_TASK_ACTION


def check_number(update, text, data_list):
    try:
        n = int(text)
    except ValueError:
        update.message.reply_text(
            "You made a mistake, please try again\n\n"
            "Input number of task, that you want to delete\n"
            "(0 - to exit)"
        )
        return -1
    if n == 0:
        return 0
    if n < 1 or n > len(data_list):
        update.message.reply_text(
            "No such number, please try again\n\n"
            "Input number of task, that you want to delete\n"
            "(0 - to exit)"
        )
        return -1
    return n


@logger_decorator
def delete_task_message(bot, update, user_data):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    update.message.reply_text("Input number of task, that you want to delete\n (0 - to exit)")
    return TASK_TO_DELETE


@logger_decorator
def make_task_done_message(bot, update, user_data):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    update.message.reply_text("Input number of task, that you want make done\n (0 - to exit)")
    return TASK_TO_DONE


@logger_decorator
def make_task_done(bot, update, user_data):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    n = check_number(update=update, text=update.message.text, data_list=user_data["list"])
    if n == -1:
        return TASK_TO_DONE
    if n == 0:
        return end_conversation()
    db.done_task(user_data["list"][n-1])
    update.message.reply_text("Task marked as done")
    return end_conversation()


@logger_decorator
def delete_task(bot, update, user_data):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    n = check_number(update=update, text=update.message.text, data_list=user_data["list"])
    if n == -1:
        return TASK_TO_DELETE
    if n == 0:
        return end_conversation()
    db.remove_task(user_data["list"][n-1])
    update.message.reply_text("Task deleted")
    return end_conversation()


@logger_decorator
def show_target(bot, update, user_data):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    msg = '{icon} You targets, {user_name} {last_name}!'.format(
        icon='\U000023F3',
        user_name=update.message.from_user.first_name,
        last_name=update.message.from_user.last_name
    )

    check_user(update, user_id)
    targets = db.get_target(user_id)
    user_data["list"] = list()
    if len(targets) == 0:
        msg += '\n You haven\'t got Targets!'
        update.message.reply_text(msg)
        return end_conversation()
    else:
        i = 0
        for target in targets:
            user_data["list"].append(target)
            i += 1
            msg += '\n {ind}: {text}'.format(
                ind=i,
                text=target.text
            )
    update.message.reply_text(msg, reply_markup=show_choose_markup)
    return CHOOSING_TARGET_ACTION


@logger_decorator
def delete_target_message(bot, update, user_data):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    update.message.reply_text("Input number of target, that you want to delete\n (0 - to exit)")
    return TARGET_TO_DELETE


@logger_decorator
def make_target_done_message(bot, update, user_data):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    update.message.reply_text("Input number of target, that you want make done\n (0 - to exit)")
    return TARGET_TO_DONE


@logger_decorator
def make_target_done(bot, update, user_data):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    n = check_number(update=update, text=update.message.text, data_list=user_data["list"])
    if n == -1:
        return TARGET_TO_DONE
    if n == 0:
        return end_conversation()
    db.done_target(user_data["list"][n-1])
    update.message.reply_text("Target marked as done")
    return end_conversation()


@logger_decorator
def delete_target(bot, update, user_data):
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    n = check_number(update=update, text=update.message.text, data_list=user_data["list"])
    if n == -1:
        return TARGET_TO_DELETE
    if n == 0:
        return end_conversation()
    db.remove_target(user_data["list"][n-1])
    update.message.reply_text("Target deleted")
    return end_conversation()




@logger_decorator
def cancel(bot, update):
    assert bot is not None, "bot is None!"
    assert update is not None, "update is not None!"
    # some text for user
    user_id = update.message.from_user.id
    log.info("user with id: " + str(user_id) + " input text: " + update.message.text)
    return end_conversation()


@logger_decorator
def error(bot, update, err):
    logger.warn('Update "%s" caused error "%s"' % (update, err))


@logger_decorator
def error_message(bot, update):
    update.message.reply_text(
        "Invalid input!!!"
    )
    return end_conversation()


@logger_decorator
def update(bot, job):
    log.info(" starting update")
    t = datetime.datetime.now()
    tasks = db.get_recent_tasks(t.strftime('%Y-%m-%d %H:%M'))
    for task in tasks:
        user = users[task.user_id]
        bot.sendMessage(user.chat_id, text=user.name + ", remind you about your task:\n" + task.text)
        db.done_task(task)
    log.info("update finished")


def main():
    global users
    users = db.get_all_users()
    updater = Updater(config.TOKEN)
    jq = JobQueue(updater.bot)
    job = Job(
        update,
        60,
        repeat=True,
        context=None
    )
    delta = 60 - datetime.datetime.now().second
    if delta == 60:
        delta = 0
    jq.put(job, delta)
    jq.start()

    task_handler = ConversationHandler(
        entry_points=[CommandHandler('task', add_task)],
        states={
            CHOOSING: [
                RegexHandler('^Today$', add_today_task, pass_user_data=True),
                RegexHandler('^Tomorrow$', add_tomorrow_task, pass_user_data=True),
                RegexHandler('^Custom$', add_custom_task, pass_user_data=False),
                RegexHandler('^Cancel$', cancel, pass_user_data=False),
                MessageHandler(Filters.text, error_message, pass_user_data=False),
            ],
            GETTING_DATE_AND_TIME: [
                MessageHandler(Filters.text, get_date_and_time, pass_user_data=True)
            ],
            GETTING_TIME: [
                MessageHandler(Filters.text, get_time, pass_user_data=True),
            ],
            GETTING_TASK_TEXT: [
                MessageHandler(Filters.text, get_task_text, pass_user_data=True,)
            ],
        },
        fallbacks=[RegexHandler('^Cancel$', cancel)]
    )
    dp = updater.dispatcher

    target_handler = ConversationHandler(
        entry_points=[CommandHandler('target', add_target)],
        states={
            GETTING_TARGET: [
                MessageHandler(Filters.text, get_target_text, pass_user_data=False),
            ],
        },
        fallbacks=[RegexHandler('^Cancel$', cancel)]
    )

    show_handler = ConversationHandler(
        entry_points=[CommandHandler('show', show_cmd)],
        states={
            CHOOSING: [
                RegexHandler('^Show Tasks$', show_task, pass_user_data=True),
                RegexHandler('^Show Targets$', show_target, pass_user_data=True),
                RegexHandler('^Cancel$', cancel, pass_user_data=False),
                MessageHandler(Filters.text, error_message, pass_user_data=False),
            ],
            CHOOSING_TARGET_ACTION: [
                RegexHandler('^Delete$', delete_target_message, pass_user_data=True),
                RegexHandler('^Make done$', make_target_done_message, pass_user_data=True),
                MessageHandler(Filters.text, error_message, pass_user_data=False),
            ],
            CHOOSING_TASK_ACTION: [
                RegexHandler('^Delete$', delete_task_message, pass_user_data=True),
                RegexHandler('^Make done$', make_task_done_message, pass_user_data=True),
                MessageHandler(Filters.text, error_message, pass_user_data=False),
            ],
            TASK_TO_DELETE: [
                MessageHandler(Filters.text, delete_task, pass_user_data=True, )
                            ],
            TASK_TO_DONE: [
                MessageHandler(Filters.text, make_task_done, pass_user_data=True, )
            ],
            TARGET_TO_DELETE: [
                MessageHandler(Filters.text, delete_target, pass_user_data=True, )
                            ],
            TARGET_TO_DONE: [
                MessageHandler(Filters.text, make_target_done, pass_user_data=True, )
            ],



        },
        fallbacks=[
            RegexHandler('^Cancel$', cancel),
            RegexHandler('^Exit', cancel),
        ]
    )

    gmt_handler = ConversationHandler(
        entry_points=[CommandHandler('GMT', change_gmt_cmd)],
        states={
            CHOOSING: [
                RegexHandler('^Change$', get_new_gmt, pass_user_data=False)
            ],
            CHANGE: [
                MessageHandler(Filters.text, change_gmt,),
            ],
        },
        fallbacks=[RegexHandler('^Cancel$', cancel)]
    )

    dp.add_handler(show_handler)
    dp.add_handler(task_handler)
    dp.add_handler(target_handler)
    dp.add_handler(gmt_handler)
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
