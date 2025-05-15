import qrcode
import requests
import io

from qrcode.constants import ERROR_CORRECT_H
from PIL import Image
from typing import Optional


def get_logo(logo_url: str) -> Image.Image:
    """
    Downloads and returns the logo from the given URL.

    Args:
        `logo_url`: URL pointing to the logo to download.

    Returns:
        `logo`: The downloaded logo image.
    """
    response = requests.get(logo_url)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    if not content_type.startswith("image/"):
        raise ValueError(f"URL does not point to an image: {content_type}")

    try:
        logo = Image.open(io.BytesIO(response.content)).convert("RGBA")
    except Exception as e:
        raise ValueError("Failed to open the image from the URL.") from e

    return logo


def generate_qr(data: str, logo_url: Optional[str] = None) -> io.BytesIO:
    """
    Generates a QR code image from the given data.

    Args:
        `data`: The data to encode in the QR code.
        `logo_url`: URL to the logo to insert in the center of the QR.

    Returns:
        `io.BytesIO: A BytesIO object containing the generated QR code.
    """
    qr = qrcode.QRCode(
        version=4,
        error_correction=ERROR_CORRECT_H, # 30% error correction
        box_size=10,
        border=2,
    )
    qr.add_data(data)
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

    output = io.BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output


if __name__ == "__main__":
    url = "https://discord.com"
    logo_url = "https://pngimg.com/uploads/discord/discord_PNG3.png"

    try:
        qr_image_bytes = generate_qr(url, logo_url)
        img = Image.open(qr_image_bytes)
        img.show()
    except Exception as e:
        print(f"Error generating QR code: {e}")
