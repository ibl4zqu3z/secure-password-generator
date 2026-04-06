import argparse
import sys

from password_utils import (
    PasswordConfig,
    calculate_entropy_bits,
    estimate_strength,
    generate_password,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generador de contraseñas seguras en Python."
    )

    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=16,
        help="Longitud de la contraseña (por defecto: 16)",
    )
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=1,
        help="Número de contraseñas a generar (por defecto: 1)",
    )
    parser.add_argument(
        "--no-uppercase",
        action="store_true",
        help="Excluir letras mayúsculas",
    )
    parser.add_argument(
        "--no-lowercase",
        action="store_true",
        help="Excluir letras minúsculas",
    )
    parser.add_argument(
        "--no-digits",
        action="store_true",
        help="Excluir números",
    )
    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Excluir símbolos",
    )
    parser.add_argument(
        "--exclude-ambiguous",
        action="store_true",
        help="Excluir caracteres ambiguos como l, I, 1, O, 0",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        config = PasswordConfig(
            length=args.length,
            use_uppercase=not args.no_uppercase,
            use_lowercase=not args.no_lowercase,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols,
            exclude_ambiguous=args.exclude_ambiguous,
        )

        for index in range(args.count):
            password = generate_password(config)
            strength = estimate_strength(password)
            entropy = calculate_entropy_bits(password)

            print(f"Contraseña {index + 1}: {password}")
            print(f"Fortaleza: {strength}")
            print(f"Entropía estimada: {entropy} bits")
            print("-" * 40)

        return 0
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
