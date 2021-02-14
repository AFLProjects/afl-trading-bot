# Opener User Agent
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'

# Data provider url
URL_FINVIZ = 'https://finviz.com/screener.ashx?v=210&s=ta_p_tlsupport&r='
URL_YAHOO = 'https://finance.yahoo.com/trending-tickers/'

# Data
TIME_FRAME_DAYS = 365
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"
DATA_PRECISION = 10e5

# Analysis
DEFAULT_EMA_1 = 200
DEFAULT_EMA_2 = 50
DEFAULT_RSI_1 = 14
DEFAULT_RSI_2 = 10
MIN_RSI_BUY = 30
MAX_RSI_SELL = 70
MIN_DATA_PTS = 200

# UI
PROGRESS_BAR_SIZE = 40
AUTOCOMPLETE_LENGTH = 14
MAIN_CURVE_COLOR = 'black'
EMA1_COLOR = 'red'
EMA2_COLOR = 'green'
RSI_COLOR = 'black'
RSI_MAX_COLOR = 'red'
RSI_MIN_COLOR = 'blue'
LINE_STYLE = '-'

# Exceptions Message
MSG_OPENER_FAILED = '[Error 1] Installing User-Agent failed !'
MSG_FETCHING_FAILED = '[Error 2] Finding markets ended due to an error !'

# IO
FILE_LOGS = "logs.txt"
FILE_CREATE = 'x'
