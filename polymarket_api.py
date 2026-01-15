import requests
import time
import logging
import config

def fetch_markets():
    """Fetches active markets. Hybrid Strategy: 400 Hot + 200 New."""
    all_markets_map = {} # Use dict to deduplicate by ID
    
    # 1. Fetch HOT Markets (Default Sort, likely Volume/Liquidity)
    limit = 100
    hot_count = 400
    for offset in range(0, hot_count, limit):
        params = {
            "limit": limit,
            "offset": offset,
            "closed": "false"
        }
        try:
            response = requests.get(config.GAMMA_API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            batch = data if isinstance(data, list) else data.get('data', [])
            if not batch: break
            
            for m in batch:
                all_markets_map[m['id']] = m
                
            time.sleep(0.3)
        except Exception as e:
            logging.error(f"Error fetching HOT markets offset {offset}: {e}")
            break

    # 2. Fetch NEW Markets (Sort by ID Descending)
    new_count = 200
    for offset in range(0, new_count, limit):
        params = {
            "limit": limit,
            "offset": offset,
            "closed": "false",
            "order": "id",
            "ascending": "false"
        }
        try:
            response = requests.get(config.GAMMA_API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            batch = data if isinstance(data, list) else data.get('data', [])
            if not batch: break
            
            for m in batch:
                # Deduplicate
                if m['id'] not in all_markets_map:
                    all_markets_map[m['id']] = m
                    
            time.sleep(0.3)
        except Exception as e:
            logging.error(f"Error fetching NEW markets offset {offset}: {e}")
            break
            
    return list(all_markets_map.values())

def is_valid_market(market):
    """Filters markets based on liquidity and tags."""
    # 1. Check Liquidity
    try:
        liquidity = float(market.get('liquidity', 0) or 0)
    except:
        liquidity = 0
        
    if liquidity < config.MIN_LIQUIDITY:
        return False

    # 2. Check Tags
    raw_tags = market.get('tags', [])
    tags = []
    for t in raw_tags:
        if isinstance(t, dict):
            tags.append(t.get('label', '').lower())
        else:
            tags.append(str(t).lower())
    
    # If any excluded tag is found, skip
    if any(ex in tags for ex in config.EXCLUDED_TAGS):
        return False
        
    return True

def get_price(market):
    """Extracts the best available price."""
    try:
        price = market.get('lastTradePrice') or market.get('bestAsk')
        return float(price) if price else None
    except:
        return None

def get_volume(market):
    """Extracts volume safely."""
    try:
        return float(market.get('volume', 0) or 0)
    except:
        return 0
