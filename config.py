import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# API Configuration
GAMMA_API_URL = "https://gamma-api.polymarket.com/markets"

# App Configuration
POLL_INTERVAL = 60  # seconds
HISTORY_WINDOW = 600  # 10 minutes (in seconds)
HEALTH_CHECK_INTERVAL = 600 # 10 minutes

# Filtering & Detection
PRICE_CHANGE_THRESHOLD = 0.10  # $0.10 alerting threshold
MIN_LIQUIDITY = 5000  # Filter out low liquidity
EXCLUDED_TAGS = {
    "sports", "nfl", "nba", "soccer", "football", "golf", "formula 1", "tennis",
    "mlb", "nhl", "cricket", "rugby", "mma", "ufc", "boxing"
}
