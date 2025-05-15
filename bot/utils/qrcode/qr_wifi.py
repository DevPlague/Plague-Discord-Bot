import qrcode
import io
from urllib.parse import quote

from qrcode.constants import ERROR_CORRECT_H
from PIL import Image
from typing import Optional
from qr_str import get_logo




def generate_wifi_qr(ssid: str, security: str, password: str, logo_url: Optional[str] = None) -> io.BytesIO:
    """
    Generates a WiFi QR code image that can be scanned to connect automatically.

    Args:
        `ssid`: Network name (SSID).
        `security`: Security type (WEP, WPA, WPA2, WPA3, nopass).
        `password`: Network password.
        `logo_url`: URL to the logo to insert in the center of the QR.

    Returns:
        `io.BytesIO`: A BytesIO object containing the generated QR code.
    """

    # Validations
    if not ssid:
        raise ValueError("SSID cannot be empty")

    if security not in ['WEP', 'WPA', 'WPA2', 'WPA3', 'nopass']:
        raise ValueError("Invalid security type")

    if security != 'nopass' and not password:
        raise ValueError("Password cannot be empty for secured networks")

    if security == 'nopass':
        wifi_data = 'WIFI:S:{};T:{};;'.format(quote(ssid), security)
    else:
        wifi_data = 'WIFI:S:{};T:{};P:{};;'.format(quote(ssid), security, quote(password))


    qr = qrcode.QRCode(
        version=4,
        error_correction=ERROR_CORRECT_H, # 30% error correction
        box_size=10,
        border=2,
    )
    qr.add_data(wifi_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB") # type: ignore

    if logo_url:
        logo = get_logo(logo_url)
        wsize = img.size[0] // 4  # 25%
        wpercent = wsize / float(logo.size[0])
        hsize = int(float(logo.size[1]) * wpercent) #Maintain aspect ratio
        logo = logo.resize((wsize, hsize), Image.Resampling.LANCZOS)

        center = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
        img.paste(logo, center, mask=logo)

    # Return image as bytes
    output = io.BytesIO()
    img.save(output, format="JPEG")
    output.seek(0)
    return output