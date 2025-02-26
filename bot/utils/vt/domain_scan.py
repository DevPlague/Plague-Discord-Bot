# Finished
from urllib.parse import urlparse
import base64 as b64
import aiohttp

# ---- Functions ----
async def valid_url(url: str) -> bool:
    """Check if the URL is valid and exists."""
    try:
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            return False

        headers = {"cache-control": "no-cache"}

        async with aiohttp.ClientSession() as session:
            async with session.head(url, allow_redirects=True, headers=headers) as response:
                return 200 <= response.status < 400

    except aiohttp.ClientError as e:
        print(f"[Error] Client error checking URL: {e}")
        return False
    except Exception as e:
        print(f"[Error] Unexpected error checking URL: {e}")
        return False


async def url_report(url: str, api_key: str):
    """Request a report of a URL from VirusTotal API."""
    if not await valid_url(url):
        return f"Did you just unlock a new level of imagination? That URL doesn't exist."

    headers = {
        "x-apikey": str(api_key),
        "Accept": "application/json",
        "cache-control": "no-cache",
    }

    # RFC 4648 URL-safe Base64 encoding (removes padding `=` correctly)
    url_encoded = b64.urlsafe_b64encode(url.encode()).decode().rstrip("=")

    request_url = f"https://www.virustotal.com/api/v3/urls/{url_encoded}"

    try:
        async with aiohttp.ClientSession() as session:  # HTTP session for requests
            async with session.get(request_url, headers=headers) as response:
                response.raise_for_status()  # Raise exception if status is not 200
                data = await response.json()

                if "data" in data:
                    return data["data"]["attributes"]["last_analysis_stats"]

                return f"Data not found for {url}. Try again later or request a scan on the website."

    except aiohttp.ClientError as e:
        return f"Error in the request: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

