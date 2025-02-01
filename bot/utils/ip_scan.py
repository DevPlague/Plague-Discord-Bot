# This script is used to get IPv4 address report received by ipWD.py via VirusTotal API.
import aiohttp
import os
from ipaddress import ip_address

# ---- Funciones ----
async def valid_ip(ip: str) -> bool:
    """Check if the IP address is valid and public."""
    try:
        ipv4 = ip_address(ip)
        return ipv4.is_global #Check if the IP address is public
    except ValueError:
        return False

async def ip_request(ip: str, api_key: str): 
    """Request a report of an IP address from VirusTotal API."""
    if not await valid_ip(ip):
        return f"IP address {ip} given isn't valid nor public."
    
    headers = {
        "x-apikey": str(api_key),
        "Accept": "application/json",
        "cache-control": "no-cache",
    }

    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"

    try:
        async with aiohttp.ClientSession() as session:#HTTP session to make requests
            async with session.get(url, headers=headers) as response:
                response.raise_for_status() #Raise an exception if the response status is not 200
                data = await response.json()
                
                if "data" in data:
                    return data["data"]["attributes"]["last_analysis_stats"]
                
                return f"Data not found from {ip}. Test it again later or request a scan of it on the website."

    except aiohttp.ClientError as e:
        return f"Error in the request: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"
