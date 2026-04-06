import math
import secrets
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PassphraseConfig:
    words_count: int = 6
    separator: str = "-"
    capitalize: bool = False
    add_number: bool = False
    add_symbol: bool = False


DEFAULT_SYMBOLS = "!@#$%^&*"


def load_wordlist(wordlist_path: str) -> list[str]:
    path = Path(wordlist_path)

    if not path.exists():
        raise FileNotFoundError(f"No se encontró la wordlist: {wordlist_path}")

    words = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    if not words:
        raise ValueError("La wordlist está vacía.")

    return words


def generate_passphrase(config: PassphraseConfig, wordlist_path: str) -> str:
    if config.words_count < 2:
        raise ValueError("La passphrase debe tener al menos 2 palabras.")

    words = load_wordlist(wordlist_path)
    chosen_words = [secrets.choice(words) for _ in range(config.words_count)]

    if config.capitalize:
        chosen_words = [w.capitalize() for w in chosen_words]

    passphrase = config.separator.join(chosen_words)

    if config.add_number:
        passphrase += str(secrets.randbelow(10))

    if config.add_symbol:
        passphrase += secrets.choice(DEFAULT_SYMBOLS)

    return passphrase


def estimate_passphrase_entropy(word_count: int, wordlist_size: int, add_number: bool = False, add_symbol: bool = False) -> float:
    if word_count <= 0 or wordlist_size <= 1:
        raise ValueError("Parámetros inválidos para calcular entropía.")

    entropy = word_count * math.log2(wordlist_size)

    if add_number:
        entropy += math.log2(10)

    if add_symbol:
        entropy += math.log2(len(DEFAULT_SYMBOLS))

    return entropy
