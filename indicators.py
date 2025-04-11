# This file contains all the math tools our trading bot uses! 🧮

def get_wma(candles: list) -> float:
	if len(candles) == 0:
		return 0
	if len(candles) == 1:
		return candles[0]
	coe = 1
	base = 2 ** (1 / (len(candles) - 1))
	coe_sum = 0
	sum = 0
	for i in range(len(candles)):
		sum += candles[i] * coe
		coe *= base
		coe_sum += coe
	return sum / coe_sum


def get_ma(candles: list) -> float:
	if len(candles) == 0:
		return 0
	rs = 0
	for item in range(len(candles)):
		rs += float(candles[item])
	rs = rs / len(candles)
	return rs


def get_new_ema(old_ema: float, new_price: float, period: int) -> float:
	"""
	Calculate a new EMA (Exponential Moving Average) - like a smooth line following the price
	Think of it like drawing a line that follows the price but doesn't jump around too much
	"""
	multiplier = 2 / (period + 1)  # How much to trust the new price
	return new_price * multiplier + old_ema * (1 - multiplier)  # Mix old and new prices


def get_rsi(prices: list, period: int = 14) -> float:
	"""
	Calculate RSI (Relative Strength Index) - tells us if something is too expensive or too cheap
	Like a thermometer that shows if the price is too hot (overbought) or too cold (oversold)
	"""
	if len(prices) < period + 1:  # Need enough prices to calculate
		return 50.0  # Middle value if we don't have enough data
	
	# Calculate price changes
	changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]
	
	# Separate gains and losses
	gains = [change if change > 0 else 0 for change in changes]
	losses = [-change if change < 0 else 0 for change in changes]
	
	# Calculate average gains and losses
	avg_gain = sum(gains[-period:]) / period
	avg_loss = sum(losses[-period:]) / period
	
	if avg_loss == 0:  # If no losses, RSI is 100
		return 100.0
	
	# Calculate RSI
	rs = avg_gain / avg_loss  # Relative Strength
	rsi = 100 - (100 / (1 + rs))  # Final RSI calculation
	
	return round(rsi, 2)  # Round to 2 decimal places


def get_sma(prices: list, period: int) -> float:
	"""
	Calculate SMA (Simple Moving Average) - average of last few prices
	Like taking the average of your last few test scores
	"""
	if len(prices) < period:  # Need enough prices
		return prices[-1] if prices else 0  # Return last price if not enough data
	
	return sum(prices[-period:]) / period  # Average of last 'period' prices


def get_ema(prices: list, period: int) -> float:
	"""
	Calculate EMA from scratch using a list of prices
	Like drawing a smooth line through all the price points
	"""
	if len(prices) < period:  # Need enough prices
		return prices[-1] if prices else 0  # Return last price if not enough data
	
	sma = get_sma(prices, period)  # Start with simple average
	multiplier = 2 / (period + 1)  # How much to trust new prices
	
	# Calculate EMA step by step
	ema = sma
	for price in prices[period:]:
		ema = (price - ema) * multiplier + ema
	
	return ema


def get_macd(prices: list, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> tuple:
	"""
	Calculate MACD (Moving Average Convergence Divergence) - shows price momentum
	Like watching two cars race and seeing which one is pulling ahead
	"""
	# Calculate the fast and slow EMAs
	fast_ema = get_ema(prices, fast_period)
	slow_ema = get_ema(prices, slow_period)
	
	# Calculate MACD line (difference between fast and slow)
	macd_line = fast_ema - slow_ema
	
	# Calculate signal line (EMA of MACD line)
	signal_line = get_ema([macd_line], signal_period)
	
	return macd_line, signal_line  # Return both lines
