import time
import json
from datetime import datetime

import requests


class Double:
    def __init__(
        self,
        start_date="2023-27-12",
        end_date="2024-26-01",
        save_file=False,
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.save_file = save_file

    def get_current_time_hours(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    def get_blaze_data(self):
        cur_hour = self.get_current_time_hours()
        url = f"https://blaze-7.com/api/roulette_games/history?startDate=2023-12-27T14:27:14.680Z&endDate=2024-01-26T14:27:14.680Z&page=1"

        headers = {
            "Cache-Control": "no-cache",
        }

        r = requests.get(url, headers=headers)

        if r.status_code != 200:
            print(f"Erro ao acessar a página. Status code: {r.status_code}")
            return None

        try:
            json_data = r.json()
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON da resposta: {e}")
            print(f"Conteúdo da resposta: {r.text}")
            return None

        if self.save_file:
            self.save_data_to_file(json.dumps(json_data, indent=2))
        return json_data

    def save_data_to_file(self, data):
        with open("result.json", "w") as f:
            f.write(data)

    def get_total_pages(self, data):
        if data and "total_pages" in data:
            return data["total_pages"]
        else:
            return 0

    def get_only_result_data(self, data):
        if data and "records" in data:
            results = [v["roll"] for v in data["records"]]
            print(results)
        else:
            print("Dados ausentes ou formato inesperado.")


if __name__ == "__main__":
    while True:
        obj = Double(save_file=True)
        data = obj.get_blaze_data()
        obj.get_only_result_data(data)
        # Aguarda 10 segundos antes de fazer a próxima solicitação
        time.sleep(10)
