from hashlib import md5, sha256, sha3_256
from bcrypt import hashpw, gensalt, checkpw     # Necesita ser instalado: pip install bcrypt
from argon2 import PasswordHasher, Type         # Necesita ser instalado: pip install argon2-cffi

# Bcrypt function variables. Source: https://bcrypt-generator.com/
DEAULT_SALT_ROUNDS = 12
MAX_SALT_ROUNDS = 20
MIN_SALT_ROUNDS = 1

# Maximum and minimum allowed values for Argon2 parameters. Source: https://argon2.online/
MAX_MEMORY_COST = 1000000
MAX_PARALLELISM = 10
MAX_ITERATIONS = 20
MAX_HASH_LENGTH = 100

MIN_MEMORY_COST = 80
MIN_PARALLELISM = 1
MIN_ITERATIONS = 1
MIN_HASH_LENGTH = 4

# PasswordHasher object use to verify Argon2 hashes. 
# Used to avoid creating an instance each time verify_hash() is called.
verifier = PasswordHasher()


# FUNCTIONS
def MD5(text: str):
    """Hashes `text` using the MD5 algorithm."""
    return md5(text.encode()).hexdigest()

def SHA_256(text: str):
    """Hashes `text` using the SHA-256 algorithm."""
    return sha256(text.encode()).hexdigest()

def SHA_3(text: str):
    """Hashes `text` using the SHA-3 algorithm."""
    return sha3_256(text.encode()).hexdigest()


# Mainly used for savely storing passwords. Reason why we use "password" and not "text".
def Bcrypt(password: str, rounds: int = DEAULT_SALT_ROUNDS):
    """
    Hashes a password using the bcrypt algorithm.

    Args:
        `password`: The password to be hashed.
        `rounds`: The number of salt rounds to use.

    Returns:
        `str|None`: The hashed password as a string if successful, or `None` if the provided rounds parameter is invalid.

    Note:
        A higher number of rounds increases security, but also computation time.
    """

    bcrypt_hash = None

    if MIN_SALT_ROUNDS <= rounds <= MAX_SALT_ROUNDS:
        bcrypt_hash = hashpw(password.encode(), gensalt(rounds)).decode()
    else:
        print(f"Invalid parameter: 'rounds' must be between {MIN_SALT_ROUNDS}-{MAX_SALT_ROUNDS}.")

    return bcrypt_hash


def Argon2(password: str, iterations: int = 3, memory_cost: int = 65536, parallelism: int = 4, hash_len: int = 32, type: str = "id") -> str | None:
    """
    Hashes a password using the Argon2 algorithm.

    Args:
        `password`: The password to be hashed.
        `iterations`: The number of iterations (time cost). 
        `memory_cost`: The memory usage in KB. 
        `parallelism`: The number of threads for parallel processing. 
        `hash_len`: The length of the output hash in bytes. 
        `type`: The Argon2 variant to use ('id', 'i', or 'd').

    Returns:
        `str|None`: The hashed password as a string if successful, or `None` if an invalid parameter is provided or an error occurs.

    Raises:
        ValueError: If any parameter is outside its valid range.
        Exception: If an unexpected error occurs during hashing.

    Note:
        - A higher number of iterations and memory cost increases security, but also computation time.
        - The "id" variant is recommended for general use, as it provides resistance against GPU and side-channel attacks.
    """
    
    # Pre-Conditions
    limits = {
        "iterations": (MIN_ITERATIONS, MAX_ITERATIONS, iterations),
        "memory_cost": (MIN_MEMORY_COST, MAX_MEMORY_COST, memory_cost),
        "parallelism": (MIN_PARALLELISM, MAX_PARALLELISM, parallelism),
        "hash_len": (MIN_HASH_LENGTH, MAX_HASH_LENGTH, hash_len),
    }

    for param, (min_val, max_val, value) in limits.items():
        if not min_val <= value <= max_val:
            print(f"Invalid parameter: '{param}'.")
            return None

    # Type conversion
    if type == "id": type = Type.ID
    elif type == "i": type = Type.I
    elif type == "d": type = Type.D
    else: 
        print("Invalid parameter: 'type'.")
        return None

    # Generate hash
    argon2_hash = None
    ph = PasswordHasher(iterations, memory_cost, parallelism, hash_len, type = type)
    
    try:
        argon2_hash = ph.hash(password)
    except:
        print("An unexpected error ocurred. Hashing failed.")

    return argon2_hash
    

def verify_hash(hash_func: str, original_text: str, hash: str) -> bool:
    """
    Verifies if the given hash matches the original text using the specified hash function.

    Args:
        `hash_func`: The name of the hash function to use ('md5', 'sha256', 'sha3', 'bcrypt', or 'argon2').
        `original_text`: The original text to compare with the given hash.
        `hash`: The hash to compare the original text against.

    Returns:
        `bool`: `True` if the hash matches the original text using the specified hash function, `False` otherwise.
    """

    valid = False

    match hash_func:
        case "md5": valid = md5(original_text.encode()).hexdigest() == hash

        case "sha256": valid = sha256(original_text.encode()).hexdigest() == hash

        case "sha3": valid = sha3_256(original_text.encode()).hexdigest() == hash

        case "bcrypt": checkpw(original_text, hash.encode())

        case "argon2": 
            try:
                valid = verifier.verify(hash, original_text)
            except:
                pass

        case _:
            print(f"Invalid hash function: '{hash_func}'.")
    
    return valid