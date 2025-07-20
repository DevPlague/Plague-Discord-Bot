import aiohttp
from io import BytesIO
from typing import Union
from base64 import b64decode


async def valid_file(file: bytes, mb: int = 32) -> bool:
    """Checks that the file don't surpass API's size limit and is not empty."""
    max_size = mb * 1024**2
    try:
        file_size = len(file)
        if file_size > max_size or file_size <= 0:
            return False
        return True
    except Exception as e:
        return False



async def file_analysis(file_data: bytes, filename: str, api_key: str) -> Union[bool, str]:
    """Upload file to VirusTotal for analysis."""
    is_valid = await valid_file(file_data)
    if not is_valid:
        return False
    
    headers = {
        "x-apikey": str(api_key),
        "Accept": "application/json",
    }
    
    file_obj = BytesIO(file_data)
    file_obj.name = filename
    
    try:
        # Prepare form data
        data = aiohttp.FormData()
        data.add_field(
            'file',
            file_obj,
            filename=filename,
            content_type='application/octet-stream'
        )
        
        request = "https://www.virustotal.com/api/v3/files"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(request, headers=headers, data=data) as response:
                if response.raise_for_status():
                    return "There was an error uploading the file. Check if you exceeded API rate limit"

                result = await response.json()
                if "data" in result and "id" in result["data"]:
                    return result["data"]["id"]

                else:
                    error_text = await response.text()
                    return f"Upload failed with status {response.status}: {error_text}"

    except aiohttp.ClientError as e:
        return f"Network error while uploading file: {str(e)}"
    except Exception as e:
        return f"Unexpected error while uploading file: {str(e)}"
    finally:
        file_obj.close()



async def file_report(file_id: str, api_key: str):
    """Request a report of a file from VirusTotal API."""
    decoded = b64decode(file_id)
    
    if b":" in decoded: 
        decoded = decoded.split(b":")[0].decode()
    else:
        decoded = decoded.decode()

    headers = {
        "x-apikey": str(api_key),
        "Accept": "application/json",
    }
    request = f"https://www.virustotal.com/api/v3/files/{decoded}"

    try:
        async with aiohttp.ClientSession() as session:  
            async with session.get(request, headers=headers) as response:
                if response.raise_for_status():
                    return "There was an error while making the request. Check if you exceeded API rate limit"
                data = await response.json()

                if "data" in data:
                    return data["data"]["attributes"]["last_analysis_stats"], decoded

                else:
                    error_text = await response.text()
                    return f"Request failed with status {response.status}: {error_text}"

    except aiohttp.ClientError as e:
        return f"Error in the request: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"
