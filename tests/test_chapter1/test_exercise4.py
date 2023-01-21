from exercises.chapter1 import exercise4

import pytest


@pytest.mark.parametrize("message", [
    "Hello world!",
    "The cuckoo has flown the nest.",
    "What's for dinner?"
])
def test_encrypt_decrypt(message):
    key, ciphertext = exercise4.encrypt(message)
    plaintext: str = exercise4.decrypt(key, ciphertext)
    assert plaintext == message