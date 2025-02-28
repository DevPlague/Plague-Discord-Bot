from secrets import choice, randbelow
from random import shuffle
from math import log
from os import getcwd, path
import string

# Password Length Variables
MIN_PASS_LEN = 8
MAX_PASS_LEN = 64
MIN_PASS_WORDS = 4
MAX_PASS_WORDS = 10

def read_words() -> list:
    """Returns a list containing all words used for the `memorable_password_generator()` function."""
    with open(path.join(getcwd(), "bot/data/words.txt"), "r") as file:
        lines = file.readlines()

    # Remove "\n"
    words = [line[:-1] for line in lines]
    return words

# Words used to generate memorable passwords.
WORDS = read_words()


def random_password_generator(length: int = 20, capital: bool = True, numbers: bool = True, symbols: bool = True):
    """
    Generates a random password, consisting of a string of random ASCII characters.
    Passwords are guaranteed to contain at least one of each character type, if specified.

    Passwords do not include whitespace characters: `" ", "\\n", "\\r", "\\t"`

    E.g. `$[OyjIJH=iph[njS&48z`

    Parameters:
        `length`: Length of the password. Passwords must be 8-64 characters long.
        `capital`: Use capital letters.
        `numbers`: Use numbers.
        `symbols`: Use special characters.
    
    Returns a tuple `(password, entropy)`.
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
        characters = string.printable.strip()
        password += choice(characters[62:])
    
    # Algorithm
    while len(password) < length:
        password += choice(characters)

    password = list(password)
    shuffle(password)
    password = "".join(password)

    return password, entropy(len(characters), password)


def memorable_password_generator(words: int = 5):
    """
    Generates a random memorable password. Passwords are made of random words and a number, separated by "-".
    E.g. `Three7-Production4-Deer9-Satisfied5`

    Parameters:
        `words`: Number of words used to create the password.
    
    Returns a tuple `(password, entropy)`.
    """

    # Pre-Conditions
    if type(words) != int: words = MIN_PASS_WORDS
    elif words > MAX_PASS_WORDS: words = MAX_PASS_WORDS
    elif words < MIN_PASS_WORDS: words = MIN_PASS_WORDS
    
    # Algorithm
    password = "".join(f"{choice(WORDS)}{randbelow(10)}-" for _ in range(words))
    return password[:-1], entropy(len(WORDS), password)   # Remove last character (-)


def entropy(n_characters: int, password: str) -> int:
    """
    Returns the entropy of a password.
    Parameters:
        `n_characters`: Number of possible characters used to create `password`.
        `password`: Your password.

    `n_character` increases when you add different characters into your password:
    - Numbers (Range size: 10)
    - Lowercase Latin letters (Range size: 26)
    - Uppercase Latin letters (Range size: 26)
    - Special symbols (Range size: 32)
    """

    return len(password) * log(n_characters, 2)


if __name__ == "__main__":
    # TESTING MAIN, REMOVE
    random = True

    if random:
        passw = random_password_generator(8, False, False, False)
    else:
        passw = memorable_password_generator(1)
    
    if passw[1] < 50: strength = "Vulnerable"
    elif passw[1] < 75: strength = "Medium"
    elif passw[1] < 90: strength = "Strong"
    else: strength = "Very Strong"

    print(f"Password: {passw[0]}\nEntropy: {passw[1]:.2f}\nStrength: {strength}")
