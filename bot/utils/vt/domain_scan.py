import aiohttp
import base64 as b64
from urllib.parse import urlparse
from typing import Union

async def valid_url(url: str) -> bool:
    """Check if the URL is valid and exists."""
    try:
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            return False

        headers = {"cache-control": "no-cache"}

        async with aiohttp.ClientSession() as session:
            async with session.head(url, allow_redirects=True, headers=headers) as response:
                check1 = 200 <= response.status < 400
            async with session.get(url, allow_redirects=True, headers=headers) as response:
                check2 = 200 <= response.status < 400
        return check1 or check2

    except aiohttp.ClientError as e:
        return False

    except Exception as e:
        return False


async def url_report(url: str, api_key: str) -> Union[bool, dict, str]:
    """Request a report of a URL from VirusTotal API."""
    if not await valid_url(url):
        return False

    headers = {
        "x-apikey": str(api_key),
        "Accept": "application/json",
        "cache-control": "no-cache",
    }

    # RFC 4648 URL-safe Base64 encoding (removes padding `=` correctly)
    url_encoded = b64.urlsafe_b64encode(url.encode()).decode().rstrip("=")

    request_url = f"https://www.virustotal.com/api/v3/urls/{url_encoded}"

    try:
        async with aiohttp.ClientSession() as session:  
            async with session.get(request_url, headers=headers) as response:
                if response.raise_for_status():
                    return "There was an error while making the request. Check if you exceeded API rate limit"
                data = await response.json()

                if "data" in data:
                    return data["data"]["attributes"]["last_analysis_stats"]

                else:
                    error_text = await response.text()
                    return f"Request failed with status {response.status}: {error_text}"

    except aiohttp.ClientError as e:
        return f"Error in the request: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"