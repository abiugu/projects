from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import time

# Configuração do bot Telegram
TOKEN = '6739402312:AAFB-etL3rw9N29myNo5bmdKSvuJ3ppdamY'
CHAT_ID = '6739402312'

# Função para extrair informações e verificar a sequência estratégica


def iniciar_bot(update: Update, context: CallbackContext):
    # Configuração do Selenium
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Para execução em background

    # Substitua 'caminho/para/seu/chromedriver' pelo caminho real para o seu chromedriver
    chrome_path = r'caminho\para\seu\chromedriver'

    driver = webdriver.Chrome(
        executable_path=chrome_path, options=chrome_options)

    try:
        # URL do site
        url = 'https://livecasino.bet365.com/Play/MegaFireBlazeRoulette'

        # Fazendo a requisição HTTP para obter o HTML da página usando o Selenium
        driver.get(url)

        # Aguarde o carregamento da página
        time.sleep(5)

        # Pegue o HTML da página após o carregamento completo
        html = driver.page_source

        # Parseando o HTML com BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Encontrando a tabela de resultados anteriores
        tabela_resultados_anteriores = soup.find(
            'div', class_='roulette-history-results')  # Substitua 'div' pela tag correta

        # Exibindo as informações dos resultados anteriores
        for resultado in tabela_resultados_anteriores.find_all('div', class_='roulette-history-item'):
            cor_resultado = determinar_cor_resultado_anterior(resultado)
            context.bot.send_message(
                chat_id=CHAT_ID, text=f'Cor do resultado anterior: {cor_resultado}')

    except Exception as e:
        context.bot.send_message(chat_id=CHAT_ID, text=f'Erro: {e}')

    finally:
        # Feche o navegador ao finalizar
        driver.quit()

# Função para determinar a cor do resultado anterior


def determinar_cor_resultado_anterior(resultado):
    classes = resultado.get('class', [])
    if 'roulette-history-item_red' in classes:
        return 'vermelho'
    elif 'roulette-history-item_black' in classes:
        return 'preto'
    elif 'roulette-history-item_green' in classes:
        return 'verde'
    else:
        return 'desconhecida'


def main():
    # Configuração do bot e adicionando o manipulador de comando
    updater = Updater(token=TOKEN, use_context=True)

    # Registrar um manipulador para o comando 'iniciar'
    updater.dispatcher.add_handler(CommandHandler("iniciar", iniciar_bot))

    # Iniciando o bot
    updater.start_polling()

    # Mantendo o script em execução
    updater.idle()


if __name__ == '__main__':
    main()
