import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QPushButton, QTableWidget, 
                           QTableWidgetItem, QGroupBox, QGridLayout, QSpinBox,
                           QDoubleSpinBox, QComboBox, QCheckBox, QMessageBox,
                           QFormLayout, QLineEdit, QListWidget, QScrollArea,
                           QTabWidget, QFrame, QSizePolicy, QDialog, QDialogButtonBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor
import sys
import logging
from datetime import datetime
from config import *
from main import *
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import QSettings

# Define color scheme
COLORS = {
    'primary': '#1E88E5',       # Blue
    'secondary': '#FFC107',     # Amber
    'success': '#4CAF50',       # Green
    'danger': '#F44336',        # Red
    'warning': '#FF9800',       # Orange
    'info': '#2196F3',         # Light Blue
    'background': '#FFFFFF',    # White
    'surface': '#F5F5F5',      # Light Gray
    'text': '#212121',         # Dark Gray
    'text_secondary': '#757575' # Medium Gray
}

class StyleHelper:
    @staticmethod
    def setup_table_style(table):
        """Apply consistent styling to tables"""
        table.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                gridline-color: #E0E0E0;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                padding: 5px;
                border: none;
                border-right: 1px solid #E0E0E0;
                border-bottom: 1px solid #E0E0E0;
                font-weight: bold;
            }
        """)
        
    @staticmethod
    def setup_button_style(button, primary=True):
        """Apply consistent styling to buttons"""
        if primary:
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['primary']};
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #1976D2;
                }}
                QPushButton:disabled {{
                    background-color: #BDBDBD;
                }}
            """)
        else:
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: white;
                    color: {COLORS['primary']};
                    border: 2px solid {COLORS['primary']};
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #F5F5F5;
                }}
                QPushButton:disabled {{
                    border-color: #BDBDBD;
                    color: #BDBDBD;
                }}
            """)

    @staticmethod
    def setup_group_box_style(group_box):
        """Apply consistent styling to group boxes"""
        group_box.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                margin-top: 1em;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
                color: #424242;
                font-weight: bold;
            }
        """)

class StrategySettingsWidget(QWidget):
    def __init__(self, strategy_id, description):
        super().__init__()
        self.setup_ui(strategy_id, description)
        
    def setup_ui(self, strategy_id, description):
        layout = QFormLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Strategy enable/disable with better styling
        self.enabled = QCheckBox("Enable Strategy")
        self.enabled.setStyleSheet("""
            QCheckBox {
                spacing: 8px;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        self.enabled.setChecked(True)
        layout.addRow(self.enabled)
        
        # Strategy description with better styling
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(f"color: {COLORS['text_secondary']}; padding: 5px 0;")
        layout.addRow(desc_label)
        
        # Common spinbox style
        spinbox_style = """
            QSpinBox, QDoubleSpinBox {
                padding: 5px;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                min-width: 100px;
            }
        """
        
        # Take Profit and Stop Loss
        self.tp_spin = QDoubleSpinBox()
        self.tp_spin.setRange(0.1, 100.0)
        self.tp_spin.setValue(2.0)
        self.tp_spin.setSingleStep(0.1)
        self.tp_spin.setStyleSheet(spinbox_style)
        layout.addRow(self.create_label("Take Profit (%):"), self.tp_spin)
        
        self.sl_spin = QDoubleSpinBox()
        self.sl_spin.setRange(-100.0, -0.1)
        self.sl_spin.setValue(-1.0)
        self.sl_spin.setSingleStep(0.1)
        self.sl_spin.setStyleSheet(spinbox_style)
        layout.addRow(self.create_label("Stop Loss (%):"), self.sl_spin)
        
        # Strategy specific settings
        if strategy_id in [0, 1]:  # Price Movement Strategies
            self.add_ema_settings(layout, spinbox_style)
        elif strategy_id in [2, 3]:  # MACD Strategies
            self.add_macd_settings(layout, spinbox_style)
        elif strategy_id == 4:  # RSI Strategy
            self.add_rsi_settings(layout, spinbox_style)
        
        self.setLayout(layout)
        
    def create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-weight: bold; color: #424242;")
        return label
        
    def add_ema_settings(self, layout, style):
        self.ema_fast = QSpinBox()
        self.ema_fast.setRange(5, 50)
        self.ema_fast.setValue(20)
        self.ema_fast.setStyleSheet(style)
        layout.addRow(self.create_label("Fast EMA Period:"), self.ema_fast)
        
        self.ema_slow = QSpinBox()
        self.ema_slow.setRange(10, 200)
        self.ema_slow.setValue(50)
        self.ema_slow.setStyleSheet(style)
        layout.addRow(self.create_label("Slow EMA Period:"), self.ema_slow)
        
    def add_macd_settings(self, layout, style):
        self.macd_fast = QSpinBox()
        self.macd_fast.setRange(5, 50)
        self.macd_fast.setValue(12)
        self.macd_fast.setStyleSheet(style)
        layout.addRow(self.create_label("MACD Fast Period:"), self.macd_fast)
        
        self.macd_slow = QSpinBox()
        self.macd_slow.setRange(10, 100)
        self.macd_slow.setValue(26)
        self.macd_slow.setStyleSheet(style)
        layout.addRow(self.create_label("MACD Slow Period:"), self.macd_slow)
        
        self.macd_signal = QSpinBox()
        self.macd_signal.setRange(2, 50)
        self.macd_signal.setValue(9)
        self.macd_signal.setStyleSheet(style)
        layout.addRow(self.create_label("MACD Signal Period:"), self.macd_signal)
        
    def add_rsi_settings(self, layout, style):
        self.rsi_period = QSpinBox()
        self.rsi_period.setRange(2, 50)
        self.rsi_period.setValue(11)
        self.rsi_period.setStyleSheet(style)
        layout.addRow(self.create_label("RSI Period:"), self.rsi_period)
        
        self.rsi_oversold = QDoubleSpinBox()
        self.rsi_oversold.setRange(0, 50)
        self.rsi_oversold.setValue(6)
        self.rsi_oversold.setStyleSheet(style)
        layout.addRow(self.create_label("RSI Oversold Level:"), self.rsi_oversold)
        
        self.rsi_overbought = QDoubleSpinBox()
        self.rsi_overbought.setRange(50, 100)
        self.rsi_overbought.setValue(94)
        self.rsi_overbought.setStyleSheet(style)
        layout.addRow(self.create_label("RSI Overbought Level:"), self.rsi_overbought)

class TradingBotGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_settings()  # Load saved settings
        self.setWindowTitle("Advanced Binance Futures Trading Bot")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set window background color
        self.setStyleSheet("background-color: #F5F5F5;")
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget with margins
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create top section
        top_section = QHBoxLayout()
        top_section.setSpacing(15)
        
        # Status section with better styling
        status_group = QGroupBox("Bot Status")
        status_group.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                margin-top: 1em;
                font-weight: bold;
            }
            QGroupBox::title {
                color: #424242;
            }
        """)
        status_layout = QHBoxLayout()
        status_layout.setSpacing(10)
        
        self.bot_status_label = QLabel("Status: Stopped")
        self.bot_status_label.setFont(QFont('Arial', 10, QFont.Bold))
        self.bot_status_label.setStyleSheet("color: #F44336;")  # Red color for stopped status
        status_layout.addWidget(self.bot_status_label)
        
        self.start_button = QPushButton("Start Bot")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #1E88E5;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """)
        self.start_button.clicked.connect(self.start_bot)
        status_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop Bot")
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1E88E5;
                border: 2px solid #1E88E5;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F5F5F5;
            }
            QPushButton:disabled {
                border-color: #BDBDBD;
                color: #BDBDBD;
            }
        """)
        self.stop_button.clicked.connect(self.stop_bot)
        self.stop_button.setEnabled(False)
        status_layout.addWidget(self.stop_button)
        
        status_group.setLayout(status_layout)
        top_section.addWidget(status_group)
        
        # Account info section with better styling
        account_group = QGroupBox("Account Information")
        account_group.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                margin-top: 1em;
                font-weight: bold;
            }
            QGroupBox::title {
                color: #424242;
            }
        """)
        account_layout = QHBoxLayout()
        account_layout.setSpacing(20)
        
        # Create info labels with better styling
        balance_layout = QVBoxLayout()
        balance_title = QLabel("Available:")
        balance_title.setStyleSheet("color: #757575; font-size: 12px;")
        self.balance_label = QLabel("0 USDT")
        self.balance_label.setStyleSheet("color: #212121; font-size: 14px; font-weight: bold;")
        balance_layout.addWidget(balance_title)
        balance_layout.addWidget(self.balance_label)
        
        total_balance_layout = QVBoxLayout()
        total_balance_title = QLabel("Total:")
        total_balance_title.setStyleSheet("color: #757575; font-size: 12px;")
        self.total_balance_label = QLabel("0 USDT")
        self.total_balance_label.setStyleSheet("color: #212121; font-size: 14px; font-weight: bold;")
        total_balance_layout.addWidget(total_balance_title)
        total_balance_layout.addWidget(self.total_balance_label)
        
        profit_layout = QVBoxLayout()
        profit_title = QLabel("P/L:")
        profit_title.setStyleSheet("color: #757575; font-size: 12px;")
        self.unrealized_profit_label = QLabel("0 USDT")
        self.unrealized_profit_label.setStyleSheet("color: #212121; font-size: 14px; font-weight: bold;")
        profit_layout.addWidget(profit_title)
        profit_layout.addWidget(self.unrealized_profit_label)
        
        account_layout.addLayout(balance_layout)
        account_layout.addLayout(total_balance_layout)
        account_layout.addLayout(profit_layout)
        
        account_group.setLayout(account_layout)
        top_section.addWidget(account_group)
        
        main_layout.addLayout(top_section)
        
        # Create settings tabs
        self.create_settings_tabs(main_layout)
        
        # Create tables section
        self.create_tables_section(main_layout)
        
        # Setup update timer
        self.setup_timer()
        
    def create_menu_bar(self):
        """Create the main menu bar with settings"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: white;
                border-bottom: 1px solid #E0E0E0;
            }
            QMenuBar::item {
                padding: 8px 12px;
                background-color: transparent;
            }
            QMenuBar::item:selected {
                background-color: #E3F2FD;
                color: #1E88E5;
            }
            QMenu {
                background-color: white;
                border: 1px solid #E0E0E0;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 25px 8px 20px;
                border-radius: 4px;
                margin: 2px 5px;
            }
            QMenu::item:selected {
                background-color: #E3F2FD;
                color: #1E88E5;
            }
        """)

        # File Menu
        file_menu = menubar.addMenu('File')
        
        # Settings action
        settings_action = QAction('Settings', self)
        settings_action.setShortcut('Ctrl+,')
        settings_action.triggered.connect(self.show_settings_dialog)
        file_menu.addAction(settings_action)
        
        # Add separator
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def show_settings_dialog(self):
        """Show the settings dialog"""
        dialog = SettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.save_settings()
            self.load_settings()

    def load_settings(self):
        """Load settings from QSettings"""
        settings = QSettings('BinanceFuturesBot', 'TradingBot')
        
        # Load API keys
        try:
            from api_keys import API_KEY, API_SECRET
            self.api_key = API_KEY
            self.api_secret = API_SECRET
        except:
            self.api_key = ""
            self.api_secret = ""
        
        # Load other settings with defaults
        self.leverage = settings.value('leverage', 1, type=int)
        self.hedge_mode = settings.value('hedge_mode', True, type=bool)
        self.timeframe = settings.value('timeframe', "3 Minutes", type=str)
        
        # Load selected pairs
        selected_pairs = settings.value('selected_pairs', [], type=list)
        if hasattr(self, 'pairs_list'):
            for i in range(self.pairs_list.count()):
                item = self.pairs_list.item(i)
                item.setSelected(item.text() in selected_pairs)

    def save_settings(self):
        """Save settings using QSettings"""
        settings = QSettings('BinanceFuturesBot', 'TradingBot')
        
        # Save API keys to file
        if hasattr(self, 'api_key') and hasattr(self, 'api_secret'):
            with open('api_keys.py', 'w') as f:
                f.write(f'''# Binance Futures API Keys
# Replace these with your actual API keys from Binance Futures
API_KEY = "{self.api_key}"
API_SECRET = "{self.api_secret}"

# IMPORTANT: Never share these keys with anyone!
# Keep this file private and add it to .gitignore''')
        
        # Save other settings
        if hasattr(self, 'leverage_spin'):
            settings.setValue('leverage', self.leverage_spin.value())
        if hasattr(self, 'hedge_mode_check'):
            settings.setValue('hedge_mode', self.hedge_mode_check.isChecked())
        if hasattr(self, 'timeframe_combo'):
            settings.setValue('timeframe', self.timeframe_combo.currentText())
        
        # Save selected pairs
        if hasattr(self, 'pairs_list'):
            selected_pairs = [item.text() for item in self.pairs_list.selectedItems()]
            settings.setValue('selected_pairs', selected_pairs)

    def create_settings_tabs(self, main_layout):
        settings_tabs = QTabWidget()
        settings_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                background: white;
            }
            QTabBar::tab {
                background: #F5F5F5;
                border: 1px solid #E0E0E0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
            }
        """)
        
        # Trading Pairs Tab
        pairs_tab = QWidget()
        pairs_layout = QVBoxLayout()
        pairs_layout.setSpacing(10)
        pairs_layout.setContentsMargins(15, 15, 15, 15)
        
        # Add title and description
        title = QLabel("Select Trading Pairs")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #424242;")
        pairs_layout.addWidget(title)
        
        desc = QLabel("Choose one or more trading pairs to monitor and trade. Use the search box to filter pairs.")
        desc.setStyleSheet("color: #757575;")
        pairs_layout.addWidget(desc)
        
        # Add search box and buttons layout
        search_layout = QHBoxLayout()
        
        # Create search box container
        search_container = QWidget()
        search_container_layout = QHBoxLayout()
        search_container_layout.setContentsMargins(0, 0, 0, 0)
        search_container_layout.setSpacing(5)
        
        # Add search icon and box
        self.pairs_search = QLineEdit()
        self.pairs_search.setPlaceholderText("🔍 Search trading pairs...")
        self.pairs_search.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                background: white;
                font-size: 13px;
                min-width: 200px;
            }
            QLineEdit:focus {
                border: 1px solid #1E88E5;
                background: #F8F9FA;
            }
        """)
        self.pairs_search.textChanged.connect(self.filter_pairs)
        search_container_layout.addWidget(self.pairs_search)
        search_container.setLayout(search_container_layout)
        search_layout.addWidget(search_container)
        
        # Add spacer
        search_layout.addStretch()
        
        # Add filter buttons with improved styling
        button_style = """
            QPushButton {
                padding: 8px 16px;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                background: white;
                min-width: 80px;
                font-weight: 500;
                color: #424242;
            }
            QPushButton:hover {
                background: #F5F5F5;
                border-color: #1E88E5;
                color: #1E88E5;
            }
            QPushButton:pressed {
                background: #E3F2FD;
            }
            QPushButton:checked {
                background: #E3F2FD;
                border-color: #1E88E5;
                color: #1E88E5;
            }
        """
        
        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.setCheckable(True)
        self.select_all_btn.setStyleSheet(button_style)
        self.select_all_btn.clicked.connect(self.toggle_select_all)
        search_layout.addWidget(self.select_all_btn)
        
        major_pairs_btn = QPushButton("Major")
        alt_pairs_btn = QPushButton("Alts")
        meme_pairs_btn = QPushButton("Meme")
        clear_filter_btn = QPushButton("Show All")
        
        for btn in [major_pairs_btn, alt_pairs_btn, meme_pairs_btn, clear_filter_btn]:
            btn.setStyleSheet(button_style)
            search_layout.addWidget(btn)
        
        major_pairs_btn.clicked.connect(lambda: self.quick_filter("major"))
        alt_pairs_btn.clicked.connect(lambda: self.quick_filter("alt"))
        meme_pairs_btn.clicked.connect(lambda: self.quick_filter("meme"))
        clear_filter_btn.clicked.connect(lambda: self.quick_filter("all"))
        
        pairs_layout.addLayout(search_layout)
        
        # Add BTC Price Display
        btc_price_container = QWidget()
        btc_price_layout = QHBoxLayout()
        btc_price_layout.setContentsMargins(0, 10, 0, 10)
        
        self.btc_price_label = QLabel("BTC/USDT: $0.00")
        self.btc_price_label.setStyleSheet("""
            QLabel {
                color: #212121;
                font-size: 16px;
                font-weight: bold;
                padding: 8px 16px;
                background: white;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
            }
        """)
        btc_price_layout.addWidget(self.btc_price_label)
        btc_price_layout.addStretch()
        btc_price_container.setLayout(btc_price_layout)
        pairs_layout.addWidget(btc_price_container)
        
        # Setup list widget with enhanced styling
        self.pairs_list = QListWidget()
        self.pairs_list.setSelectionMode(QListWidget.MultiSelection)
        self.pairs_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                padding: 5px;
                background: white;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 10px 15px;
                border-bottom: 1px solid #F5F5F5;
                margin: 2px 5px;
            }
            QListWidget::item:selected {
                background: #E3F2FD;
                color: #1E88E5;
                border-radius: 4px;
                border: none;
            }
            QListWidget::item:hover {
                background: #F5F5F5;
                border-radius: 4px;
            }
            QScrollBar:vertical {
                border: none;
                background: #F5F5F5;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #BDBDBD;
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        # Add trading pairs
        trading_pairs = [
            "1000000MOGUSDT", "1000BONKUSDT", "1000CATUSDT", "1000CHEEMSUSDT", "1000FLOKIUSDT",
            "1000LUNCUSDT", "1000PEPEUSDT", "1000RATSUSDT", "1000SATSUSDT", "1000SHIBUSDT",
            "1000WHYUSDT", "1000XECUSDT", "1000XUSDT", "1INCHUSDT", "1MBABYDOGEUSDT", "AAVEUSDT",
            "ACEUSDT", "ACHUSDT", "ACTUSDT", "ACXUSDT", "ADAUSDT", "AERGOUSDT", "AEROUSDT",
            "AEVOUSDT", "AGIXUSDT", "AGLDUSDT", "AI16ZUSDT", "AIUSDT", "AIXBTUSDT", "AKTUSDT",
            "ALCHUSDT", "ALGOUSDT", "ALICEUSDT", "ALPACAUSDT", "ALPHAUSDT", "ALTUSDT", "AMBUSDT",
            "ANIMEUSDT", "ANKRUSDT", "APEUSDT", "API3USDT", "APTUSDT", "ARBUSDT", "ARCUSDT",
            "ARKMUSDT", "ARKUSDT", "ARPAUSDT", "ARUSDT", "ASTRUSDT", "ATAUSDT", "ATOMUSDT",
            "AUCTIONUSDT", "AVAAIUSDT", "AVAUSDT", "AVAXUSDT", "AXLUSDT", "AXSUSDT", "B3USDT",
            "BADGERUSDT", "BAKEUSDT", "BALUSDT", "BANANAS31USDT", "BANANAUSDT", "BANDUSDT",
            "BANUSDT", "BATUSDT", "BBUSDT", "BCHUSDT", "BEAMXUSDT", "BELUSDT", "BERAUSDT",
            "BICOUSDT", "BIDUSDT", "BIGTIMEUSDT", "BIOUSDT", "BLURUSDT", "BLZUSDT", "BMTUSDT",
            "BNBUSDT", "BNTUSDT", "BNXUSDT", "BOMEUSDT", "BONDUSDT", "BRETTUSDT",
            "BROCCOLI714USDT", "BROCCOLIF3BUSDT", "BRUSDT", "BSVUSDT", "BSWUSDT", "BTCDOMUSDT",
            "BTCUSDT", "C98USDT", "CAKEUSDT", "CATIUSDT", "CELOUSDT", "CELRUSDT", "CETUSUSDT",
            "CFXUSDT", "CGPTUSDT", "CHESSUSDT", "CHILLGUYUSDT", "CHRUSDT", "CHZUSDT", "CKBUSDT",
            "COMBOUSDT", "COMPUSDT", "COOKIEUSDT", "COSUSDT", "COTIUSDT", "COWUSDT", "CRVUSDT",
            "CTKUSDT", "CTSIUSDT", "CVCUSDT", "CVXUSDT", "CYBERUSDT", "DARUSDT", "DASHUSDT",
            "DEFIUSDT", "DEGENUSDT", "DEGOUSDT", "DENTUSDT", "DEXEUSDT", "DFUSDT", "DGBUSDT",
            "DIAUSDT", "DODOXUSDT", "DOGEUSDT", "DOGSUSDT", "DOTUSDT", "DRIFTUSDT", "DUSDT",
            "DUSKUSDT", "DYDXUSDT", "DYMUSDT", "EDUUSDT", "EGLDUSDT", "EIGENUSDT", "ENAUSDT",
            "ENJUSDT", "ENSUSDT", "EOSUSDT", "EPICUSDT", "ETCUSDT", "ETHFIUSDT", "ETHUSDT",
            "ETHWUSDT", "FARTCOINUSDT", "FETUSDT", "FIDAUSDT", "FILUSDT", "FIOUSDT", "FLMUSDT",
            "FLOWUSDT", "FLUXUSDT", "FORMUSDT", "FTMUSDT", "FTTUSDT", "FXSUSDT", "GALAUSDT",
            "GASUSDT", "GHSTUSDT", "GLMRUSDT", "GLMUSDT", "GMTUSDT", "GMXUSDT", "GOATUSDT",
            "GPSUSDT", "GRASSUSDT", "GRIFFAINUSDT", "GRTUSDT", "GTCUSDT", "GUSDT", "HBARUSDT",
            "HEIUSDT", "HFTUSDT", "HIFIUSDT", "HIGHUSDT", "HIPPOUSDT", "HIVEUSDT", "HMSTRUSDT",
            "HOOKUSDT", "HOTUSDT", "ICPUSDT", "ICXUSDT", "IDEXUSDT", "IDUSDT", "ILVUSDT",
            "IMXUSDT", "INJUSDT", "IOSTUSDT", "IOTAUSDT", "IOTXUSDT", "IOUSDT", "IPUSDT",
            "JASMYUSDT", "JELLYJELLYUSDT", "JOEUSDT", "JTOUSDT", "JUPUSDT", "KAIAUSDT",
            "KAITOUSDT", "KASUSDT", "KAVAUSDT", "KDAUSDT", "KEYUSDT", "KLAYUSDT", "KMNOUSDT",
            "KNCUSDT", "KOMAUSDT", "KSMUSDT", "LAYERUSDT", "LDOUSDT", "LEVERUSDT", "LINAUSDT",
            "LINKUSDT", "LISTAUSDT", "LITUSDT", "LOKAUSDT", "LOOMUSDT", "LPTUSDT", "LQTYUSDT",
            "LRCUSDT", "LSKUSDT", "LTCUSDT", "LUMIAUSDT", "LUNA2USDT", "MAGICUSDT", "MANAUSDT",
            "MANTAUSDT", "MASKUSDT", "MAVIAUSDT", "MAVUSDT", "MBOXUSDT", "MDTUSDT",
            "MELANIAUSDT", "MEMEUSDT", "METISUSDT", "MEUSDT", "MEWUSDT", "MINAUSDT", "MKRUSDT",
            "MOCAUSDT", "MOODENGUSDT", "MORPHOUSDT", "MOVEUSDT", "MOVRUSDT", "MTLUSDT",
            "MUBARAKUSDT", "MYROUSDT", "NEARUSDT", "NEIROETHUSDT", "NEIROUSDT", "NEOUSDT",
            "NFPUSDT", "NILUSDT", "NKNUSDT", "NMRUSDT", "NOTUSDT", "NTRNUSDT", "NULSUSDT",
            "OCEANUSDT", "OGNUSDT", "OMGUSDT", "OMNIUSDT", "OMUSDT", "ONDOUSDT", "ONEUSDT",
            "ONGUSDT", "ONTUSDT", "OPUSDT", "ORBSUSDT", "ORCAUSDT", "ORDIUSDT", "OXTUSDT",
            "PARTIUSDT", "PENDLEUSDT", "PENGUUSDT", "PEOPLEUSDT", "PERPUSDT", "PHAUSDT",
            "PHBUSDT", "PIPPINUSDT", "PIXELUSDT", "PLUMEUSDT", "PNUTUSDT", "POLUSDT",
            "POLYXUSDT", "PONKEUSDT", "POPCATUSDT", "PORTALUSDT", "POWRUSDT", "PROMUSDT",
            "PYTHUSDT", "QNTUSDT", "QTUMUSDT", "QUICKUSDT", "RADUSDT", "RAREUSDT", "RAYSOLUSDT",
            "RAYUSDT", "RDNTUSDT", "REDUSDT", "REEFUSDT", "REIUSDT", "RENDERUSDT", "RENUSDT",
            "REZUSDT", "RIFUSDT", "RLCUSDT", "RONINUSDT", "ROSEUSDT", "RPLUSDT", "RSRUSDT",
            "RUNEUSDT", "RVNUSDT", "SAFEUSDT", "SAGAUSDT", "SANDUSDT", "SANTOSUSDT",
            "SCRTUSDT", "SCRUSDT", "SCUSDT", "SEIUSDT", "SFPUSDT", "SHELLUSDT", "SIRENUSDT",
            "SKLUSDT", "SLERFUSDT", "SLPUSDT", "SNTUSDT", "SNXUSDT", "SOLUSDT", "SOLVUSDT",
            "SONICUSDT", "SPELLUSDT", "SPXUSDT", "SSVUSDT", "STEEMUSDT", "STGUSDT", "STMXUSDT",
            "STORJUSDT", "STPTUSDT", "STRAXUSDT", "STRKUSDT", "STXUSDT", "SUIUSDT", "SUNUSDT",
            "SUPERUSDT", "SUSDT", "SUSHIUSDT", "SWARMSUSDT", "SWELLUSDT", "SXPUSDT", "SYNUSDT",
            "SYSUSDT", "TAOUSDT", "THETAUSDT", "THEUSDT", "TIAUSDT", "TLMUSDT", "TNSRUSDT",
            "TOKENUSDT", "TONUSDT", "TRBUSDT", "TROYUSDT", "TRUMPUSDT", "TRUUSDT", "TRXUSDT",
            "TSTUSDT", "TURBOUSDT", "TUSDT", "TUTUSDT", "TWTUSDT", "UMAUSDT", "UNFIUSDT",
            "UNIUSDT", "USTCUSDT", "USUALUSDT", "UXLINKUSDT", "VANAUSDT", "VANRYUSDT",
            "VELODROMEUSDT", "VETUSDT", "VICUSDT", "VIDTUSDT", "VINEUSDT", "VIRTUALUSDT",
            "VOXELUSDT", "VTHOUSDT", "VVVUSDT", "WAVESUSDT", "WAXPUSDT", "WIFUSDT", "WLDUSDT",
            "WOOUSDT", "WUSDT", "XAIUSDT", "XEMUSDT", "XLMUSDT", "XMRUSDT", "XRPUSDT",
            "XTZUSDT", "XVGUSDT", "XVSUSDT", "YFIUSDT", "YGGUSDT", "ZECUSDT", "ZENUSDT",
            "ZEREBROUSDT", "ZETAUSDT", "ZILUSDT", "ZKUSDT", "ZROUSDT", "ZRXUSDT"
        ]
        
        # Define major pairs for quick filtering
        self.major_pairs = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", "SOLUSDT", "DOTUSDT", "MATICUSDT", "LTCUSDT"]
        
        # Define meme pairs for quick filtering
        self.meme_pairs = [pair for pair in trading_pairs if any(meme in pair.upper() for meme in ["DOGE", "SHIB", "PEPE", "FLOKI", "MEME", "CAT", "CHEEMS", "BONK"])]
        
        for pair in sorted(trading_pairs):
            self.pairs_list.addItem(pair)
        
        pairs_layout.addWidget(self.pairs_list)
        pairs_tab.setLayout(pairs_layout)
        
        # Strategy Settings Tab
        strategy_tab = QWidget()
        strategy_layout = QVBoxLayout()
        strategy_layout.setSpacing(15)
        strategy_layout.setContentsMargins(15, 15, 15, 15)
        
        strategy_scroll = QScrollArea()
        strategy_scroll.setWidgetResizable(True)
        strategy_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #F5F5F5;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #BDBDBD;
                border-radius: 5px;
            }
        """)
        
        strategy_content = QWidget()
        strategy_content_layout = QVBoxLayout()
        strategy_content_layout.setSpacing(15)
        
        # Strategy descriptions
        strategy_descriptions = [
            "Strategy 0: Price Movement - Uses EMA crossover for trend following",
            "Strategy 1: Enhanced Price Movement - Uses EMA crossover with wider targets",
            "Strategy 2: MACD - Uses MACD crossover for momentum trading",
            "Strategy 3: Enhanced MACD - Uses MACD crossover with wider targets",
            "Strategy 4: RSI - Uses RSI indicator for oversold/overbought conditions"
        ]
        
        self.strategy_widgets = []
        for i, desc in enumerate(strategy_descriptions):
            frame = QFrame()
            frame.setFrameStyle(QFrame.StyledPanel)
            frame.setStyleSheet("""
                QFrame {
                    background: white;
                    border: 1px solid #E0E0E0;
                    border-radius: 4px;
                    padding: 10px;
                }
            """)
            
            frame_layout = QVBoxLayout()
            strategy_widget = StrategySettingsWidget(i, desc)
            self.strategy_widgets.append(strategy_widget)
            frame_layout.addWidget(strategy_widget)
            
            frame.setLayout(frame_layout)
            strategy_content_layout.addWidget(frame)
        
        strategy_content.setLayout(strategy_content_layout)
        strategy_scroll.setWidget(strategy_content)
        strategy_layout.addWidget(strategy_scroll)
        strategy_tab.setLayout(strategy_layout)
        
        # General Settings Tab
        general_tab = QWidget()
        general_layout = QFormLayout()
        general_layout.setSpacing(15)
        general_layout.setContentsMargins(15, 15, 15, 15)
        
        # Style for combo boxes and spin boxes
        widget_style = """
            QComboBox, QSpinBox {
                padding: 5px;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                min-width: 150px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """
        
        # Timeframe Selection
        self.timeframe_combo = QComboBox()
        self.timeframe_combo.addItems(["1 Minute", "3 Minutes", "15 Minutes", "1 Hour", "2 Hours", "4 Hours", "1 Day"])
        self.timeframe_combo.setCurrentText("3 Minutes")
        self.timeframe_combo.setStyleSheet(widget_style)
        
        timeframe_label = QLabel("Timeframe:")
        timeframe_label.setStyleSheet("font-weight: bold; color: #424242;")
        general_layout.addRow(timeframe_label, self.timeframe_combo)
        
        # Leverage Setting
        self.leverage_spin = QSpinBox()
        self.leverage_spin.setRange(1, 125)
        self.leverage_spin.setValue(1)
        self.leverage_spin.setStyleSheet(widget_style)
        
        leverage_label = QLabel("Leverage:")
        leverage_label.setStyleSheet("font-weight: bold; color: #424242;")
        general_layout.addRow(leverage_label, self.leverage_spin)
        
        # Hedge Mode Setting
        self.hedge_mode_check = QCheckBox()
        self.hedge_mode_check.setChecked(True)
        self.hedge_mode_check.setStyleSheet("""
            QCheckBox {
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        
        hedge_label = QLabel("Allow Both Long/Short:")
        hedge_label.setStyleSheet("font-weight: bold; color: #424242;")
        general_layout.addRow(hedge_label, self.hedge_mode_check)
        
        general_tab.setLayout(general_layout)
        
        # Add all tabs
        settings_tabs.addTab(pairs_tab, "Trading Pairs")
        settings_tabs.addTab(strategy_tab, "Strategy Settings")
        settings_tabs.addTab(general_tab, "General Settings")
        
        main_layout.addWidget(settings_tabs)
        
    def create_tables_section(self, main_layout):
        tables_layout = QHBoxLayout()
        tables_layout.setSpacing(15)
        
        # Positions table
        positions_group = QGroupBox("Active Positions")
        positions_group.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                margin-top: 1em;
                font-weight: bold;
            }
            QGroupBox::title {
                color: #424242;
            }
        """)
        positions_layout = QVBoxLayout()
        
        self.positions_table = QTableWidget()
        self.positions_table.setColumnCount(6)
        self.positions_table.setHorizontalHeaderLabels([
            "Strategy ID", "Symbol", "Side", "Amount", "Entry Price", "PNL"
        ])
        self.positions_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #E0E0E0;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                padding: 5px;
                border: none;
                border-right: 1px solid #E0E0E0;
                border-bottom: 1px solid #E0E0E0;
                font-weight: bold;
            }
        """)
        
        # Set table properties
        self.positions_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.positions_table.horizontalHeader().setStretchLastSection(True)
        self.positions_table.verticalHeader().setVisible(False)
        
        positions_layout.addWidget(self.positions_table)
        positions_group.setLayout(positions_layout)
        tables_layout.addWidget(positions_group)
        
        # Log table
        log_group = QGroupBox("Trading Log")
        log_group.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                margin-top: 1em;
                font-weight: bold;
            }
            QGroupBox::title {
                color: #424242;
            }
        """)
        log_layout = QVBoxLayout()
        
        self.log_table = QTableWidget()
        self.log_table.setColumnCount(4)
        self.log_table.setHorizontalHeaderLabels([
            "Time", "Level", "Symbol", "Message"
        ])
        self.log_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #E0E0E0;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                padding: 5px;
                border: none;
                border-right: 1px solid #E0E0E0;
                border-bottom: 1px solid #E0E0E0;
                font-weight: bold;
            }
        """)
        
        # Set table properties
        self.log_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.log_table.horizontalHeader().setStretchLastSection(True)
        self.log_table.verticalHeader().setVisible(False)
        
        log_layout.addWidget(self.log_table)
        log_group.setLayout(log_layout)
        tables_layout.addWidget(log_group)
        
        main_layout.addLayout(tables_layout)
        
    def setup_timer(self):
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_gui)
        self.update_timer.start(1000)
        
        # Initialize bot state
        self.is_bot_running = False
        self.trading_thread = None

    def create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-weight: bold; color: #424242;")
        return label

    def start_bot(self):
        try:
            # Get selected trading pairs
            selected_pairs = [item.text() for item in self.pairs_list.selectedItems()]
            if not selected_pairs:
                raise ValueError("Please select at least one trading pair")
            
            # Update config with GUI values
            global LEVERAGE, HEDGE_MODE, TIMEFRAME
            
            # Basic settings
            LEVERAGE = self.leverage_spin.value()
            HEDGE_MODE = self.hedge_mode_check.isChecked()
            TIMEFRAME = self.timeframe_combo.currentText()
            
            # Collect strategy settings
            strategy_settings = []
            for i, widget in enumerate(self.strategy_widgets):
                if widget.enabled.isChecked():
                    settings = {
                        "enabled": True,
                        "tp_percent": widget.tp_spin.value(),
                        "sl_percent": widget.sl_spin.value()
                    }
                    
                    # Add strategy-specific settings
                    if i in [0, 1]:  # Price Movement Strategies
                        settings.update({
                            "ema_fast": widget.ema_fast.value(),
                            "ema_slow": widget.ema_slow.value()
                        })
                    elif i in [2, 3]:  # MACD Strategies
                        settings.update({
                            "macd_fast": widget.macd_fast.value(),
                            "macd_slow": widget.macd_slow.value(),
                            "macd_signal": widget.macd_signal.value()
                        })
                    elif i == 4:  # RSI Strategy
                        settings.update({
                            "rsi_period": widget.rsi_period.value(),
                            "rsi_oversold": widget.rsi_oversold.value(),
                            "rsi_overbought": widget.rsi_overbought.value()
                        })
                    
                    strategy_settings.append(settings)
            
            if not strategy_settings:
                raise ValueError("Please enable at least one strategy")
            
            # Initialize indicators dictionary if needed
            try:
                load_indicators_dict()
            except:
                indicators_dict = {
                    "candle_open_timestamp": 0,
                    "candle_close_timestamp": 0,
                    "candle_close_price": 0,
                    "close_prices": []
                }
                save_indicators_dict()
            
            # Start the bot
            self.is_bot_running = True
            self.bot_status_label.setText("Status: Running")
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            
            # Start the main trading loop in a separate thread
            import threading
            self.trading_thread = threading.Thread(
                target=run_trading_bot,
                args=(selected_pairs, strategy_settings)
            )
            self.trading_thread.daemon = True
            self.trading_thread.start()
            
            # Log startup info
            pairs_str = ", ".join(selected_pairs)
            strategies_str = ", ".join([f"Strategy {i}" for i, s in enumerate(strategy_settings) if s["enabled"]])
            self.add_log("INFO", f"Bot started with pairs: {pairs_str}")
            self.add_log("INFO", f"Active strategies: {strategies_str}")
            self.add_log("INFO", f"Timeframe: {TIMEFRAME}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start bot: {str(e)}")
            self.stop_bot()
    
    def stop_bot(self):
        try:
            self.is_bot_running = False
            self.bot_status_label.setText("Status: Stopped")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            
            if self.trading_thread:
                self.trading_thread.join(timeout=5)
            
            self.add_log("INFO", "Bot stopped successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to stop bot: {str(e)}")
    
    def run_trading_bot(self):
        try:
            init_bot()
            update_account_balance_and_unrealized_profit(FIRST_COIN_SYMBOL)
            set_leverage(CONTRACT_SYMBOL, LEVERAGE)
            set_position_mode(HEDGE_MODE)
            
            while self.is_bot_running:
                sleep(SLEEP_INTERVAL)
                update_current_time()
                check_and_cancel_extra_open_orders()
                
                if not is_it_time_to_update_and_trade(current_time):
                    continue
                    
                load_orders_dict()
                load_indicators_dict()
                update_indicators_dict(CONTRACT_SYMBOL, current_time, self.timeframe_combo.currentText())
                update_current_time()
                update_recent_prices_list(CONTRACT_SYMBOL, current_time, IMPORTANT_CANDLES_COUNT, self.timeframe_combo.currentText())
                save_indicators_dict()
                update_contract_last_price(CONTRACT_SYMBOL)
                update_account_balance_and_unrealized_profit(FIRST_COIN_SYMBOL)
                
                # Only run active strategies
                active_strategies = [i for i, widget in enumerate(self.strategy_widgets) if widget.enabled.isChecked()]
                for i in active_strategies:
                    if not is_position_active(CONTRACT_SYMBOL, i):
                        if is_it_time_to_open_long_position(i, indicators_dict):
                            open_long_position(CONTRACT_SYMBOL, total_account_balance, TAKE_PROFIT_PERCENTS[i],
                                            STOP_LOSS_PERCENTS[i], i)
                        elif is_it_time_to_open_short_position(i, indicators_dict):
                            open_short_position(CONTRACT_SYMBOL, total_account_balance, TAKE_PROFIT_PERCENTS[i],
                                            STOP_LOSS_PERCENTS[i], i)
                
                save_orders_dict()
                
        except Exception as e:
            self.add_log("ERROR", f"Trading bot error: {str(e)}")
            self.stop_bot()
    
    def update_gui(self):
        try:
            # Update account information with color-coded values
            self.balance_label.setText(f"{account_available_balance:.2f} {FIRST_COIN_SYMBOL}")
            self.total_balance_label.setText(f"{total_account_balance:.2f} {FIRST_COIN_SYMBOL}")
            
            # Color code profit/loss with error handling
            try:
                profit_text = f"{unrealized_profit:.2f} {FIRST_COIN_SYMBOL}"
                if unrealized_profit > 0:
                    self.unrealized_profit_label.setStyleSheet("color: #4CAF50; font-size: 14px; font-weight: bold;")  # Green
                elif unrealized_profit < 0:
                    self.unrealized_profit_label.setStyleSheet("color: #F44336; font-size: 14px; font-weight: bold;")  # Red
                else:
                    self.unrealized_profit_label.setStyleSheet("color: #212121; font-size: 14px; font-weight: bold;")  # Default
            except NameError:
                profit_text = "0.00 USDT"
                self.unrealized_profit_label.setStyleSheet("color: #212121; font-size: 14px; font-weight: bold;")
            
            self.unrealized_profit_label.setText(profit_text)
            
            # Update bot status color
            if self.is_bot_running:
                self.bot_status_label.setStyleSheet("color: #4CAF50;")  # Green for running
                self.bot_status_label.setText("Status: Running")
            else:
                self.bot_status_label.setStyleSheet("color: #F44336;")  # Red for stopped
                self.bot_status_label.setText("Status: Stopped")
            
            # Update positions table
            self.update_positions_table()
            
            # Update log table
            self.update_log_table()
            
            # Update BTC price
            try:
                btc_price = float(binance_futures_api.ticker_price("BTCUSDT")["price"])
                self.btc_price_label.setText(f"BTC/USDT: ${btc_price:,.2f}")
                # Add color based on 24h change
                ticker_24h = binance_futures_api.ticker_24hr("BTCUSDT")
                price_change = float(ticker_24h["priceChangePercent"])
                if price_change > 0:
                    self.btc_price_label.setStyleSheet("""
                        QLabel {
                            color: #4CAF50;
                            font-size: 16px;
                            font-weight: bold;
                            padding: 8px 16px;
                            background: white;
                            border: 1px solid #E0E0E0;
                            border-radius: 4px;
                        }
                    """)
                elif price_change < 0:
                    self.btc_price_label.setStyleSheet("""
                        QLabel {
                            color: #F44336;
                            font-size: 16px;
                            font-weight: bold;
                            padding: 8px 16px;
                            background: white;
                            border: 1px solid #E0E0E0;
                            border-radius: 4px;
                        }
                    """)
            except Exception as e:
                self.btc_price_label.setText("BTC/USDT: Loading...")
            
        except Exception as e:
            self.add_log("ERROR", f"GUI update error: {str(e)}")
            return  # Add explicit return to ensure proper block closure
            
    def update_positions_table(self):
        try:
            # Get current positions from Binance
            positions = binance_futures_api.get_position_risk()
            
            # Update table
            self.positions_table.setRowCount(len(positions))
            for i, position in enumerate(positions):
                if float(position["positionAmt"]) != 0:
                    self.positions_table.setItem(i, 0, QTableWidgetItem(str(i)))
                    self.positions_table.setItem(i, 1, QTableWidgetItem(position["symbol"]))
                    self.positions_table.setItem(i, 2, QTableWidgetItem("LONG" if float(position["positionAmt"]) > 0 else "SHORT"))
                    self.positions_table.setItem(i, 3, QTableWidgetItem(str(abs(float(position["positionAmt"])))))
                    self.positions_table.setItem(i, 4, QTableWidgetItem(str(float(position["entryPrice"]))))
                    self.positions_table.setItem(i, 5, QTableWidgetItem(str(float(position["unRealizedProfit"]))))
            
            self.positions_table.resizeColumnsToContents()
            
        except Exception as e:
            self.add_log("ERROR", f"Failed to update positions table: {str(e)}")
    
    def update_log_table(self):
        try:
            # Read the last few lines from the log file
            with open("application.log", "r") as f:
                lines = f.readlines()[-10:]  # Get last 10 lines
            
            # Update table
            self.log_table.setRowCount(len(lines))
            for i, line in enumerate(lines):
                parts = line.split(" ")
                if len(parts) >= 4:
                    self.log_table.setItem(i, 0, QTableWidgetItem(parts[0] + " " + parts[1]))
                    self.log_table.setItem(i, 1, QTableWidgetItem(parts[2]))
                    self.log_table.setItem(i, 2, QTableWidgetItem(parts[3] if len(parts) > 3 else ""))
                    self.log_table.setItem(i, 3, QTableWidgetItem(" ".join(parts[4:])))
            
            self.log_table.resizeColumnsToContents()
            
        except Exception as e:
            self.add_log("ERROR", f"Failed to update log table: {str(e)}")
    
    def add_log(self, level, message):
        try:
            current_time = datetime.now().strftime("%Y/%m/%d %I:%M:%S %p")
            row = self.log_table.rowCount()
            self.log_table.insertRow(row)
            self.log_table.setItem(row, 0, QTableWidgetItem(current_time))
            self.log_table.setItem(row, 1, QTableWidgetItem(level))
            self.log_table.setItem(row, 2, QTableWidgetItem(CONTRACT_SYMBOL))
            self.log_table.setItem(row, 3, QTableWidgetItem(message))
            self.log_table.resizeColumnsToContents()
            
        except Exception as e:
            print(f"Failed to add log: {str(e)}")

    def filter_pairs(self):
        """Filter trading pairs based on search text"""
        search_text = self.pairs_search.text().upper()
        for i in range(self.pairs_list.count()):
            item = self.pairs_list.item(i)
            item.setHidden(search_text not in item.text().upper())
    
    def quick_filter(self, filter_type):
        """Quick filter for different types of pairs"""
        self.pairs_search.clear()
        for i in range(self.pairs_list.count()):
            item = self.pairs_list.item(i)
            if filter_type == "major":
                item.setHidden(item.text() not in self.major_pairs)
            elif filter_type == "meme":
                item.setHidden(item.text() not in self.meme_pairs)
            elif filter_type == "alt":
                item.setHidden(item.text() in self.major_pairs or item.text() in self.meme_pairs)
            else:  # Show all
                item.setHidden(False)

    def toggle_select_all(self):
        """Toggle selection of all trading pairs"""
        if self.select_all_btn.isChecked():
            for i in range(self.pairs_list.count()):
                item = self.pairs_list.item(i)
                if not item.isHidden():
                    item.setSelected(True)
            self.select_all_btn.setText("Deselect All")
        else:
            for i in range(self.pairs_list.count()):
                item = self.pairs_list.item(i)
                item.setSelected(False)
            self.select_all_btn.setText("Select All")

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Settings")
        self.setMinimumWidth(500)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Create tab widget
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                background: white;
                padding: 15px;
            }
            QTabBar::tab {
                background: #F5F5F5;
                border: 1px solid #E0E0E0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
            }
        """)
        
        # API Settings Tab
        api_tab = QWidget()
        api_layout = QFormLayout()
        api_layout.setSpacing(15)
        
        # API Key input
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter your API Key")
        self.api_key_input.setText(self.parent.api_key if hasattr(self.parent, 'api_key') else "")
        self.api_key_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                background: white;
                font-family: monospace;
            }
            QLineEdit:focus {
                border-color: #1E88E5;
                background: #F8F9FA;
            }
        """)
        
        # API Secret input
        self.api_secret_input = QLineEdit()
        self.api_secret_input.setPlaceholderText("Enter your API Secret")
        self.api_secret_input.setText(self.parent.api_secret if hasattr(self.parent, 'api_secret') else "")
        self.api_secret_input.setEchoMode(QLineEdit.Password)
        self.api_secret_input.setStyleSheet(self.api_key_input.styleSheet())
        
        # Show/Hide password button
        self.toggle_secret_btn = QPushButton("Show")
        self.toggle_secret_btn.setCheckable(True)
        self.toggle_secret_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                background: white;
                min-width: 80px;
            }
            QPushButton:hover {
                background: #F5F5F5;
                border-color: #1E88E5;
            }
            QPushButton:checked {
                background: #E3F2FD;
                border-color: #1E88E5;
            }
        """)
        self.toggle_secret_btn.toggled.connect(self.toggle_secret_visibility)
        
        # Add fields to form layout
        api_layout.addRow("API Key:", self.api_key_input)
        secret_layout = QHBoxLayout()
        secret_layout.addWidget(self.api_secret_input)
        secret_layout.addWidget(self.toggle_secret_btn)
        api_layout.addRow("API Secret:", secret_layout)
        
        # Add help text
        help_text = QLabel(
            "Your API keys are stored locally in api_keys.py and are never shared.\n"
            "Make sure to enable Futures trading permissions in your Binance account."
        )
        help_text.setStyleSheet("color: #757575; padding-top: 10px;")
        help_text.setWordWrap(True)
        api_layout.addRow("", help_text)
        
        api_tab.setLayout(api_layout)
        tab_widget.addTab(api_tab, "API Settings")
        
        # Add tab widget to main layout
        layout.addWidget(tab_widget)
        
        # Add buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                background: white;
                min-width: 80px;
            }
            QPushButton:hover {
                background: #F5F5F5;
                border-color: #1E88E5;
            }
            QPushButton[text="OK"] {
                background: #1E88E5;
                color: white;
                border-color: #1976D2;
            }
            QPushButton[text="OK"]:hover {
                background: #1976D2;
            }
        """)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def toggle_secret_visibility(self, checked):
        """Toggle API Secret visibility"""
        self.api_secret_input.setEchoMode(
            QLineEdit.Normal if checked else QLineEdit.Password
        )
        self.toggle_secret_btn.setText("Hide" if checked else "Show")

    def accept(self):
        """Save the settings when OK is clicked"""
        self.parent.api_key = self.api_key_input.text()
        self.parent.api_secret = self.api_secret_input.text()
        super().accept()

def main():
    app = QApplication(sys.argv)
    window = TradingBotGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 