A simple python server to find arbitrage among cryptos and fiat.

Usess Bellman-Ford to detect negative cycles in -log(W_ij) graph and if there is a negative cycle, there is arbitrage. W_ij is the cost of currency i in terms of currency j.

Data is pulled continously from CryptoCompare API. 

Setup:

pip install -r requirements.txt. 
NOTE: requirements is auto-generated for my current freeze.

Run:

python arbitrage_server.py

Arbitrage opportunity published on http://localhost:5000/arbitrage and current price matrix is published on http://localhost:5000/price_matrix