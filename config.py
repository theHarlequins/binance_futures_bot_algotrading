# Trading Bot Settings - Easy to understand version! 🎮

# How much money to use for trading (like how much to bet in a game)
LEVERAGE = 1  # How many times to multiply your money (like 2x means double your bet)
WALLET_USAGE_PERCENT = 50.0  # How much of your money to use (50% means use half your money)

# Game Settings
STRATEGIES_COUNT = 5  # How many different ways to trade (like having 5 different game strategies)
MAXIMUM_NUMBER_OF_API_CALL_TRIES = 5  # How many times to try if something fails
SLEEP_INTERVAL = 0.25  # How often to check prices (like checking the score every quarter second)

# File Names for Saving Game Progress
INDICATORS_DICT_FILENAME = "indicators_dict.pkl"  # Where to save trading information
ORDERS_DICT_FILENAME = "orders_dict.pkl"  # Where to save your orders

# Time Settings
ONE_MINUTE_IN_MILLISECONDS = 60 * 1000  # How long is one minute in computer time
MAXIMUM_KLINE_CANDLES_PER_REQUEST = 1000  # How many price points to get at once
HANDLING_POSITIONS_TIME_SECOND = 10  # When to check for new trades (like checking every 10 seconds)

# Game Status Codes
ERROR = -1  # Something went wrong
SUCCESSFUL = 0  # Everything worked fine

# Money Settings
FIRST_COIN_SYMBOL = "USDT"  # The money you use to trade
SECOND_COIN_SYMBOL = "BTC"  # The coin you want to trade
CONTRACT_SYMBOL = SECOND_COIN_SYMBOL + FIRST_COIN_SYMBOL  # The full name of what you're trading

# Timeframe Settings (like choosing how often to check the game)
TIMEFRAME = "h1"    # Choose from: "m1" (1 minute), "m3" (3 minutes), "m15" (15 minutes), "h1" (1 hour), "h2" (2 hours), "h4" (4 hours), "d1" (1 day)

# How much to win or lose before stopping
TAKE_PROFIT_PERCENTS = [2, 3, 1.5, 2, 1.5]  # How much profit to take for each strategy
STOP_LOSS_PERCENTS = [-1, -1, -1.5, -1.5, -1]  # How much loss to allow for each strategy

# Number Settings
PRICE_DECIMAL_DIGITS = 2  # How many numbers after the decimal point for prices
INDICATORS_DECIMAL_DIGITS = 2  # How many numbers after the decimal point for indicators
POSITION_QUANTITY_DECIMAL_DIGITS = 3  # How many numbers after the decimal point for amounts

# Trading Lines to Watch
PRICE_DIRECTION_INDICATOR_NAME_1 = "ema_20"  # First line to watch (fast line)
PRICE_DIRECTION_INDICATOR_NAME_2 = "ema_50"  # Second line to watch (slow line)

# Other Settings
NEW_CLIENT_ORDER_ID_PREFIX = "aRandomString"  # Just a name for your orders
LAST_ACCOUNT_BALANCES_LIST_MAX_LENGTH = 12  # How many past balances to remember
IMPORTANT_CANDLES_COUNT = 100  # How many past prices to look at
SEND_TELEGRAM_MESSAGE = False  # Whether to send messages to your phone
HEDGE_MODE = True  # Whether to allow both up and down trades at the same time

# API Settings
API_BASE_URL = "https://fapi.binance.com"  # Binance Futures API endpoint
