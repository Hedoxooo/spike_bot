import logging
import scanner

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("spike_bot.log"),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    bot = scanner.MarketScanner()
    bot.run()
