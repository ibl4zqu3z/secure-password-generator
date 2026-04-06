import argparse

from password_utils import (
    PasswordConfig,
    classify_entropy,
    estimate_password_entropy,
    estimate_strength,
    generate_password,
)
from passphrase_utils import (
    PassphraseConfig,
    estimate_passphrase_entropy,
    generate_passphrase,
    load_wordlist,
)


DEFAULT_WORDLIST = "wordlists/eff_large_wordlist.txt"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generador de contraseñas y passphrases seguras."
    )

    subparsers = parser.add_subparsers(dest="mode", required=True)

    password_parser = subparsers.add_parser("password", help="Generar contraseñas aleatorias")
    password_parser.add_argument("-l", "--length", type=int, default=16)
    password_parser.add_argument("--no-uppercase", action="store_true")
    password_parser.add_argument("--no-lowercase", action="store_true")
    password_parser.add_argument("--no-digits", action="store_true")
    password_parser.add_argument("--no-symbols", action="store_true")
    password_parser.add_argument("--exclude-ambiguous", action="store_true")
    password_parser.add_argument("-n", "--count", type=int, default=1)

    passphrase_parser = subparsers.add_parser("passphrase", help="Generar passphrases")
    passphrase_parser.add_argument("-w", "--words", type=int, default=6)
    passphrase_parser.add_argument("--separator", default="-")
    passphrase_parser.add_argument("--capitalize", action="store_true")
    passphrase_parser.add_argument("--add-number", action="store_true")
    passphrase_parser.add_argument("--add-symbol", action="store_true")
    passphrase_parser.add_argument("--wordlist", default=DEFAULT_WORDLIST)
    passphrase_parser.add_argument("-n", "--count", type=int, default=1)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.mode == "password":
        config = PasswordConfig(
            length=args.length,
            use_uppercase=not args.no_uppercase,
            use_lowercase=not args.no_lowercase,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols,
            exclude_ambiguous=args.exclude_ambiguous,
        )

        entropy = estimate_password_entropy(config)
        entropy_label = classify_entropy(entropy)

        for i in range(args.count):
            password = generate_password(config)
            strength = estimate_strength(password)

            print(f"[{i + 1}] {password}")
            print(f"    Fortaleza: {strength}")
            print(f"    Entropía estimada: {entropy:.2f} bits ({entropy_label})")

    elif args.mode == "passphrase":
        config = PassphraseConfig(
            words_count=args.words,
            separator=args.separator,
            capitalize=args.capitalize,
            add_number=args.add_number,
            add_symbol=args.add_symbol,
        )

        wordlist = load_wordlist(args.wordlist)
        entropy = estimate_passphrase_entropy(
            word_count=config.words_count,
            wordlist_size=len(wordlist),
            add_number=config.add_number,
            add_symbol=config.add_symbol,
        )

        for i in range(args.count):
            passphrase = generate_passphrase(config, args.wordlist)
            print(f"[{i + 1}] {passphrase}")
            print(f"    Entropía estimada: {entropy:.2f} bits")


if __name__ == "__main__":
    main()
