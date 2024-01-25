import requests
from bs4 import BeautifulSoup
import time

# Configuração do bot Telegram
TOKEN = '6739402312:AAFB-etL3rw9N29myNo5bmdKSvuJ3ppdamY'
CHAT_ID = '6739402312'

# Função para extrair informações e enviar para o bot


def iniciar_bot():
    while True:
        try:
            # URL do site
            url = 'https://livecasino.bet365.com/Play/MegaFireBlazeRoulette'

            # Cabeçalhos para simular um navegador Mozilla
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            # Fazendo a requisição HTTP para obter o HTML da página
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                # Parseando o HTML com BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Encontrando a tabela de resultados anteriores
                tabela_resultados_anteriores = soup.find(
                    'div', class_='roulette-history-results')  # Substitua 'div' pela tag correta

                # Exibindo as informações dos resultados anteriores
                for resultado in tabela_resultados_anteriores.find_all('div', class_='roulette-history-item'):
                    cor_resultado = determinar_cor_resultado_anterior(
                        resultado)
                    print(cor_resultado, end='\t')

                # Adapte conforme necessário para enviar para o bot do Telegram
                # send_telegram_message('Informações extraídas com sucesso!')

                time.sleep(2)  # Espera 2 segundos antes de verificar novamente

            else:
                print(f'Erro ao acessar a página. Status code: {
                      response.status_code}')
                time.sleep(2)  # Espera 2 segundos antes de tentar novamente

        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(2)  # Espera 2 segundos antes de tentar novamente

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


# Iniciar o bot
iniciar_bot()
