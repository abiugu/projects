
import requests
from bs4 import BeautifulSoup


def extract_double_results():
    url = "https://blaze-7.com/br/games/double?modal=double_history_index"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar a tabela de resultados do Double
        results_table = soup.find('table', class_='history__double')

        if results_table:
            # Extrair as informações da tabela
            results = []
            for row in results_table.find_all('tr'):
                cells = row.find_all('td')
                if cells:
                    result = {
                        'roll': cells[0].text.strip(),
                        'result': cells[1].text.strip(),
                        'color': cells[2].text.strip(),
                    }
                    results.append(result)

            return results
        else:
            print("Tabela de resultados não encontrada.")
    else:
        print(f"Erro ao acessar a página. Status code: {response.status_code}")

    return None


if __name__ == "__main__":
    double_results = extract_double_results()

    if double_results:
        for result in double_results:
            print(result)
