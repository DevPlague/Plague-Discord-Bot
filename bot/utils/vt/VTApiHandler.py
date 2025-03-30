import asyncio
import logging
from utils.vt.domain_scan import url_report
from utils.vt.ip_scan import ip_report

class VTApiHandler:
    def __init__(self, logger: logging.Logger, API_KEY: str) -> None:
        self.logger = logger
        self.API_KEY = API_KEY

        if API_KEY is None:
            raise ValueError("API_KEY is not set. Cannot request to VirusTotal API.")


    async def ip_result(self, ip: str):
        """Send the request to IP endpoint and returns the result."""
        result = await ip_report(ip, self.API_KEY)
        self.logger.info(f" IP scan result for {ip}: {result}")
        return result

    def sync_ip_scan(self, ip: str):
        """Send the request synchronously and returns the result."""
        return asyncio.run(self.ip_result(ip))


    async def url_result(self, url: str):
        """Send the request asynchronously and returns the result."""
        result = await url_report(url, self.API_KEY)
        self.logger.info(f" URL scan result for {url}: {result}")
        return result

    def sync_url_scan(self, url: str):
        """Send the request synchronously and returns the result."""
        return asyncio.run(self.url_result(url))
