import requests
import logging
import config

def generate_advice(change, market, alert_type="SPIKE"):
    """Generates simple trading advice based on momentum."""
    if alert_type == "WHALE":
        return "🐋 **WHALE SIGHTING**: Huge volume spike! Smart money might be taking a position."
    if alert_type == "FLIP":
        return "🔀 **THE FLIP**: Market has flipped to favorite (>50c). Momentum is shifting!"
    if alert_type == "RESOLVE":
        return "🏁 **RESOLVED?**: Price hit 99c. Market might be ending."
        
    if change > 0:
        return "🚀 **BULLISH MOMENTUM**: Price is surging! Consider **Buying YES** if you believe the news is real."
    else:
        return "🔻 **BEARISH DIP**: Price is crashing! Consider **Selling YES** to stop loss, or **Buying NO**."

def send_discord_alert(market, start_price, current_price, time_delta_str, alert_type="SPIKE", volume_change=0):
    """Sends a rich embed to Discord."""
    if not config.DISCORD_WEBHOOK_URL:
        logging.warning("No Discord Webhook URL set. Skipping alert.")
        return

    change = current_price - start_price
    direction = "📈 UP" if change > 0 else "📉 DOWN"
    question = market.get('question')
    slug = market.get('slug', market.get('id'))
    url = f"https://polymarket.com/event/{slug}"
    
    advice = generate_advice(change, market, alert_type)
    
    # Colors
    color = 5763719 # Green
    if change < 0: color = 15548997 # Red
    if alert_type == "FLIP": color = 16776960 # Yellow/Gold
    if alert_type == "RESOLVE": color = 3447003 # Blue
    if alert_type == "WHALE": color = 10181046 # Purple

    title = f"{direction} SPIKE: {question}"
    if alert_type == "FLIP": title = f"🔀 FLIP ALERT: {question}"
    if alert_type == "RESOLVE": title = f"🏁 RESOLVE ALERT: {question}"
    if alert_type == "WHALE": title = f"🐋 WHALE ALERT: {question}"

    # Description
    desc = f"Price moved **${change:+.2f}** in {time_delta_str}."
    if alert_type == "WHALE":
        desc += f"\n**Volume Delta**: +${volume_change:,.0f} 💰"

    desc += f"\n\n💡 **ADVICE**: {advice}"

    embed = {
        "title": title,
        "description": desc,
        "url": url,
        "color": color,
        "fields": [
            {"name": "Current Price", "value": f"${current_price:.3f}", "inline": True},
            {"name": "Previous Price", "value": f"${start_price:.3f}", "inline": True},
            {"name": "Liquidity", "value": f"${market.get('liquidity', 'N/A')}", "inline": True}
        ],
        "footer": {"text": f"Polymarket Spike Bot • {alert_type}"}
    }
    
    try:
        requests.post(config.DISCORD_WEBHOOK_URL, json={"embeds": [embed]})
        logging.info(f"Alert sent for {question}")
    except Exception as e:
        logging.error(f"Failed to send Discord alert: {e}")

def send_status_alert(status):
    """Sends a status update (Online/Offline) to Discord."""
    if not config.DISCORD_WEBHOOK_URL:
        return
        
    color = 5763719 if status == "ONLINE" else 15548997 # Green or Red
    embed = {
        "title": f"Bot Status: {status}",
        "description": f"The Polymarket Spike Bot is now **{status}**.",
        "color": color,
        "footer": {"text": "Polymarket Spike Bot"}
    }
    try:
        requests.post(config.DISCORD_WEBHOOK_URL, json={"embeds": [embed]})
    except:
        pass

def send_health_check(markets):
    """Sends a periodic summary of the bot's status."""
    if not config.DISCORD_WEBHOOK_URL:
        return

    try:
        total = len(markets)
        embed = {
            "title": "💚 Bot Health Check",
            "description": f"**Status**: OPERATIONAL\n**Markets Scanned**: {total}\n**Next Check**: in 10 mins.",
            "color": 3447003, # Blue
            "footer": {"text": "Polymarket Spike Bot"}
        }
        requests.post(config.DISCORD_WEBHOOK_URL, json={"embeds": [embed]})
        logging.info("Sent health check.")
    except Exception as e:
        logging.error(f"Failed to send health check: {e}")
