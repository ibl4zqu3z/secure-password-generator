import tempfile
import unittest
from pathlib import Path

from passphrase_utils import PassphraseConfig, estimate_passphrase_entropy, generate_passphrase


class TestPassphraseUtils(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.wordlist_path = Path(self.temp_dir.name) / "words.txt"
        self.wordlist_path.write_text("sol\nluna\nmar\nfaro\nnube\nroca\n", encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_generate_passphrase(self):
        config = PassphraseConfig(words_count=4, separator="-")
        value = generate_passphrase(config, str(self.wordlist_path))
        self.assertEqual(len(value.split("-")), 4)

    def test_entropy_is_positive(self):
        entropy = estimate_passphrase_entropy(word_count=4, wordlist_size=6)
        self.assertGreater(entropy, 0)


if __name__ == "__main__":
    unittest.main()
