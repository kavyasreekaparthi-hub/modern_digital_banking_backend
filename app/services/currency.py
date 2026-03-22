import requests
from datetime import datetime, timedelta

class CurrencyService:
    # Simple in-memory cache to prevent hitting the API limit too often
    _cache = {"rates": None, "last_updated": None}
    CACHE_DURATION = timedelta(hours=6)

    @staticmethod
    def get_latest_rates():
        """Fetches exchange rates with simple 6-hour caching."""
        now = datetime.utcnow()

        # Return cached data if valid
        if CurrencyService._cache["rates"] and (now - CurrencyService._cache["last_updated"] < CurrencyService.CACHE_DURATION):
            return CurrencyService._cache["rates"]

        # Replace with your actual key from ExchangeRate-API
        # Ideally, store this in your app/config.py
        API_KEY = "YOUR_FREE_KEY" 
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status() # Raise error for bad responses
            data = response.json()
            rates = data.get("conversion_rates", {})
            
            # Extract only the currencies we support
            result = {
                "INR": rates.get("INR"),
                "EUR": rates.get("EUR"),
                "GBP": rates.get("GBP")
            }
            
            # Update cache
            CurrencyService._cache["rates"] = result
            CurrencyService._cache["last_updated"] = now
            
            return result
            
        except Exception as e:
            print(f"DEBUG: Currency API Error: {e}")
            return {"error": "Currency service currently unavailable"}

    @staticmethod
    def convert(amount: float, target_currency: str):
        """Converts an amount from USD to the target currency."""
        rates = CurrencyService.get_latest_rates()
        
        if "error" in rates:
            return None
            
        rate = rates.get(target_currency)
        if not rate:
            return None
            
        return round(amount * rate, 2)