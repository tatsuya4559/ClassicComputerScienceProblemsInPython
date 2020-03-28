from secrets import token_bytes
from typing import Tuple


def random_key(length: int) -> int:
    tb = token_bytes(length)
    return int.from_bytes(tb, "big")


def encrypt(original: str) -> Tuple[int, int]:
    original_bytes = original.encode()
    dummy = random_key(len(original_bytes))
    original_key = int.from_bytes(original_bytes, "big")
    encrypted = dummy ^ original_key
    return dummy, encrypted


def decrypt(key1: int, key2: int) -> str:
    decrypted = key1 ^ key2
    return decrypted.to_bytes((decrypted.bit_length() + 7) // 8, "big").decode()

import unittest
class Test(unittest.TestCase):
    def test_ok(self):
        original = 'test this!'
        dummy, encrypted = encrypt(original)
        self.assertEqual(original, decrypt(dummy, encrypted))
