#!/usr/bin/env python3

import requests


class IEXClient:
    def __init__(self, token, baseurl='https://cloud.iexapis.com/'):
        self.token = token
        self.baseurl = baseurl

    def _get(self, path, version='beta', params={}):
        params['token'] = self.token
        rsp = requests.get(f'{self.baseurl}{version}{path}', params=params)
        rsp.raise_for_status()
        return rsp.json()

    def earnings(self, symbol, last=5, period='quarter'):
        params = {
            'period': period
        }
        return self._get(f'/stock/{symbol}/earnings/{last}', params=params)

    def sector_performance(self):
        return self._get('/stock/market/sector-performance')

    def ohlc(self, symbol):
        return self._get(f'/stock/{symbol}/ohlc')

    def balance_sheet(self, symbol):
        return self._get(f'/stock/{symbol}/balance-sheet')

    def income_statement(self, symbol):
        return self._get(f'/stock/{symbol}/income')

    def cash_flow(self, symbol):
        return self._get(f'/stock/{symbol}/cash-flow')

    def historical(self, symbol):
        return self._get(f'/stock/{symbol}/chart/6m')
