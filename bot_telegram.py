from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Substitua 'TOKEN' pelo token do seu bot, que você obtém ao conversar com o @BotFather no Telegram.
TOKEN = '6739402312:AAFB-etL3rw9N29myNo5bmdKSvuJ3ppdamY'

# Função para o comando /start


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Olá! Eu sou o seu bot do Telegram.')

# Função para lidar com mensagens de texto


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def main() -> None:
    # Criação do Updater e passagem do token do bot
    updater = Updater(TOKEN)

    # Obtenção do dispatcher para registrar manipuladores
    dispatcher = updater.dispatcher

    # Registro de manipuladores
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    # Inicialização do bot
    updater.start_polling()

    # Execução do bot até que o usuário pressione Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()

