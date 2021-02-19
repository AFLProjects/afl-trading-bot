# AFL Stock Trading Bot

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![Generic badge](https://img.shields.io/badge/License-MIT-g)](https://shields.io/) [![Generic badge](https://img.shields.io/badge/Python-3.8-blue)](https://shields.io/) [![Generic badge](https://img.shields.io/badge/Release-Not_yet-red)](https://shields.io/) 

The project is an advanced python stock trading bot using the [IB API](https://github.com/InteractiveBrokers/tws-api-public). It offers the possibility to trade internationally for free using the Interactive Brokers API.

It uses a combination of strategies and indicators to automatically find the best trades. It is based on the [RSI](https://fr.wikipedia.org/wiki/Relative_strength_index), [EMA](https://en.wikipedia.org/wiki/Moving_average), [ATR](https://en.wikipedia.org/wiki/Average_true_range) indicator and [fourier analysis](https://en.wikipedia.org/wiki/Discrete_Fourier_transform) to determine [fibonacci retracement levels](https://en.wikipedia.org/wiki/Fibonacci_retracement).
> Use the software at your own risk. The authors and all affiliates assume no responsibility for your trading results

## Setup
- Create an account at [Interactive Brokers](https://www.interactivebrokers.com/en/home.php)(Live or paper)
- Download and install the [TWS](https://www.interactivebrokers.com/en/index.php?f=16040)(Trader Workstation)
- Start and setup the TWS([Tutorial](https://interactivebrokers.github.io/tws-api/initial_setup.html))
- Download the repo 
```sh
$ git clone https://github.com/AFLProjects/afl-trading-bot.git
```
- In the file **/api/autorun.py**  insert your credentials and the trading method(paper or live)
- Create a shortcut towards **/bot.py** in your system startup folder


## Simulation Results

| Deposit     | Final Net Liquidation | Winrate | Average Gain | Gain    | Trades | Markets |
|-------------|-----------------------|---------|--------------|---------|--------|---------|
| 100 USD     | 1542.25 USD           | 53.23%  | 50.72%       | x 14.42 | 1415   | 3735    |
| 250 USD     | 2837.21 USD           | 51.34%  | 39.65%       | x 10.34 | 2244   | 3735    |
| 1000 USD    | 8721.70 USD           | 50.42%  | 30.94%       | x 8.72  | 3834   | 3735    |
| 10000 USD   | 76744.19 USD          | 50.39%  | 23.25%       | x 7.67  | 7258   | 3735    |
| 100000 USD  | 718768.17 USD         | 49.82%  | 20.04%       | x 7.18  | 9805   | 3735    |
| 1000000 USD | 7136205.29 USD        | 48.32%  | 18.63%       | x 7.13  | 11046  | 3735    |