import unittest

from password_utils import PasswordConfig, estimate_password_entropy, estimate_strength, generate_password


class TestPasswordUtils(unittest.TestCase):
    def test_password_length(self):
        config = PasswordConfig(length=20)
        password = generate_password(config)
        self.assertEqual(len(password), 20)

    def test_contains_selected_groups(self):
        config = PasswordConfig(
            length=16,
            use_uppercase=True,
            use_lowercase=True,
            use_digits=True,
            use_symbols=True,
        )
        password = generate_password(config)

        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(not c.isalnum() for c in password))

    def test_invalid_length(self):
        config = PasswordConfig(
            length=2,
            use_uppercase=True,
            use_lowercase=True,
            use_digits=True,
            use_symbols=False,
        )
        with self.assertRaises(ValueError):
            generate_password(config)

    def test_strength(self):
        self.assertEqual(estimate_strength("abc"), "Débil")
        self.assertEqual(estimate_strength("abc1234567"), "Media")
        self.assertEqual(estimate_strength("Abc123456789"), "Fuerte")
        self.assertEqual(estimate_strength("Abc123456789!@#$"), "Muy fuerte")

    def test_entropy_is_positive(self):
        config = PasswordConfig(length=16)
        entropy = estimate_password_entropy(config)
        self.assertGreater(entropy, 0)


if __name__ == "__main__":
    unittest.main()
