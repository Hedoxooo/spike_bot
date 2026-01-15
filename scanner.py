import time
import logging
from collections import deque
import config
import polymarket_api
import notifier

class MarketScanner:
    def __init__(self):
        # Dictionary to store price history: {market_id: deque([(timestamp, price, volume)])}
        self.price_history = {}
        # Track last alert to avoid spamming: {market_id: last_alert_timestamp}
        self.last_alerted = {} 
        self.alert_cooldown = 300 # 5 minutes cooldown per market
        self.last_health_check = time.time()

    def process_markets(self, markets):
        now = time.time()
        
        for market in markets:
            if not polymarket_api.is_valid_market(market):
                continue
                
            m_id = market.get('id')
            price = polymarket_api.get_price(market)
            volume = polymarket_api.get_volume(market)
            
            if price is None:
                continue

            # Initialize history
            if m_id not in self.price_history:
                self.price_history[m_id] = deque()
            
            history = self.price_history[m_id]
            # Store (Time, Price, Volume)
            history.append((now, price, volume))
            
            # Prune old history
            while history and history[0][0] < now - config.HISTORY_WINDOW:
                history.popleft()
                
            if not history:
                continue
                
            # Compare current state to OLDEST state in window
            old_data = history[0]
            start_time = old_data[0]
            start_price = old_data[1]
            start_volume = old_data[2] if len(old_data) > 2 else volume 
            
            price_change = price - start_price
            volume_change = volume - start_volume

            # FEATURE 2: THE FLIP
            is_flip = (start_price < 0.50 and price >= 0.50)
            is_resolve = (start_price < 0.99 and price >= 0.99)
            
            # FEATURE 3: WHALE WATCH (Volume > $50k)
            is_whale = (volume_change > 50000)

            # Condition 1: Spike
            threshold_met = abs(price_change) >= config.PRICE_CHANGE_THRESHOLD
            
            # Trigger if Spike OR Flip OR Resolve OR Whale
            if threshold_met or is_flip or is_resolve or is_whale:
                last_alert = self.last_alerted.get(m_id, 0)
                if now - last_alert > self.alert_cooldown:
                    time_ago = int(now - start_time)
                    time_str = f"{time_ago}s" if time_ago < 60 else f"{time_ago//60}m"
                    
                    logging.info(f"*** ALERT *** {market.get('question')} | Triggered Alert")
                    
                    alert_type = "SPIKE"
                    if is_flip: alert_type = "FLIP"
                    if is_resolve: alert_type = "RESOLVE"
                    if is_whale: alert_type = "WHALE"
                    
                    notifier.send_discord_alert(market, start_price, price, time_str, alert_type, volume_change)
                    
                    self.last_alerted[m_id] = now

    def run(self):
        logging.info("Starting Spike Bot...")
        notifier.send_status_alert("ONLINE")
        self.last_health_check = time.time()
        
        try:
            while True:
                start_cycle = time.time()
                markets = polymarket_api.fetch_markets()
                logging.info(f"Fetched {len(markets)} markets.")
                if markets:
                    self.process_markets(markets)
                
                # Check for Health Check
                if time.time() - self.last_health_check > config.HEALTH_CHECK_INTERVAL:
                    notifier.send_health_check(markets)
                    self.last_health_check = time.time()
                
                elapsed = time.time() - start_cycle
                sleep_time = max(0, config.POLL_INTERVAL - elapsed)
                time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            logging.info("Stopping bot...")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        finally:
            notifier.send_status_alert("OFFLINE")
            logging.info("Bot stopped.")
