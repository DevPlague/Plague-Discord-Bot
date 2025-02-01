# This file will be used to scan for domains received by urlWD.py via VirusTotal API.

from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import urlparse

import os
import base64 as b64
import requests as http

# ---- Load environment variables ----
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(ENV_PATH)


# ---- Functions ----
def valid_url(url):
    """Check if the URL is valid and exists."""
    try:
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            return False
        
        headers = {"cache-control": "no-cache",}
        
        response = http.head(url, allow_redirects=True, timeout=5, headers=headers)
        return 200 <= response.status_code < 400

    except (http.RequestException, Exception) as e:
        print("Error in the request:", e)
        return False


def url_report(url):
    """Request a report of a URL from VirusTotal API."""
    if not valid_url(url):
        return f"URL {url} given isn't valid nor exists."
        
    headers = {
        "x-apikey": str(os.getenv("VT_API_KEY")),
        "Accept": "application/json",
        "cache-control": "no-cache",
    }
    
    # RFC 4648 URL-safe Base64 encoding. Code from https://docs.virustotal.com/reference/url
    url_formated = b64.urlsafe_b64encode(str(url).encode()).decode().strip("=")
    
    try:
        response = http.get(f"https://www.virustotal.com/api/v3/urls/{url_formated}", headers=headers)
        response.raise_for_status()
        
        data = response.json()
        if "data" in data:
            return data["data"]["attributes"]["last_analysis_stats"]
        
        return f"URL {url} data not found. Test it again later or request a scan of it on the website."
        
    except http.exceptions.RequestException as e:
        return f"Error in the request: {e}"
    
    except Exception as e:
        return f"Unexpected error: {e}"
    

if __name__ == "__main__":
    url = "https://www.google.com"
    result = url_report(url)
    print(result)
    