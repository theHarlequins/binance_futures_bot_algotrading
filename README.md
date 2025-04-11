# Advanced Binance Futures Trading Bot 🚀

A professional-grade, multi-strategy automated trading bot for Binance Futures with an intuitive GUI interface and real-time market monitoring capabilities.

## ✨ Key Features

- **Professional GUI Interface**

  - Real-time market data monitoring
  - Live BTC price tracking with trend indicators
  - Active position management
  - Comprehensive trading logs
  - Dark/Light theme support

- **Advanced Trading Capabilities**

  - Multiple trading strategies support
  - Real-time strategy performance monitoring
  - Customizable take-profit and stop-loss settings
  - Support for all Binance Futures trading pairs
  - Leverage and hedge mode configuration

- **Smart Trading Features**

  - Quick filters for major, alt, and meme coins
  - Search functionality for trading pairs
  - Batch selection tools
  - Persistent settings storage
  - Secure API key management

- **Trading Strategies**
  1. Price Movement (EMA Crossover)
  2. Enhanced Price Movement
  3. MACD Strategy
  4. Enhanced MACD
  5. RSI Strategy

## 🚀 Quick Start

1. **Installation**

   ```bash
   # Clone the repository
   git clone https://github.com/theHarlequins/binance_futures_bot_algotrading.git
   cd binance-futures-trading-bot

   # Install dependencies
   pip install -r requirements.txt

   # Initialize required files
   python init_indicators_dict.py
   python init_orders_dict.py
   ```

2. **Configuration**

   - Launch the application: `python gui.py`
   - Go to File → Settings
   - Enter your Binance API credentials
   - Configure your preferred trading settings

3. **Start Trading**
   - Select your desired trading pairs
   - Enable and configure strategies
   - Click "Start Bot" to begin trading

## 💻 System Requirements

- Python 3.7+
- PyQt5
- Active Binance Futures account
- Supported OS: Windows, macOS, Linux

## 🔧 Configuration Options

### Trading Pairs

- Support for 300+ trading pairs
- Quick filters for different coin categories
- Multi-select capability for batch trading

### Strategy Settings

- **Take Profit**: 0.1% to 100%
- **Stop Loss**: -0.1% to -100%
- **Leverage**: 1x to 125x
- **Timeframes**: 1m, 3m, 15m, 1h, 2h, 4h, 1d

### Risk Management

- Customizable position sizes
- Automated stop-loss
- Take-profit management
- Maximum position limits

## 🔐 Security Features

- Secure local storage of API keys
- Encrypted credentials handling
- Rate limit management
- Error handling and recovery
- Automatic session management

## 📊 Trading Strategies Detail

### 1. Price Movement Strategy

- Uses EMA crossover for trend following
- Customizable EMA periods
- Suitable for trending markets

### 2. Enhanced Price Movement

- Modified EMA crossover with wider targets
- Additional confirmation signals
- Better performance in volatile markets

### 3. MACD Strategy

- Classic MACD crossover implementation
- Customizable MACD parameters
- Momentum-based trading

### 4. Enhanced MACD

- MACD with optimized parameters
- Wider targets for better profitability
- Additional filter conditions

### 5. RSI Strategy

- RSI-based entry and exit points
- Customizable overbought/oversold levels
- Mean reversion trading

## ⚠️ Risk Warning

Trading cryptocurrencies involves substantial risk and is not suitable for all investors. The high degree of leverage can work against you as well as for you. Before deciding to trade cryptocurrencies, you should carefully consider your investment objectives, level of experience, and risk appetite.

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📧 Support

For support and queries:

- Create an issue in the repository
- Join our community discussions

---

**Disclaimer**: This software is for educational purposes only. Do not risk money which you are afraid to lose. USE THE SOFTWARE AT YOUR OWN RISK. THE AUTHORS AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS.
