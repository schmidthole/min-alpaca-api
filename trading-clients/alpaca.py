#!/usr/bin/env python3

import requests

# minimum allowed sec between requests to stay under rate limits
REQ_SPACING_S = 0.3


class AlpacaClient:
    def __init__(
        self,
        apikey,
        secret,
        baseurl="https://api.alpaca.markets/",
        dataurl="https://data.alpaca.markets/",
    ):
        self.apikey = apikey
        self.secret = secret
        self.baseurl = baseurl
        self.dataurl = dataurl

    def _make_headers(self):
        return {"APCA-API-KEY-ID": self.apikey, "APCA-API-SECRET-KEY": self.secret}

    def _get(self, path, version="v2", payload={}):
        rsp = requests.get(
            f"{self.baseurl}{version}{path}",
            headers=self._make_headers(),
            params=payload,
        )
        rsp.raise_for_status()
        return rsp.json()

    def _data_get(self, path, version="v1", payload={}):
        rsp = requests.get(
            f"{self.dataurl}{version}{path}",
            headers=self._make_headers(),
            params=payload,
        )
        rsp.raise_for_status()
        return rsp.json()

    def _post(self, path, version="v2", json={}):
        rsp = requests.post(
            f"{self.baseurl}{version}{path}", headers=self._make_headers(), json=json
        )
        rsp.raise_for_status()
        return rsp.json()

    def _put(self, path, version="v2", json={}):
        rsp = requests.put(
            f"{self.baseurl}{version}{path}", headers=self._make_headers(), json=json
        )
        rsp.raise_for_status()
        return rsp.json()

    def _delete(self, path, version="v2", payload={}):
        rsp = requests.delete(
            f"{self.baseurl}{version}{path}",
            headers=self._make_headers(),
            params=payload,
        )
        rsp.raise_for_status()
        return rsp

    def account(self):
        return self._get("/account")

    def order(self, orderid):
        return self._get(f"/orders/{orderid}")

    def orders(self):
        return self._get("/orders")

    def place_market_order(self, symbol, qty, side, time_in_force):
        payload = {
            "symbol": symbol,
            "qty": qty,
            "side": side,
            "type": "market",
            "time_in_force": time_in_force,
        }
        return self._post("/orders", json=payload)

    def place_stop_order(self, symbol, qty, side, time_in_force, stop):
        payload = {
            "symbol": symbol,
            "qty": qty,
            "side": side,
            "type": "stop",
            "time_in_force": time_in_force,
            "stop_price": stop,
        }
        return self._post("/orders", json=payload)

    def cancel_order(self, orderid):
        return self._delete(f"/orders/{orderid}")

    def positions(self):
        return self._get("/positions")

    def position(self, symbol):
        return self._get(f"/positions/{symbol}")

    def close_positions(self):
        return self._delete("/positions")

    def close_position(self, symbol):
        return self._delete(f"/positions/{symbol}")

    def assets(self):
        return self._get("/assets")

    def clock(self):
        return self._get("/clock")

    def barset(self, symbols, timeframe="day", limit=500):
        payload = {"symbols": symbols, "limit": limit}
        return self._data_get(f"/bars/{timeframe}", payload=payload)

    def last_trade(self, symbol):
        return self._data_get(f"/last/stocks/{symbol}")

    def create_watchlist(self, name, symbols):
        payload = {"name": name, "symbols": symbols}
        return self._post("/watchlists", json=payload)

    def delete_watchlist(self, watchlist_id):
        return self._delete(f"/watchlists/{watchlist_id}")

    def all_watchlists(self):
        return self._get("/watchlists")

    def get_watchlist(self, watchlist_id):
        return self._get(f"/watchlists/{watchlist_id}")

    def add_to_watchlist(self, watchlist_id, symbol):
        payload = {"symbol": symbol}
        return self._post(f"/watchlists/{watchlist_id}", json=payload)

    def remove_from_watchlist(self, watchlist_id, symbol):
        return self._delete(f"/watchlists/{watchlist_id}/{symbol}")
