import configparser
import logging
import re

from telegram.ext import CommandHandler, ConversationHandler, Filters,\
    MessageHandler, PicklePersistence, Updater

# emojis
E_ram = "\U0001F40F"
E_sheep = "\U0001F411"
E_tada = "\U0001F389"
E_wave = "\U0001F44B"

# version
CURRENT_VERSION = "1.0.0"
WHATS_NEW = {}

# states
INPUT = range(1)


def help(botname):
    return "Der " + botname + " grüsst Schafe (" + E_sheep + " und "\
        + E_ram + ") mit einem herzlichen 'määäh'. Schick eine Nachricht "\
        "wie zum Beispiel\n\n"\
        "\t\U00002022 Schau, ein Schaf " + E_sheep + " auf der Wiese!\n"\
        "\t\U00002022 " + E_sheep + " und " + E_ram + " machen määäh.\n\n"\
        "Oder lass das Schaf was sagen, zum Beispiel\n\n"\
        "/say Hi!\n"


# configure logger
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def sheepSay(text):
    return E_sheep + " määäh\n\n" + text


def newerVersionExists(userVersion):
    (major, minor, patch) = userVersion.split(".")
    (cMajor, cMinor, cPatch) = CURRENT_VERSION.split(".")
    return major < cMajor or (major == cMajor and (
        minor < cMinor or (minor == cMinor and patch < cPatch)))


def setDefaultUserData(context, key, value):
    if key not in context.user_data:
        context.user_data[key] = value


def whatsNewMessage(context):
    ctx = context.job.context
    context.bot.send_message(ctx["chat_id"], text=ctx["text"])


def start_cmd(update, context):
    # track current version to send "What's new" messages
    setDefaultUserData(context, "version", CURRENT_VERSION)

    update.message.reply_text(sheepSay(help(context.bot.name)),
                              parse_mode='Markdown',
                              disable_web_page_preview=True)


def help_cmd(update, context):
    update.message.reply_text(sheepSay(help(context.bot.name)),
                              parse_mode='Markdown',
                              disable_web_page_preview=True)


def about_cmd(update, context):
    bot = context.bot.name
    about = "Der " + bot + " ist ein open-source Projekt: "\
        "[github](https://github.com/romanc/maehrobot)\n\n"\
        "Der " + bot + " ist nur möglich dank [python-telegram-bot]"\
        "(https://github.com/python-telegram-bot/python-telegram-bot)."
    update.message.reply_text(sheepSay(about), parse_mode="Markdown")


def say_cmd(update, context):
    filtered = re.sub("/say", "", update.message.text).strip()
    if filtered:
        update.message.reply_text(sheepSay(filtered))
        return ConversationHandler.END
    else:
        update.message.reply_text("Was soll das Schaf sagen?")
        return INPUT


def inputListener(update, context):
    update.message.reply_text(sheepSay(update.message.text))
    return ConversationHandler.END


def greet_cmd(update, context):
    # count sheep
    sheeps = len(re.findall(
        r'[' + E_sheep + '|' + E_ram + ']', update.message.text))

    # greet sheep if we find some
    if sheeps > 0:
        update.message.reply_text("määäh " * sheeps)


def cancel_cmd(update, context):
    update.message.reply_text(sheepSay("Gotta go, määäh! %s" % E_wave))
    return ConversationHandler.END


def maehrobot(token):
    pp = PicklePersistence(filename="maehrobot_data")
    updater = Updater(token, persistence=pp, use_context=True)

    dispatcher = updater.dispatcher
    # needed
    dispatcher.add_handler(CommandHandler("start", start_cmd))
    dispatcher.add_handler(CommandHandler("help", help_cmd))
    dispatcher.add_handler(CommandHandler("hilfe", help_cmd))
    dispatcher.add_handler(CommandHandler("about", about_cmd))

    # /say
    handler = ConversationHandler(
        entry_points=[CommandHandler('say', say_cmd)],
        states={INPUT: [MessageHandler(
            Filters.text & ~Filters.command, inputListener)]},
        fallbacks=[CommandHandler('cancel', cancel_cmd)])
    dispatcher.add_handler(handler)

    # on non command i.e message: count sheeps and greet them
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, greet_cmd))

    # send what's new messages
    user_data = pp.get_user_data()

    for item in pp.get_chat_data().items():
        chat_id = item[0]
        this_user = user_data[chat_id]

        if newerVersionExists(this_user.get("version", "1.0.2")):
            # we have a newer version -> show what's new
            text = "Here's what's new in version %s %s\n\n" % (
                CURRENT_VERSION, E_tada)
            for note in WHATS_NEW[CURRENT_VERSION]:
                text = text + ("\t\U00002022 %s\n" % note)

            # send a what's new message
            updater.job_queue.run_once(whatsNewMessage, 2, context={
                "chat_id": chat_id, "text": sheepSay(text)},
                name="new%s" % str(chat_id))

            # then, update current version
            dispatcher.user_data[chat_id]["version"] = CURRENT_VERSION

    # start bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logger.info("Parsing configfile")
    config = configparser.ConfigParser()
    config.read("config.ini")

    logger.info("Starting maehrobot")
    maehrobot(config['api.telegram.org']['token'])
