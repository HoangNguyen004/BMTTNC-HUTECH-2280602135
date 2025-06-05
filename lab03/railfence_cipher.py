import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox

class RailFenceCipher:
    def rail_fence_encrypt(self, plain_text, num_rails):
        if num_rails <= 1:
            return plain_text
        rails = [[] for _ in range(num_rails)]
        rail_index = 0
        direction = 1  # 1: xuống, -1: lên
        for char in plain_text:
            rails[rail_index].append(char)
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction
        return "".join("".join(rail) for rail in rails)

    def rail_fence_decrypt(self, cipher_text, num_rails):
        if num_rails <= 1:
            return cipher_text
        rail_lengths = [0] * num_rails
        rail_index = 0
        direction = 1
        for _ in cipher_text:
            rail_lengths[rail_index] += 1
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        rails = []
        start = 0
        for length in rail_lengths:
            rails.append(list(cipher_text[start : start + length]))
            start += length

        result = ""
        rail_index = 0
        direction = 1
        for _ in cipher_text:
            result += rails[rail_index].pop(0)
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction
        return result

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/vigenere.ui', self)  # Đường dẫn UI

        self.cipher = RailFenceCipher()

        # Bắt sự kiện nút
        self.btn_encrypt.clicked.connect(self.encrypt_text)
        self.btn_decrypt.clicked.connect(self.decrypt_text)
        self.btn_encrypt_2.clicked.connect(self.encrypt_text)  # Nút ENCRYPT phụ

        self.show()

    def encrypt_text(self):
        plain_text = self.txt_plain_text.toPlainText().strip()
        key = self.txt_key.toPlainText().strip()
        if not plain_text or not key.isdigit():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập PLAIN_TEXT và KEY là số nguyên.")
            return
        num_rails = int(key)
        cipher_text = self.cipher.rail_fence_encrypt(plain_text, num_rails)
        self.txt_cipher_text.setPlainText(cipher_text)

    def decrypt_text(self):
        cipher_text = self.txt_cipher_text.toPlainText().strip()
        key = self.txt_key.toPlainText().strip()
        if not cipher_text or not key.isdigit():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập CIPHER_TEXT và KEY là số nguyên.")
            return
        num_rails = int(key)
        plain_text = self.cipher.rail_fence_decrypt(cipher_text, num_rails)
        self.txt_plain_text.setPlainText(plain_text)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
