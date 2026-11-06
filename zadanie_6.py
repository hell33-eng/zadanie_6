import requests

API_URL = "https://api.coingecko.com/api/v3/simple/price"

# Список популярных монет: id в CoinGecko -> (название, тикер)
COINS = {
    "bitcoin":     ("Bitcoin",  "BTC"),
    "ethereum":    ("Ethereum", "ETH"),
    "tether":      ("Tether",   "USDT"),
    "binancecoin": ("BNB",      "BNB"),
    "solana":      ("Solana",   "SOL"),
    "ripple":      ("XRP",      "XRP"),
    "cardano":     ("Cardano",  "ADA"),
    "dogecoin":    ("Dogecoin", "DOGE"),
    "toncoin":     ("Toncoin",  "TON"),
}

AUTO_OPTIONS = {"Выкл": 0, "30 секунд": 30, "1 минута": 60, "5 минут": 300}


def fetch_prices(timeout: float = 10.0) -> dict:
    """Возвращает {id: {"usd": цена, "usd_24h_change": изменение}}.

    Бросает RuntimeError с понятным сообщением, если что-то пошло не так.
    """
    params = {
        "ids": ",".join(COINS),
        "vs_currencies": "usd",
        "include_24hr_change": "true",
    }
    try:
        response = requests.get(API_URL, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        raise RuntimeError("Сервер не ответил вовремя. Проверьте соединение.")
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Нет соединения с интернетом.")
    except ValueError:
        raise RuntimeError("Сервер вернул некорректный ответ.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Ошибка запроса: {e}")

    if not isinstance(data, dict):
        raise RuntimeError("Неожиданный формат ответа API.")
    return data
