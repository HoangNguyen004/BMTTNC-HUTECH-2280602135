# cipher/caesar.py
from string import ascii_uppercase

ALPHABET = ascii_uppercase

class CaesarCipher:
    @staticmethod
    def encrypt_text(text: str, key: int) -> str:
        alphabet_len = len(ALPHABET)
        encrypted_text = ""
        for letter in text.upper():
            if letter in ALPHABET:
                letter_index = ALPHABET.index(letter)
                encrypted_index = (letter_index + key) % alphabet_len
                encrypted_text += ALPHABET[encrypted_index]
            else:
                encrypted_text += letter
        return encrypted_text

    @staticmethod
    def decrypt_text(text: str, key: int) -> str:
        alphabet_len = len(ALPHABET)
        decrypted_text = ""
        for letter in text.upper():
            if letter in ALPHABET:
                letter_index = ALPHABET.index(letter)
                decrypted_index = (letter_index - key) % alphabet_len
                decrypted_text += ALPHABET[decrypted_index]
            else:
                decrypted_text += letter
        return decrypted_text
