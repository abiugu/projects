from pybit.unified_trading import HTTP
import pandas as pd
from datetime import datetime
from keys import api, secret
from config import config

session = HTTP(
    api_key=api,
    api_secret=secret
)

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

# Função para colocar ordens de mercado com TP e SL
def place_order_market(symbol, side, last_trade_time):
    try:
        price_precision, qty_precision = get_precisions(symbol)
        mark_price = float(session.get_tickers(category='linear', symbol=symbol)['result']['list'][0]['markPrice'])
        print(f'Placing {side} order for {symbol}. Mark price: {mark_price}')
        
        leveraged_qty = config["qty"] * config["leverage"]  # qtd * leverage
        order_qty = round(leveraged_qty / mark_price, qty_precision)
        
        tp_price = round(mark_price * (1 + config["tp"] if side == 'buy' else 1 - config["tp"]), price_precision)
        sl_price = round(mark_price * (1 - config["sl"] if side == 'buy' else 1 + config["sl"]), price_precision)

        # session.set_leverage(
        #     category='linear',
        #     symbol=symbol,
        #     buyLeverage=config["leverage"],
        #     sellLeverage=config["leverage"]
        # )
        
        if side == 'buy':
            resp = session.place_order(
                category='linear',
                symbol=symbol,
                side='Buy',
                orderType='Market',
                qty=order_qty,
                takeProfit=tp_price,
                stopLoss=sl_price,
                tpTriggerBy='LastPrice',
                slTriggerBy='LastPrice'
            )
        elif side == 'sell':
            resp = session.place_order(
                category='linear',
                symbol=symbol,
                side='Sell',
                orderType='Market',
                qty=order_qty,
                takeProfit=tp_price,
                stopLoss=sl_price,
                tpTriggerBy='LastPrice',
                slTriggerBy='LastPrice'
            )
        
        print(resp)
        if 'result' in resp and 'orderId' in resp['result']:
            last_trade_time[symbol] = datetime.now()  # Atualiza o timestamp da última negociação
            
            # Simular o resultado da ordem
            kl_4h = klines(symbol, config["timeframe_4h"])
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

            return mark_price, tp_price, sl_price, close_price, result
    except Exception as err:
        print(f"Error placing {side} order for {symbol}: {err}")
        return None, None, None, None, "error"
