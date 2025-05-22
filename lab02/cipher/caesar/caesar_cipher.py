from string import ascii_uppercase

ALPHABET = ascii_uppercase

class CaesarCipher:
    def encrypt_text(self, text: str, key: int) -> str:
        alphabet_len = len(ALPHABET)
        encrypted_text = ""
        for letter in text:
            if letter in ALPHABET:
                letter_index = ALPHABET.index(letter)
                encrypted_index = (letter_index + key) % alphabet_len
                encrypted_text += ALPHABET[encrypted_index]
            else:
                encrypted_text += letter
        return "".join(encrypted_text)

    def decrypt_text(self, text: str, key: int) -> str:
        alphabet_len = len(ALPHABET)
        decrypted_text = ""
        for letter in text:
            if letter in ALPHABET:
                letter_index = ALPHABET.index(letter)
                decrypted_index = (letter_index - key) % alphabet_len
                decrypted_text += ALPHABET[decrypted_index]
            else:
                decrypted_text += letter
        return "".join(decrypted_text)