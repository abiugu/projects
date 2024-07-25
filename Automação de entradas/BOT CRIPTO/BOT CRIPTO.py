from keys import api, secret
from pybit.unified_trading import HTTP
import pandas as pd
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from time import sleep
import threading
from finta import TA

session = HTTP(
    api_key=api,
    api_secret=secret
)

# Configuração
tp = 0.1  # Take Profit +10%
sl = 0.009  # Stop Loss -0.9%
timeframe_4h = 240  # 4 horas
timeframe_1d = 'D'  # 1 dia
mode = 1  # 1 - Isolated, 0 - Cross
leverage = 10  # Alavancagem desejada
max_leverage = 15  # Alavancagem máxima permitida
qty = 20  # Quantidade de USDT para uma ordem
max_pos = 50  # Máximo de ordens atuais

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

tree = ttk.Treeview(root, columns=("Symbol", "Signal", "Timestamp", "Entry Price", "Close Price", "Result", "Balance"), show='headings')
tree.heading("Symbol", text="Symbol")
tree.heading("Signal", text="Signal")
tree.heading("Timestamp", text="Timestamp")
tree.heading("Entry Price", text="Entry Price")
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
def update_log(symbol, signal, timestamp, entry_price, close_price, result, balance):
    formatted_trade = (symbol, signal, timestamp, entry_price, close_price, result, balance)
    tree.insert("", "end", values=formatted_trade)
    root.update_idletasks()

# Função para atualizar o rótulo do saldo no Tkinter
def update_balance_label(balance):
    balance_label.config(text=f"Balance: {balance:.2f} USDT")
    root.update_idletasks()

# Função para obter o saldo na conta de Derivativos Bybit (em USDT)
def get_balance():
    try:
        resp = session.get_wallet_balance(accountType="UNIFIED", coin="USDT")['result']['list'][0]['coin'][0]['walletBalance']
        return float(resp)
    except Exception as err:
        print(f"Error getting balance: {err}")
        return None

# Função para obter todos os símbolos disponíveis no mercado de Derivativos
def get_tickers():
    try:
        resp = session.get_tickers(category="linear")['result']['list']
        symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "LINKUSDT", "LTCUSDT", "PENDLEUSDT"]
        return symbols
    except Exception as err:
        print(f"Error getting tickers: {err}")
        return []

# Função para obter klines de um símbolo específico
def klines(symbol, interval, limit=500):
    try:
        resp = session.get_kline(
            category='linear',
            symbol=symbol,
            interval=interval,
            limit=limit
        )['result']['list']
        resp = pd.DataFrame(resp)
        resp.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Turnover']
        resp['Time'] = pd.to_numeric(resp['Time'])  # Converte para numérico antes de usar to_datetime
        resp['Time'] = pd.to_datetime(resp['Time'], unit='ms')  # Corrige a conversão de timestamp
        resp = resp.set_index('Time')
        resp = resp.astype(float)
        return resp
    except Exception as err:
        print(f"Error getting klines for {symbol}: {err}")
        return pd.DataFrame()

# Função para obter posições atuais
def get_positions():
    try:
        resp = session.get_positions(
            category='linear',
            settleCoin='USDT'
        )['result']['list']
        pos = {elem['symbol']: elem for elem in resp}
        return pos
    except Exception as err:
        print(f"Error getting positions: {err}")
        return {}

# Função para obter o número de dígitos decimais para preço e quantidade
def get_precisions(symbol):
    try:
        resp = session.get_instruments_info(
            category='linear',
            symbol=symbol
        )['result']['list'][0]
        price = resp['priceFilter']['tickSize']
        qty = resp['lotSizeFilter']['qtyStep']
        price_precision = len(price.split('.')[1]) if '.' in price else 0
        qty_precision = len(qty.split('.')[1]) if '.' in qty else 0
        return price_precision, qty_precision
    except Exception as err:
        print(f"Error getting precisions for {symbol}: {err}")
        return 0, 0

# Função para simular ordens de mercado com TP e SL
def simulate_order_market(symbol, side):
    try:
        price_precision, qty_precision = get_precisions(symbol)
        mark_price = float(session.get_tickers(category='linear', symbol=symbol)['result']['list'][0]['markPrice'])
        print(f'[SIMULATION] Placing {side} order for {symbol}. Mark price: {mark_price}')
        
        leveraged_qty = qty * leverage
        order_qty = round(leveraged_qty / mark_price, qty_precision)
        
        actual_leverage = min(leverage, max_leverage)
        tp_price = round(mark_price * (1 + tp if side == 'buy' else 1 - tp), price_precision)
        sl_price = round(mark_price * (1 - sl if side == 'buy' else 1 + sl), price_precision)
        
        # Simular resposta da ordem
        resp = {
            'result': {
                'orderId': 'simulation_order_id'
            }
        }
        print(resp)
        if 'result' in resp and 'orderId' in resp['result']:
            last_trade_time[symbol] = datetime.now()  # Atualiza o timestamp da última negociação
            
            # Simular o resultado da ordem
            kl_4h = klines(symbol, timeframe_4h)
            future_prices = kl_4h[kl_4h.index > datetime.now()].copy()
            close_price = None
            result = "pending"
            
            if side == 'buy':
                if (future_prices['High'] >= tp_price).any():
                    close_price = future_prices[future_prices['High'] >= tp_price]['High'].iloc[0]
                    result = "win"
                elif (future_prices['Low'] <= sl_price).any():
                    close_price = future_prices[future_prices['Low'] <= sl_price]['Low'].iloc[0]
                    result = "loss"
            elif side == 'sell':
                if (future_prices['Low'] <= tp_price).any():
                    close_price = future_prices[future_prices['Low'] <= tp_price]['Low'].iloc[0]
                    result = "win"
                elif (future_prices['High'] >= sl_price).any():
                    close_price = future_prices[future_prices['High'] >= sl_price]['High'].iloc[0]
                    result = "loss"

            return mark_price, close_price, result
    except Exception as err:
        print(f"Error placing {side} order for {symbol}: {err}")
        return None, None, "error"

# Função para calcular o Volume Profile
def calculate_volume_profile(df, bins=20):
    bin_edges = pd.cut(df['Close'], bins=bins, retbins=True)[1]
    volume_profile = [(bin_edges[i], bin_edges[i+1], df[(df['Close'] >= bin_edges[i]) & (df['Close'] < bin_edges[i+1])]['Volume'].sum())
                      for i in range(len(bin_edges) - 1)]
    volume_profile_df = pd.DataFrame(volume_profile, columns=['Low', 'High', 'Volume'])
    volume_profile_df = volume_profile_df.sort_values(by='Volume', ascending=False)
    return volume_profile_df

# Função para gerar sinal de compra/venda baseado em RSI e Volume Profile
def rsi_volume_profile_signal(df_4h):
    rsi = TA.RSI(df_4h)
    volume_profile = calculate_volume_profile(df_4h)
    significant_volume_nodes = volume_profile.head(5)

    signals = []
    for i in range(1, len(df_4h)):
        if rsi.iloc[i] <= 30 and rsi.iloc[i - 1] > 30:
            for _, row in significant_volume_nodes.iterrows():
                if row['Low'] <= df_4h['Close'].iloc[i] <= row['High']:
                    signals.append(('buy', df_4h.index[i]))
                    break
        elif rsi.iloc[i] >= 70 and rsi.iloc[i - 1] < 70:
            for _, row in significant_volume_nodes.iterrows():
                if row['Low'] <= df_4h['Close'].iloc[i] <= row['High']:
                    signals.append(('sell', df_4h.index[i]))
                    break
    return signals

# Função para verificar se deve processar o sinal
def should_process_signal(symbol, signal, timestamp):
    if symbol in last_signals:
        last_signal, last_time = last_signals[symbol]
        if last_signal == signal and (timestamp - last_time).total_seconds() < timeframe_4h * 60 * 60:
            return False
    if symbol in last_trade_time:
        time_since_last_trade = (datetime.now() - last_trade_time[symbol]).total_seconds()
        if time_since_last_trade < timeframe_4h * 60 * 60:
            return False
    last_signals[symbol] = (signal, timestamp)
    return True

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
            kl_4h = klines(symbol, timeframe_4h)
            if kl_4h.empty:
                continue

            # Filtra para incluir apenas os dados do dia atual
            today = datetime.now().date()
            kl_4h_today = kl_4h[kl_4h.index.date == today]

            signals = rsi_volume_profile_signal(kl_4h_today)
            for signal, timestamp in signals:
                if should_process_signal(symbol, signal, timestamp):
                    entry_price, close_price, result = simulate_order_market(symbol, signal)
                    balance = get_balance()
                    if balance:
                        update_balance_label(balance)
                    update_log(symbol, signal, timestamp, entry_price, close_price, result, balance)
        sleep(60)  # Aguardar um minuto antes de verificar novamente

# Função principal
def main():
    threading.Thread(target=monitor_market).start()
    root.mainloop()

if __name__ == "__main__":
    main()
