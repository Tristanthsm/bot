import asyncio
from typing import List

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Simple trading bot skeleton using moving average crossover strategy
# Fetches data periodically and notifies on signals

class TradingBot:
    def __init__(self, symbol: str, short_window: int = 20, long_window: int = 50):
        self.symbol = symbol
        self.short_window = short_window
        self.long_window = long_window
        self.prices = pd.DataFrame()

    async def fetch_price(self) -> None:
        ticker = yf.Ticker(self.symbol)
        data = ticker.history(period="1d", interval="1m")
        if not data.empty:
            self.prices = data

    def analyze(self) -> List[str]:
        signals = []
        if self.prices.empty:
            return signals
        df = self.prices.copy()
        df["short_ma"] = df["Close"].rolling(window=self.short_window).mean()
        df["long_ma"] = df["Close"].rolling(window=self.long_window).mean()
        if len(df) < self.long_window:
            return signals
        if df["short_ma"].iloc[-2] <= df["long_ma"].iloc[-2] and df["short_ma"].iloc[-1] > df["long_ma"].iloc[-1]:
            signals.append("BUY")
        if df["short_ma"].iloc[-2] >= df["long_ma"].iloc[-2] and df["short_ma"].iloc[-1] < df["long_ma"].iloc[-1]:
            signals.append("SELL")
        return signals

    def plot(self) -> None:
        if self.prices.empty:
            return
        df = self.prices
        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df["Close"], label="Close")
        plt.plot(df.index, df["Close"].rolling(window=self.short_window).mean(), label=f"MA{self.short_window}")
        plt.plot(df.index, df["Close"].rolling(window=self.long_window).mean(), label=f"MA{self.long_window}")
        plt.legend()
        plt.show()

    async def send_notification(self, message: str) -> None:
        # Placeholder for notification logic (email, SMS, etc.)
        print(f"Notification: {message}")

    async def run(self) -> None:
        while True:
            await self.fetch_price()
            signals = self.analyze()
            for signal in signals:
                await self.send_notification(f"{signal} signal for {self.symbol}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    bot = TradingBot("AAPL")
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("Stopping bot")
