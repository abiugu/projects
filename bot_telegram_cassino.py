import requests
from bs4 import BeautifulSoup
import time

# Configuração do bot Telegram
TOKEN = '6739402312:AAFB-etL3rw9N29myNo5bmdKSvuJ3ppdamY'
CHAT_ID = '6739402312'

# Função para extrair informações e verificar a sequência estratégica


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

                # Exibe as informações dos resultados anteriores (apenas para debug)
                print("=== Resultados Anteriores ===")
                for resultado in tabela_resultados_anteriores.find_all('div', class_='roulette-history-item'):
                    cor_resultado = determinar_cor_resultado_anterior(
                        resultado)
                    print(cor_resultado, end='\t')
                print("=============================")

                # Verifica a sequência de cores nos resultados anteriores
                if verificar_sequencia_cores_resultados_anteriores(tabela_resultados_anteriores):
                    send_telegram_message('Prepare-se para fazer uma entrada!')

                # Espera 10 segundos antes de verificar novamente
                time.sleep(10)
            else:
                send_telegram_message(f'Erro ao acessar a página. Status code: {
                                      response.status_code}')
                time.sleep(10)  # Espera 10 segundos antes de tentar novamente

        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(10)  # Espera 10 segundos antes de tentar novamente


def determinar_cor_resultado_anterior(resultado):
    # Obtém as classes atribuídas ao resultado anterior
    classes = resultado.get('class', [])

    # Verifica se a classe do resultado anterior indica vermelho, preto ou verde
    if 'roulette-history-item_red' in classes:
        return 'vermelho'
    elif 'roulette-history-item_black' in classes:
        return 'preto'
    elif 'roulette-history-item_green' in classes:
        return 'verde'
    else:
        return 'desconhecida'  # Se a classe não corresponder a nenhuma das cores conhecidas


def verificar_sequencia_cores_resultados_anteriores(tabela_resultados_anteriores):
    sequencia_cores = ['vermelho', 'preto', 'verde']
    cores_encontradas = []

    for resultado in tabela_resultados_anteriores.find_all('div', class_='roulette-history-item'):
        cor_resultado = determinar_cor_resultado_anterior(resultado)
        cores_encontradas.append(cor_resultado)

    if cores_encontradas == sequencia_cores:
        return True
    else:
        return False


def send_telegram_message(message):
    api_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    params = {
        'chat_id': CHAT_ID,
        'text': message,
    }
    requests.post(api_url, params=params)


# Iniciando o bot
iniciar_bot()
