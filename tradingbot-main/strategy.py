import pandas as pd
from finta import TA
from datetime import datetime
from config import config

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
def should_process_signal(symbol, signal, timestamp, last_signals, last_trade_time):
    if symbol in last_signals:
        last_signal, last_time = last_signals[symbol]
        if last_signal == signal and (timestamp - last_time).total_seconds() < config["timeframe_4h"] * 60 * 60:
            return False
    if symbol in last_trade_time:
        time_since_last_trade = (datetime.now() - last_trade_time[symbol]).total_seconds()
        if time_since_last_trade < config["timeframe_4h"] * 60 * 60:
            return False
    last_signals[symbol] = (signal, timestamp)
    return True
