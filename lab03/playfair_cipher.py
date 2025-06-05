# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from ui.playfair import Ui_MainWindow


class PlayfairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        key = key.replace("J", "I").upper()
        seen = set()
        matrix = []

        for char in key:
            if char not in seen and char.isalpha():
                seen.add(char)
                matrix.append(char)

        for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # J is merged with I
            if char not in seen:
                seen.add(char)
                matrix.append(char)

        return [matrix[i:i + 5] for i in range(0, 25, 5)]

    def find_letter_coords(self, matrix, letter):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col
        return None, None

    def preprocess_text(self, text):
        text = text.replace("J", "I").upper()
        result = ""
        i = 0
        while i < len(text):
            a = text[i]
            b = text[i + 1] if i + 1 < len(text) else "X"
            if a == b:
                result += a + "X"
                i += 1
            else:
                result += a + b
                i += 2
        if len(result) % 2 == 1:
            result += "X"
        return result

    def playfair_encrypt(self, plain_text, matrix):
        plain_text = self.preprocess_text(plain_text)
        cipher_text = ""

        for i in range(0, len(plain_text), 2):
            a, b = plain_text[i], plain_text[i + 1]
            row1, col1 = self.find_letter_coords(matrix, a)
            row2, col2 = self.find_letter_coords(matrix, b)

            if row1 == row2:
                cipher_text += matrix[row1][(col1 + 1) % 5]
                cipher_text += matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                cipher_text += matrix[(row1 + 1) % 5][col1]
                cipher_text += matrix[(row2 + 1) % 5][col2]
            else:
                cipher_text += matrix[row1][col2]
                cipher_text += matrix[row2][col1]

        return cipher_text

    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = cipher_text.upper()
        plain_text = ""

        for i in range(0, len(cipher_text), 2):
            a, b = cipher_text[i], cipher_text[i + 1]
            row1, col1 = self.find_letter_coords(matrix, a)
            row2, col2 = self.find_letter_coords(matrix, b)

            if row1 == row2:
                plain_text += matrix[row1][(col1 - 1) % 5]
                plain_text += matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                plain_text += matrix[(row1 - 1) % 5][col1]
                plain_text += matrix[(row2 - 1) % 5][col2]
            else:
                plain_text += matrix[row1][col2]
                plain_text += matrix[row2][col1]

        return plain_text


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cipher = PlayfairCipher()

        self.ui.btn_encrypt.clicked.connect(self.encrypt)
        self.ui.btn_decrypt.clicked.connect(self.decrypt)

    def encrypt(self):
        key = self.ui.txt_key.toPlainText()
        plain_text = self.ui.txt_plain_text.toPlainText()
        matrix = self.cipher.create_playfair_matrix(key)
        result = self.cipher.playfair_encrypt(plain_text, matrix)

        # hiển thị kết quả
        self.ui.txt_cipher_text.setPlainText(result)
        self.display_matrix(matrix)

    def decrypt(self):
        key = self.ui.txt_key.toPlainText()
        cipher_text = self.ui.txt_cipher_text.toPlainText()
        matrix = self.cipher.create_playfair_matrix(key)
        result = self.cipher.playfair_decrypt(cipher_text, matrix)

        # hiển thị kết quả
        self.ui.txt_plain_text.setPlainText(result)
        self.display_matrix(matrix)

    def display_matrix(self, matrix):
        output = ""
        for row in matrix:
            output += " ".join(row) + "\n"
        self.ui.txt_matrix.setPlainText(output.strip())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
