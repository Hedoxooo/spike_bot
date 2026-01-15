# Polymarket Spike Alert Bot 🚀

A real-time notification bot that monitors ~600 Polymarket markets and alerts you of significant price spikes, volume surges, and market flips via Discord.

## Features

*   **⚡ Hybrid Watchlist**: Scans top 400 "Hot" markets + 200 "Newest" markets.
*   **📈 Spike Detection**: Alerts when price moves > $0.10 in 10 minutes.
*   **🐋 Whale Watch**: Detects volume surges > $50,000.
*   **🔀 The Flip**: Alerts when a market flips to a favorite (>50c) or resolves.
*   **🤖 Smart Advice**: Generates automated trading advice based on momentum.

## Setup

1.  **Clone the repo**:
    ```bash
    git clone https://github.com/yourusername/spike-bot.git
    cd spike-bot
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    *   Copy `.env.example` to `.env`.
    *   Open `.env` and paste your Discord Webhook URL.
    ```bash
    cp .env.example .env
    # Edit .env file
    ```

4.  **Run the Bot**:
    ```bash
    python main.py
    ```

## Configuration

You can tweak thresholds in `config.py`:
*   `PRICE_CHANGE_THRESHOLD`: Sensitivity (Default: 0.10)
*   `POLL_INTERVAL`: Scan frequency (Default: 60s)
*   `MIN_LIQUIDITY`: Minimum market liquidity (Default: $5000)

## License
MIT
