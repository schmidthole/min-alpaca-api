#!/usr/bin/env python3

import requests


class PolygonClient:
    def __init__(self, apikey, baseurl='https://api.polygon.io/'):
        self.apikey = apikey
        self.baseurl = baseurl

    def _get(self, path, version='v1', payload={}):
        params = dict({'apiKey': self.apikey}, **payload)
        rsp = requests.get(f'{self.baseurl}{version}{path}', params=params)
        rsp.raise_for_status()
        return rsp.json()

    def details(self, symbol):
        return self._get(f'/meta/symbols/{symbol}/company')

    def financials(self, symbol, type='Q', limit=16):
        payload = {
            'limit': limit,
            'type': type
        }
        return self._get(f'/reference/financials/{symbol}',
                         version='v2',
                         payload=payload)

    def news(self, symbol):
        return self._get(f'/meta/symbols/{symbol}/news')

    def aggregate(self, symbol, limit=500):
        payload = {'limit': limit}
        return self._get(f'/historic/agg/day/{symbol}', payload=payload)

    def snapshot(self, symbol):
        return self._get(
            f'/snapshot/locale/us/markets/stocks/tickers/{symbol}',
            version='v2')

    def prev(self, symbol):
        return self._get(f'/aggs/ticker/{symbol}/prev', version='v2')

    def lastquote(self, symbol):
        return self._get(f'/last_quote/stocks/{symbol}')
