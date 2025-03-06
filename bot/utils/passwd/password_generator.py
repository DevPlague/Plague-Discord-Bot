from secrets import choice, randbelow
from random import shuffle
from math import log
from os import getcwd, path
import string

def read_words() -> list[str]:
    """Returns a list containing all words used for the `memorable_password_generator()` function."""
    with open(path.join(getcwd(), "bot/data/words.txt"), "r") as file:
        lines = file.readlines()

    # Remove "\n"
    words = [line[:-1] for line in lines]
    return words

# Password Length Variables
MIN_PASS_LEN = 8
MAX_PASS_LEN = 64
MIN_PASS_WORDS = 4
MAX_PASS_WORDS = 10
WORDS = read_words()

def random_password_generator(length: int = 20, capital: bool = True, numbers: bool = True, symbols: bool = True) -> tuple[str, float]:
    """Generates a random password consisting of ASCII characters.

    Passwords are guaranteed to contain at least one of each specified character type.
    Whitespace characters are **excluded**: `" "`, `"\n"`, `"\r"`, `"\t"`.

    E.g: `$[OyjIJH=iph[njS&48z`

    Arguments:
        `length`: Length of the password. Must be between 8 and 64 characters.
        `capital`: If `True`, include uppercase letters.
        `numbers`: If `True`, include numbers.
        `symbols`: If `True`, include special characters (" ` " excluded).

    Returns:
        `tuple[str, float]`: A tuple containing the generated password and its entropy.
    """

    # Pre-Conditions
    if type(length) != int: length = MIN_PASS_LEN
    elif length > MAX_PASS_LEN: length = MAX_PASS_LEN
    elif length < MIN_PASS_LEN: length = MIN_PASS_LEN

    # Add characters to password character list
    password = choice(string.ascii_lowercase)
    characters = string.ascii_lowercase

    if capital: 
        characters += string.ascii_uppercase
        password += choice(string.ascii_uppercase)

    if numbers: 
        characters += string.digits
        password += choice(string.digits)

    if symbols:
        special_chars = string.printable[62:89] + string.printable[91:94]  # Backticks mess up discord messages
        characters += special_chars
        password += choice(special_chars)
    
    while len(password) < length:
        password += choice(characters)

    password = list(password)
    shuffle(password)
    password = "".join(password)

    return password, entropy(len(characters), password)


def memorable_password_generator(words: int = 5) -> tuple[str, float]:
    """Generates a random memorable password.

    Passwords are made of random words and a number, separated by `"-"` characters.
    
    - E.g. `Three7-Production4-Deer9-Satisfied5`

    Arguments:
        `words`: Number of words used to create the password.

    Returns:
        `tuple[str, float]`: A tuple containing the generated password and its entropy.
    """

    # Pre-Conditions
    if type(words) != int: words = MIN_PASS_WORDS
    elif words > MAX_PASS_WORDS: words = MAX_PASS_WORDS
    elif words < MIN_PASS_WORDS: words = MIN_PASS_WORDS

    password = "".join(f"{choice(WORDS)}{randbelow(10)}-" for _ in range(words))
    return password[:-1], entropy(len(WORDS), password)   # Remove last character (-)


def entropy(n_characters: int, password: str) -> float:
    """
    Calculates the entropy of a password.

    Parameters:
        `n_characters`: Number of possible characters used to create the password.
        `password`: Your password.

    Returns:
        `float`: The entropy of the password.
        
    Notes:
        The value of `n_characters` increases when you add different character types into your password:
        - Numbers (Range size: 10)
        - Lowercase Latin letters (Range size: 26)
        - Uppercase Latin letters (Range size: 26)
        - Special symbols (Range size: 32)
    """
    return len(password) * log(n_characters, 2)