import tkinter as tk
from tkinter import ttk
from time import sleep
import threading
from datetime import datetime
from pybit.unified_trading import HTTP
from keys import api, secret
from strategy import rsi_volume_profile_signal, should_process_signal
from utils import get_balance, get_tickers, klines, simulate_order_market
from config import config

# Variável para controlar a execução do bot
running = True

# Lista para armazenar sinais processados
processed_signals = []

# Dicionário para controlar os pares já negociados e o timestamp da última negociação
last_trade_time = {}

# Dicionário para armazenar os últimos sinais processados para cada símbolo
last_signals = {}

# Tkinter setup
root = tk.Tk()
root.title("Trade Log")

tree = ttk.Treeview(root, columns=("Symbol", "Signal", "Timestamp", "Entry Price", "TP Price", "SL Price", "Close Price", "Result", "Balance"), show='headings')
tree.heading("Symbol", text="Symbol")
tree.heading("Signal", text="Signal")
tree.heading("Timestamp", text="Timestamp")
tree.heading("Entry Price", text="Entry Price")
tree.heading("TP Price", text="TP Price")
tree.heading("SL Price", text="SL Price")
tree.heading("Close Price", text="Close Price")
tree.heading("Result", text="Result")
tree.heading("Balance", text="Balance")
tree.pack(expand=True, fill='both')

result_label = tk.Label(root)
result_label.pack()

# Label para exibir o saldo atual
balance_label = tk.Label(root, text="Balance: Updating...")
balance_label.pack()

# Botão para parar o bot
def stop_bot():
    global running
    running = False

stop_button = tk.Button(root, text="Stop", command=stop_bot)
stop_button.pack()

# Função para atualizar o log no Tkinter
def update_log(symbol, signal, timestamp, entry_price, tp_price, sl_price, close_price, result, balance):
    formatted_trade = (symbol, signal, timestamp, entry_price, tp_price, sl_price, close_price, result, balance)
    tree.insert("", "end", values=formatted_trade)
    root.update_idletasks()

# Função para atualizar o rótulo do saldo no Tkinter
def update_balance_label(balance):
    balance_label.config(text=f"Balance: {balance:.2f} USDT")
    root.update_idletasks()

# Função para monitorar dados em tempo real e executar a estratégia
def monitor_market():
    global running
    initial_balance = get_balance()
    if initial_balance is None:
        print('Cannot connect to API')
        return

    while running:
        symbols = get_tickers()
        for symbol in symbols:
            kl_4h = klines(symbol, config["timeframe_4h"])
            if kl_4h.empty:
                continue

            # Filtra para incluir apenas os dados do dia atual
            today = datetime.now().date()
            kl_4h_today = kl_4h[kl_4h.index.date == today]

            signals = rsi_volume_profile_signal(kl_4h_today)
            for signal, timestamp in signals:
                if should_process_signal(symbol, signal, timestamp, last_signals, last_trade_time):
                    entry_price, tp_price, sl_price, close_price, result = simulate_order_market(symbol, signal, last_trade_time)
                    balance = get_balance()
                    if balance:
                        update_balance_label(balance)
                    update_log(symbol, signal, timestamp, entry_price, tp_price, sl_price, close_price, result, balance)
        sleep(60)  # Aguardar um minuto antes de verificar novamente

# Função principal
def main():
    threading.Thread(target=monitor_market).start()
    root.mainloop()

if __name__ == "__main__":
    main()
