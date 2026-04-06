import math
import secrets
import string
from dataclasses import dataclass


AMBIGUOUS_CHARS = "lI1O0"
DEFAULT_SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?/"


@dataclass
class PasswordConfig:
    length: int = 16
    use_uppercase: bool = True
    use_lowercase: bool = True
    use_digits: bool = True
    use_symbols: bool = True
    exclude_ambiguous: bool = False


def remove_ambiguous_chars(characters: str) -> str:
    return "".join(c for c in characters if c not in AMBIGUOUS_CHARS)


def build_charsets(config: PasswordConfig) -> list[str]:
    charsets = []

    if config.use_uppercase:
        charset = string.ascii_uppercase
        if config.exclude_ambiguous:
            charset = remove_ambiguous_chars(charset)
        if charset:
            charsets.append(charset)

    if config.use_lowercase:
        charset = string.ascii_lowercase
        if config.exclude_ambiguous:
            charset = remove_ambiguous_chars(charset)
        if charset:
            charsets.append(charset)

    if config.use_digits:
        charset = string.digits
        if config.exclude_ambiguous:
            charset = remove_ambiguous_chars(charset)
        if charset:
            charsets.append(charset)

    if config.use_symbols:
        charsets.append(DEFAULT_SYMBOLS)

    return charsets


def validate_config(config: PasswordConfig) -> None:
    charsets = build_charsets(config)

    if config.length < 4:
        raise ValueError("La longitud mínima recomendada es 4.")

    if not charsets:
        raise ValueError("Debes seleccionar al menos un tipo de carácter.")

    if config.length < len(charsets):
        raise ValueError(
            "La longitud debe ser al menos igual al número de grupos seleccionados."
        )


def generate_password(config: PasswordConfig) -> str:
    validate_config(config)
    charsets = build_charsets(config)

    password_chars = [secrets.choice(charset) for charset in charsets]
    all_chars = "".join(charsets)

    for _ in range(config.length - len(password_chars)):
        password_chars.append(secrets.choice(all_chars))

    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def calculate_charset_size(config: PasswordConfig) -> int:
    charsets = build_charsets(config)
    unique_chars = set("".join(charsets))
    return len(unique_chars)


def estimate_entropy_bits(length: int, charset_size: int) -> float:
    if length <= 0 or charset_size <= 0:
        raise ValueError("La longitud y el tamaño del conjunto deben ser mayores que cero.")
    return length * math.log2(charset_size)


def estimate_password_entropy(config: PasswordConfig) -> float:
    charset_size = calculate_charset_size(config)
    return estimate_entropy_bits(config.length, charset_size)


def classify_entropy(entropy_bits: float) -> str:
    if entropy_bits < 40:
        return "Baja"
    if entropy_bits < 60:
        return "Media"
    if entropy_bits < 80:
        return "Alta"
    return "Muy alta"


def estimate_strength(password: str) -> str:
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)

    score = sum([has_upper, has_lower, has_digit, has_symbol])

    if length >= 16 and score >= 4:
        return "Muy fuerte"
    if length >= 12 and score >= 3:
        return "Fuerte"
    if length >= 10 and score >= 2:
        return "Media"
    return "Débil"
