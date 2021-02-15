# AFL Stock Trading Bot

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![Generic badge](https://img.shields.io/badge/License-MIT-g)](https://shields.io/) [![Generic badge](https://img.shields.io/badge/Python-3.8-blue)](https://shields.io/) [![Generic badge](https://img.shields.io/badge/Release-Not_yet-red)](https://shields.io/) 

The project is an advanced python stock trading bot using the [IB API](https://github.com/InteractiveBrokers/tws-api-public). It offers the possibility to trade internationally for free using the Interactive Brokers API.

It uses a combination of strategies and indicators to automatically find the best trades. It is based on the [RSI](https://fr.wikipedia.org/wiki/Relative_strength_index), [EMA](https://en.wikipedia.org/wiki/Moving_average), [ATR](https://en.wikipedia.org/wiki/Average_true_range) indicator and [fourier analysis](https://en.wikipedia.org/wiki/Discrete_Fourier_transform) to determine [fibonacci retracement levels](https://en.wikipedia.org/wiki/Fibonacci_retracement). It also offers possibilities to use [MACD](https://en.wikipedia.org/wiki/MACD), [MFI](https://en.wikipedia.org/wiki/Money_flow_index), [OBV](https://en.wikipedia.org/wiki/On-balance_volume) and [VWAP](https://en.wikipedia.org/wiki/Volume-weighted_average_price).
> Use the software at your own risk. The authors and all affiliates assume no responsibility for your trading results

## Setup
- Create an account at [Interactive Brokers](https://www.interactivebrokers.com/en/home.php)(Live or paper)
> Note that have always the possibility to use a paper account and trade with fake money
- Download and install the [TWS](https://www.interactivebrokers.com/en/index.php?f=16040)(Trader Workstation)
> Please note that you MUST download the OFFLINE version of TWS, not the self- updating version
- Start and setup the TWS([Tutorial](https://interactivebrokers.github.io/tws-api/initial_setup.html))
- Download the repo 
```sh
$ git clone https://github.com/AFLProjects/afl-trading-bot.git
```
- In the **/autorun** folder insert your credentials and the trading method(paper or live)
> This folder contains the IBController 3.4 release, in order to automatically start the TWS, see their documentation for more information
- Start **setup.py**
> setup.py will install the necessary python libraries
- To start the bot automatically put a shortcut towards **bot.py** in your system startup folder
> Everytime your computer will start, the bot will automatically start TWS, insert your credentials and start trading in the desired mode.

## Simulation Results

| Time Interval (years) | Winrate | Trades | Markets |
|-----------------------|---------|--------|---------|
| 1                     | 90.67%  | 215    | 133     |
| 2                     | 81.74%  | 471    | 133     |
| 3                     | 75.64%  | 624    | 133     |
| 4                     | 77.54%  | 757    | 133     |
| 5                     | 78.38%  | 902    | 133     |
| 10                    | 76.60%  | 1492   | 133     |