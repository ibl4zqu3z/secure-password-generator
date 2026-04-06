import math
import secrets
import string
from dataclasses import dataclass


AMBIGUOUS_CHARS = "lI1O0"
DEFAULT_SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?/"


@dataclass(frozen=True)
class PasswordConfig:
    length: int = 16
    use_uppercase: bool = True
    use_lowercase: bool = True
    use_digits: bool = True
    use_symbols: bool = True
    exclude_ambiguous: bool = False
    symbols: str = DEFAULT_SYMBOLS


def remove_ambiguous_chars(characters: str) -> str:
    return "".join(c for c in characters if c not in AMBIGUOUS_CHARS)


def build_charsets(config: PasswordConfig) -> list[str]:
    charsets: list[str] = []

    if config.use_uppercase:
        charset = string.ascii_uppercase
        if config.exclude_ambiguous:
            charset = remove_ambiguous_chars(charset)
        charsets.append(charset)

    if config.use_lowercase:
        charset = string.ascii_lowercase
        if config.exclude_ambiguous:
            charset = remove_ambiguous_chars(charset)
        charsets.append(charset)

    if config.use_digits:
        charset = string.digits
        if config.exclude_ambiguous:
            charset = remove_ambiguous_chars(charset)
        charsets.append(charset)

    if config.use_symbols:
        if not config.symbols:
            raise ValueError("El conjunto de símbolos no puede estar vacío.")
        charsets.append(config.symbols)

    return [charset for charset in charsets if charset]


def validate_config(config: PasswordConfig) -> None:
    if config.length < 4:
        raise ValueError("La longitud mínima admitida es 4.")

    charsets = build_charsets(config)
    if not charsets:
        raise ValueError("Debes habilitar al menos un grupo de caracteres.")

    if config.length < len(charsets):
        raise ValueError(
            "La longitud debe ser al menos igual al número de grupos de caracteres seleccionados."
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


def calculate_entropy_bits(password: str) -> float:
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(not c.isalnum() for c in password):
        pool += len(DEFAULT_SYMBOLS)

    if pool == 0:
        return 0.0

    return round(len(password) * math.log2(pool), 2)


def estimate_strength(password: str) -> str:
    entropy = calculate_entropy_bits(password)

    if entropy >= 90:
        return "Muy fuerte"
    if entropy >= 70:
        return "Fuerte"
    if entropy >= 50:
        return "Media"
    return "Débil"
