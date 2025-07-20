import aiohttp
from ipaddress import ip_address
from typing import Union

async def valid_ip(ip: str) -> bool:
    """Check if the IP address is valid and public."""
    try:
        ipv4 = ip_address(ip)
        return ipv4.is_global
    except ValueError:
        return False

async def ip_report(ip: str, api_key: str) -> Union[bool, dict, str]: 
    """Request a report of an IP address from VirusTotal API."""
    if not await valid_ip(ip):
        return False
    
    headers = {
        "x-apikey": str(api_key),
        "Accept": "application/json",
        "cache-control": "no-cache",
    }

    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
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
