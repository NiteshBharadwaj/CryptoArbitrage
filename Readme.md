# A simple python server to find arbitrage among cryptos and fiat

Uses Bellman-Ford to detect negative cycles in -log(W_ij) graph and if there is a negative cycle, there is arbitrage. W_ij is the cost of currency i in terms of currency j.

Data is pulled continously from CryptoCompare API. 

#### Setup:

```pip install -r requirements.txt``` 
NOTE: requirements is auto-generated for my current freeze.

#### Run:

```python arbitrage_server.py```

Arbitrage opportunity published on http://localhost:5000/arbitrage and current price matrix is published on http://localhost:5000/price_matrix

#### Sample outputs:

```{"0": {"Id": 1, "Cycle": "LTC-SGD-GBP-LTC", "Quantity": 1, "Profit_USD": 0.14437446114481436}}```

From below data, using 1 unit of LTC, we can buy 1x150.74 SGD, and then using this SGD we can buy 1x150.74x0.5596 GBP and subsequently buy 1x150.74x0.5596x0.01187 = 1.00128321448 LTC ending up with arbitrage profit of 0.00128321448 LTC = 0.1443744 USD


```{"BTC": {"BTC": 1, "LTC": 64.1, "ETH": 12.8, "REQ": 63211.13, "NEO": 148.85, "USD": 7212.6, "EUR": 6124.04, "SGD": 9662.73, "GBP": 5405.84}, "LTC": {"BTC": 0.0156, "LTC": 1, "ETH": 0.1997, "REQ": 986.09, "NEO": 2.32, "USD": 112.51, "EUR": 95.9, "SGD": 150.74, "GBP": 84.33}, "ETH": {"BTC": 0.07809, "LTC": 5.01, "ETH": 1, "REQ": 4945.54, "NEO": 11.63, "USD": 561.84, "EUR": 478.6, "SGD": 753.02, "GBP": 421.9}, "REQ": {"BTC": 1.582e-05, "LTC": 0.001014, "ETH": 0.0002027, "REQ": 1, "NEO": 0.002354, "USD": 0.1141, "EUR": 0.09696, "SGD": 0.1527, "GBP": 0.08551}, "NEO": {"BTC": 0.006721, "LTC": 0.4308, "ETH": 0.08611, "REQ": 424.84, "NEO": 1, "USD": 48.38, "EUR": 41.19, "SGD": 65.43, "GBP": 36.32}, "USD": {"BTC": 0.0001386, "LTC": 0.008889, "ETH": 0.001781, "REQ": 8.76, "NEO": 0.02067, "USD": 1, "EUR": 0.8475, "SGD": 1.34, "GBP": 0.7493}, "EUR": {"BTC": 0.0001633, "LTC": 0.01043, "ETH": 0.002093, "REQ": 10.32, "NEO": 0.0243, "USD": 1.18, "EUR": 1, "SGD": 1.58, "GBP": 0.882}, "SGD": {"BTC": 0.0001036, "LTC": 0.006642, "ETH": 0.001328, "REQ": 6.55, "NEO": 0.01528, "USD": 0.747, "EUR": 0.6347, "SGD": 1, "GBP": 0.5596}, "GBP": {"BTC": 0.0001852, "LTC": 0.01187, "ETH": 0.002372, "REQ": 11.7, "NEO": 0.02754, "USD": 1.33, "EUR": 1.13, "SGD": 1.79, "GBP": 1}}```
