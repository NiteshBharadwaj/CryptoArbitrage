#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import math
import requests
import time

app = Flask(__name__)
api = Api(app)


coins = ['BTC','LTC','ETH','REQ','NEO']
fiat = ['USD', 'EUR', 'SGD', 'GBP']

ccys = []
for c in coins:
	ccys.append(c);
for c in fiat:
	ccys.append(c);

price_matrix_json = {'BTC': {'BTC': 1, 'LTC': 63.82, 'ETH': 12.77, 'REQ': 61162.08, 'NEO': 145.75, 'USD': 7652.88, 'EUR': 6501.76, 'SGD': 10835.86, 'GBP': 5669.05}, 'LTC': {'BTC': 0.01567, 'LTC': 1, 'ETH': 0.2001, 'REQ': 958.41, 'NEO': 2.28, 'USD': 119.78, 'EUR': 102.1, 'SGD': 169.8, 'GBP': 88.83}, 'ETH': {'BTC': 0.07832, 'LTC': 5, 'ETH': 1, 'REQ': 4790.21, 'NEO': 11.42, 'USD': 596.65, 'EUR': 506.79, 'SGD': 848.66, 'GBP': 444}, 'REQ': {'BTC': 1.635e-05, 'LTC': 0.001043, 'ETH': 0.0002088, 'REQ': 1, 'NEO': 0.002383, 'USD': 0.1251, 'EUR': 0.1063, 'SGD': 0.1772, 'GBP': 0.09318}, 'NEO': {'BTC': 0.006861, 'LTC': 0.4378, 'ETH': 0.0876, 'REQ': 419.63, 'NEO': 1, 'USD': 52.55, 'EUR': 44.62, 'SGD': 74.34, 'GBP': 39.1}, 'USD': {'BTC': 0.0001307, 'LTC': 0.00835, 'ETH': 0.001676, 'REQ': 7.99, 'NEO': 0.01903, 'USD': 1, 'EUR': 0.8475, 'SGD': 1.42, 'GBP': 0.7446}, 'EUR': {'BTC': 0.0001537, 'LTC': 0.009794, 'ETH': 0.001972, 'REQ': 9.4, 'NEO': 0.02241, 'USD': 1.18, 'EUR': 1, 'SGD': 1.67, 'GBP': 0.8763}, 'SGD': {'BTC': 9.229e-05, 'LTC': 0.005889, 'ETH': 0.001178, 'REQ': 5.64, 'NEO': 0.01344, 'USD': 0.7062, 'EUR': 0.6002, 'SGD': 1, 'GBP': 0.5259}, 'GBP': {'BTC': 0.0001755, 'LTC': 0.0112, 'ETH': 0.00224, 'REQ': 10.73, 'NEO': 0.02556, 'USD': 1.34, 'EUR': 1.14, 'SGD': 1.9, 'GBP': 1}}


price_matrix = []
for c1 in ccys:
	c1x = []
	for c2 in ccys:
		c1x.append(price_matrix_json[c1][c2])
	price_matrix.append(c1x)
class Price_Matrix(Resource):
	def get(self):
		return price_matrix_json
	
	def post(self):
		conn = db_connect.connect()
		print(request.json)
		return {'status':'success'}

import time
def price(symbol, comparison_symbols=['USD'], exchange=''):
	url = 'https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}'\
		.format(symbol.upper(), ','.join(comparison_symbols).upper())
	if exchange:
		url += '&e={}'.format(exchange)
	page = requests.get(url)
	data = page.json()
	return data

def price_matrix_downloader():
	while True:
		time.sleep(0.1)
		for i in range(0,len(ccys)):
			c1 = ccys[i]
			for j in range(0,len(ccys)):
				c2 = ccys[j]
				price_fetched = price(c1,[c2])
				price_matrix[i][j] = price_fetched[c2]
				price_matrix_json[c1][c2] = price_fetched[c2]
				
	


import threading
def start_downloading_price_matrix(inp):
	download_thread = threading.Thread(target=price_matrix_downloader, args=inp)
	download_thread.start()



import numpy as np
import math


# bellman-ford with parent pointers to detect negative cycle
def bellmanFord(src,pm_nmp):
	log_pm = np.negative(np.log(pm_nmp))
	parent = []
	dist = []
	neg_idx = -1
	for i in range(0,len(ccys)):
		if i==src:
			dist.append(0)
		else:
			dist.append(math.inf)
		parent.append(-1)
	for k in range(0,len(ccys)):
		for i in range(0,len(ccys)):
			for j in range(0,len(ccys)):
				w = 0 if (i==j or i==len(ccys) or j==len(ccys)) else log_pm[i][j]
				if dist[i] + w < dist[j]:
					dist[j] = dist[i] + w
					parent[j] = i
	negCycleFound = False;
	for i in range(0,len(ccys)):            
		if negCycleFound:
			break;
		for j in range(0,len(ccys)):
			w = 0 if (i==j or i==len(ccys) or j==len(ccys)) else log_pm[i][j]
			if dist[i] + w < dist[j]:
				# neg cycle
				neg_idx = j
				negCycleFound = True;
				break;
	if negCycleFound:
		neg_cycle_u = set();
		neg_cycle = []
		st = neg_idx
		for i in range(0,len(ccys)):
			if st in neg_cycle_u:
				break;
			neg_cycle_u.add(st)
			neg_cycle.append(st)
			st = parent[st]
		return neg_cycle[::-1]
	else:
		return None

arbitrage_opportunities = {}
def arbitrageFinder():
	while True:
		time.sleep(0.5)
		for i in range(0,len(ccys)):
			pm_nmp = np.array(price_matrix)
			n_c = bellmanFord(i,pm_nmp)
			neg_cycl_tmp = ''
			if n_c is not None:
				n_c = [n_c[-1]]+n_c
				quantity = 1
				quantityFinal = quantity;
				neg_cycl_tmp = ccys[n_c[0]]
				for j in range(1,len(n_c)):
					neg_cycl_tmp = neg_cycl_tmp+'-'+ccys[n_c[j]]
					quantityFinal = quantityFinal*pm_nmp[n_c[j-1]][n_c[j]]
				usdamt = (quantityFinal-quantity)*pm_nmp[n_c[0]][5]
				myRes = {}
				myRes['Id'] = 1
				myRes['Cycle'] = neg_cycl_tmp
				myRes['Quantity'] = 1
				myRes['Profit_USD'] = usdamt
				arbitrage_opportunities[0] = myRes
				break;
def find_arbitrage(inp):
	download_thread = threading.Thread(target=arbitrageFinder, args=inp)
	download_thread.start()

class Arbitrage(Resource):
	def get(self):
		return arbitrage_opportunities
api.add_resource(Price_Matrix, '/price_matrix') # Route_1
api.add_resource(Arbitrage, '/arbitrage') # Route_1
start_downloading_price_matrix([])
find_arbitrage([])
#arbitrageFinder()

if __name__ == '__main__':
	app.run()
