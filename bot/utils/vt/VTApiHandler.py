import asyncio
import logging
from utils.vt.domain_scan import url_report
from utils.vt.ip_scan import ip_report
from utils.vt.file_scan import file_report, file_analysis

class VTApiHandler:
    def __init__(self, logger: logging.Logger, API_KEY: str) -> None:
        self.logger = logger
        self.API_KEY = API_KEY

        if API_KEY is None:
            raise ValueError("API_KEY is not set. Cannot request to VirusTotal API.")


    async def ip_result(self, ip: str):
        result = await ip_report(ip, self.API_KEY)
        return result

    def sync_ip_scan(self, ip: str):
        return asyncio.run(self.ip_result(ip))


    async def url_result(self, url: str):
        result = await url_report(url, self.API_KEY)
        return result

    def sync_url_scan(self, url: str):
        return asyncio.run(self.url_result(url))


    async def file_upload_and_analyze(self, file_data: bytes, filename: str):
        result = await file_analysis(file_data, filename, self.API_KEY)
        if isinstance(result, str) and (result.startswith("There was an error") or result.startswith("Upload failed")):
            return result

        elif isinstance(result, bool) and not result:
            return False

        else:
            return await file_report(str(result), self.API_KEY)

    def sync_file_upload(self, file_data: bytes, filename: str):
        return asyncio.run(self.file_upload_and_analyze(file_data, filename))