import asyncio
import logging
from bot.utils.domain_scan import url_report
from ip_scan import ip_request

class ApiHandler:
    def __init__(self, logger: logging.Logger, API_KEY: str) -> None:
        self.logger = logger # Register messages returned by application
        self.API_KEY = API_KEY

        if API_KEY is None:
            raise ValueError("API_KEY is not set.")

    async def ip_scan(self, ip: str):
        """Send the request asynchronously and returns the result."""
        result = await ip_request(ip, self.API_KEY)
        self.logger.info(f"IP scan result for {ip}: {result}")
        return result

    def sync_ip_scan(self, ip: str):
        """Send the request synchronously and returns the result."""
        return asyncio.run(self.ip_scan(ip))
    
    async def url_scan(self, url: str):
        """Send the request asynchronously and returns the result."""
        result = await url_report(url, self.API_KEY)
        self.logger.info(f"URL scan result for {url}: {result}")
        return result

    def sync_url_scan(self, url: str):
        """Send the request synchronously and returns the result."""
        return asyncio.run(self.url_scan(url))
    
# Usage example:
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO) # Set the logging level to INFO
    logger = logging.getLogger(__name__)

    API_KEY = "apikey"
    api_handler = ApiHandler(logger, API_KEY)
    
    ip = "8.8.8.8"
    
    # Asynchronous request
    asyncio.run(api_handler.ip_scan(ip))
