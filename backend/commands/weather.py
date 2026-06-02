import requests
import urllib.parse
from utils.logger import get_logger
from utils.helpers import format_response

logger = get_logger()

def get_weather(city: str = None) -> dict:
    try:
        # If no city is specified, wttr.in automatically detects by IP!
        if city:
            city_encoded = urllib.parse.quote(city.strip())
            url = f"https://wttr.in/{city_encoded}?format=3"
        else:
            url = "https://wttr.in/?format=3"
            
        logger.info(f"Querying wttr.in weather: {url}")
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            weather_text = response.text.strip()
            # Clean up double spacing
            weather_text = " ".join(weather_text.split())
            logger.info(f"Weather response: {weather_text}")
            return format_response(True, f"The weather is: {weather_text}", {"weather": weather_text})
        else:
            return format_response(False, "Could not fetch weather data from wttr.in service.")
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        return format_response(False, f"Failed to get weather details: {str(e)}")
