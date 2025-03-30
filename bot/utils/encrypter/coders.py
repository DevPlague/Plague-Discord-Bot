from base64 import b64encode, b64decode
from binascii import Error
from urllib.parse import quote, unquote
from codecs import encode as cd

# MASTER ENCODING FUNCTION
def encode(format: str, text: str) -> str | None:
    """Encodes the given text into a given format (`binary`, `octal`, `hex`, `base64`, `URL` or `ROT13`).

    Args:
        `format`: Encoding format. Available formats: `"b"`, `"o"`, `"x"`, `"X"`, `"b64"`, `"url"`, `"rot13"`.

        `text`: The text to be encoded.

    Returns:
        `str|None`: The encoded text as a string, or `None` if the given format is invalid.
    
    Note: Both `"x"` and `"X"` formats encode the given text into a Hexadecimal string. 
        `"x"` uses lowercase letters, `"X"` uses uppercase letters.
    """

    encoded_text = None

    match format:
        case "b" | "o" | "x" | "X":
            if format == "b":
                format_pattern = "08b"
            elif format == "o":
                format_pattern = "03o"
            else:
                format_pattern = format

            encoded_text = " ".join(f"{c:{format_pattern}}" for c in bytearray(text, "utf-8"))

        case "b64":
            encoded_text = b64encode(bytearray(text, "utf-8")).decode()
        
        case "url":
            encoded_text = quote(text)
        
        case "rot13":
            encoded_text = cd(text, "rot_13")
        
        case _:
            print(f"Invalid format: '{format}'.")

    return encoded_text


# DECODING FUNCTIONS
def fromBinary(text: str) -> str | None:
    """Decodes a binary-encoded string.

    Args:
        `text`: A string containing binary-encoded values, with optional spaces.

    Returns:
        `str|None`: The decoded string, or `None` if the string is not properly formatted.

    Notes:
        - The binary string should be in groups of 8 digits (bytes), with or without spaces.
        - The function assumes that the encoded characters represent valid UTF-8 characters.
    """
    text = text.replace(" ", "")
    decoded_string = None

    if(len(text) % 8 == 0):
        binary_chars = [text[i:i+8] for i in range(0, len(text), 8)]
        decoded_string = "".join(chr(int(i, 2)) for i in binary_chars)
        decoded_string = decoded_string.encode("latin-1").decode("utf-8")
    else:
        print(f"Invalid binary string: {text}.")
    
    return decoded_string

def fromOctal(text: str) -> str | None:
    """Decodes an octal-encoded string into its corresponding text.

    Args:
        `text`: A string containing octal-encoded values, with optional spaces.

    Returns:
        `str`: The decoded string, or `None` if the string is not properly formatted.

    Notes:
        - The octal string should be in groups of 3 digits, each representing a byte (with or without spaces).
        - The function assumes that the encoded characters represent valid UTF-8 characters.
    """
    text = text.replace(" ", "")

    if(len(text) % 3 == 0):
        octal_chars = [text[i:i+3] for i in range(0, len(text), 3)]
        decoded_string = "".join(chr(int(i, 8)) for i in octal_chars)
        decoded_string = decoded_string.encode("latin-1").decode("utf-8")
    else:
        print("Invalid octal string.")
        decoded_string = None
    
    return decoded_string

def fromDecimal(text: str) -> str | None:
    """Decodes an ASCII-encoded string into its corresponding text.

    Args:
        `text`: A string containing ASCII-encoded values, with mandatory whitespace separation.

    Returns:
        `str|None`: The decoded string, or `None` if the string is not properly formatted.
    
    Notes:
        - Each ASCII integer must be separated by whitespaces. E.g: 72 101 108 108 111
        - The function assumes that the encoded characters represent valid UTF-8 characters.
    """

    decoded_string = None
    ascii_chars = text.strip().split(" ")

    try:
        decoded_string = "".join(chr(int(c)) for c in ascii_chars)
        decoded_string = decoded_string.encode("latin-1").decode("utf-8")

    except ValueError:
        print(f"Invalid decimal string: {ascii_chars}.")

    except OverflowError:
        print("Invalid decimal string. Characters must be separated.\nE.g: 72 101 108 108 111")

    return decoded_string

def fromHex(text: str) -> str | None:
    """Decodes a hexadecimal-encoded string into its corresponding text.

    Args:
        `text` (str): A string containing hexadecimal-encoded values, with optional spaces.

    Returns:
        `str|None`: The decoded string, or `None` if the string is invalid or not properly formatted.

    Notes:
        - The hexadecimal string should have an even length, as each byte is represented by two hexadecimal characters.
    """
    decoded_string = None
    text = text.replace(" ", "")

    if(len(text) % 2 == 0):
        try:
            decoded_string = bytes.fromhex(text).decode("utf-8")
        except UnicodeDecodeError:
            print(f"Invalid hexadecimal string: {text}.")
    else:
        print(f"Invalid length for hexadecimal string: {len(text)} characters (should be even).")

    return decoded_string

def fromBase64(text: str) -> str | None:
    """Decodes a base64-encoded string into its corresponding text.

    Args:
        `text`: The base64-encoded string.

    Returns:
        `str|None`: The decoded string, or `None` if the string is invalid.

    Note:
        - The function assumes that the encoded characters represent valid UTF-8 characters.
    """

    decoded_string = None

    try:
        decoded_string = b64decode(bytearray(text, "utf-8"), validate=True).decode()
    except Error:
        print(f"Invalid base64 string: '{text}'")
    
    return decoded_string

def URLDecode(text: str) -> str:
    """Decodes a URL-encoded string into its corresponding text.

    Args:
        `text`: The URL-encoded string.

    Returns:
        `str`: The decoded string.

    Note:
        - By default, percent-encoded sequences are decoded with UTF-8, and invalid sequences are replaced by a placeholder character.
    """
    return unquote(text)

def ROT13Decode(text: str) -> str:
    """Decodes a ROT13-encoded string into its corresponding text.

    Args:
        `text`: The ROT13-encoded string.

    Returns:
        `str`: The decoded string.
    """
    return cd(text, "rot_13")

# MASTER DECODING FUNCTION
def decode(format: str, text: str) -> str | None:
    """Decodes the given text into a `UTF-8` string.

    Args:
        `format`: Encoded text format. Avilable formats: `"b"`, `"o"`, `"x"`, `"b64"`, `"url"`, `"rot13"`.
        `text`: The text to be decoded.
    
    Returns:
        `str|None`: The decoded text as a UTF-8 string, or `None` if the given format is invalid.
    """
    decoded_string = None

    match format:
        case "b": decoded_string = fromBinary(text)
        case "o": decoded_string = fromOctal(text)
        case "d": decoded_string = fromDecimal(text)
        case "x" | "X": decoded_string = fromHex(text)
        case "b64": decoded_string = fromBase64(text)
        case "url": decoded_string = URLDecode(text)
        case "rot13": decoded_string = ROT13Decode(text)
        case _: print(f"Invalid format: '{format}'.")
    
    return decoded_string