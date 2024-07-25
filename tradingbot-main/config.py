# config.py

# Configurações do Bot de Trading
config = {
    "tp": 0.05,  # Take Profit +5%
    "sl": 0.01,  # Stop Loss -1%
    "timeframe_4h": 240,  # 4 horas
    "timeframe_1d": 'D',  # 1 dia
    "mode": 1,  # 1 - Isolated, 0 - Cross
    "leverage": 10,  # Alavancagem desejada
    "max_leverage": 15,  # Alavancagem máxima permitida
    "qty": 20,  # Quantidade de USDT para uma ordem
    "max_pos": 50  # Máximo de ordens atuais
}
