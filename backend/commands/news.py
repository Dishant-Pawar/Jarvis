import requests
import xml.etree.ElementTree as ET
from utils.logger import get_logger
from utils.helpers import format_response

logger = get_logger()

def get_news(category: str = None) -> dict:
    try:
        # Select Google News feed based on category
        if category and "tech" in category.lower():
            url = "https://news.google.com/rss/search?q=technology&hl=en-US&gl=US&ceid=US:en"
            topic = "Technology"
        else:
            url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
            topic = "General"
            
        logger.info(f"Fetching Google News RSS feed: {url}")
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            headlines = []
            
            # Parse top 5 items
            for item in root.findall(".//item")[:5]:
                title = item.find("title").text
                # Clean up source from title (usually ends with " - Source Name")
                if " - " in title:
                    title = title.rsplit(" - ", 1)[0]
                headlines.append(title)
                
            headlines_str = " | ".join(headlines)
            logger.info(f"Top headlines: {headlines_str}")
            return format_response(
                True, 
                f"Here are the top {topic} headlines: {headlines_str}", 
                {"headlines": headlines}
            )
        else:
            return format_response(False, "Could not fetch headlines from Google News RSS feed.")
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return format_response(False, f"Failed to retrieve news headlines: {str(e)}")
