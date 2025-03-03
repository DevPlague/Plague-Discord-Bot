from base64 import b64encode, b64decode
from urllib.parse import quote, unquote


# ENCODING FUNCTIONS (unused, too short)
def toBinary(text: str):
    return " ".join(format(c, '08b') for c in bytearray(text, "utf-8"))

def toOctal(text: str):
    return " ".join(format(c, '03o') for c in bytearray(text, "utf-8"))

def toDecimal(text: str):
    return " ".join(format(c, 'd') for c in bytearray(text, "utf-8"))

def toHex(text: str):
    return " ".join(format(c, 'X') for c in bytearray(text, "utf-8"))

def toBase64(text: str):
    return b64encode(bytearray(text, "utf-8")).decode()

def URLEncode(text: str):
    return quote(text)

def encode(format: str, text: str):
    match format:
        case "b" | "o" | "d" | "x" | "X" :
            if format == "b": format = "08b"
            elif format == "o": format = "03o"
            return " ".join(format(c, format) for c in bytearray(text, "utf-8"))
        
        case "b64":
            return b64encode(bytearray(text, "utf-8")).decode()
        
        case "url":
            return quote(text)
        
        case _:
            print("Invalid format.")

# DECODING FUNCTIONS
def fromBinary(text: str):
    text = text.replace(" ", "")

    if(len(text) % 8 == 0):
        binary_chars = [text[i:i+8] for i in range(0, len(text), 8)]
        decoded_string = "".join(chr(int(i, 2)) for i in binary_chars)
        decoded_string = decoded_string.encode("latin-1").decode("utf-8")
    else:
        print("Invalid Binary string.")
        decoded_string = ""
    
    return decoded_string

def fromOctal(text: str):
    text = text.replace(" ", "")

    if(len(text) % 3 == 0):
        octal_chars = [text[i:i+3] for i in range(0, len(text), 3)]
        decoded_string = "".join(chr(int(i, 8)) for i in octal_chars)
        decoded_string = decoded_string.encode("latin-1").decode("utf-8")
    else:
        print("Invalid Octal string.")
        decoded_string = ""
    
    return decoded_string

def fromDecimal(text: str):
    decoded_string = ""
    ascii_chars = text.strip().split(" ")

    try:
        decoded_string = "".join(chr(int(c)) for c in ascii_chars)
        decoded_string = decoded_string.encode("latin-1").decode("utf-8")
    except ValueError:
        print("Invalid Decimal String.")
    except OverflowError:
        print("Invalid Decimal String. Characters must be separated.\nE.g: 72 101 108 108 111")

    return decoded_string

def fromHex(text: str):
    decoded_string = ""
    text = text.replace(" ", "")

    if(len(text) % 2 == 0):
        try:
            decoded_string = bytes.fromhex(text).decode("utf-8")
        except UnicodeDecodeError:
            print("Invalid Hex string.")
    else:
        print("Invalid length for Hex string.")

    return decoded_string

def fromBase64(text: str):
    return b64decode(bytearray(text, "utf-8")).decode()

def URLDecode(text: str):
    return unquote(text)

def decode(format: str, text: str):
    match format:
        case "b": fromBinary(text)
        case "o": fromOctal(text)
        case "d": fromDecimal(text)
        case "x" | "X": fromHex(text)
        case "b64": fromBase64(text)
        case "url": URLDecode(text)
        case _:
            print("Invalid format.")



if __name__ == "__main__":
    print(toBinary("Hola a todós"))
    print(toOctal("Hola a todós"))
    print(toDecimal("Hola a todós"))
    print(toHex("Hola a todós"))
    print(toBase64("Hola a todós"))
    print(URLEncode("Hola a todós."))
    print("---------------------------------------")
    print(fromBinary("01001000 01101111 01101100 01100001 00100000 01100001 00100000 01110100 01101111 01100100 11000011 10110011 01110011"))
    print(fromOctal("110 157 154 141 040 141 040 164 157 144 303 263 163"))
    print(fromDecimal("72 111 108 97 32 97 32 116 111 100 195 179 115"))
    print(fromHex("48 6F 6C 61 20 61 20 74 6F 64 C3 B3 73"))
    print(fromBase64("SG9sYSBhIHRvZMOzcw=="))
    print(URLDecode("Hola%20a%20tod%C3%B3s."))