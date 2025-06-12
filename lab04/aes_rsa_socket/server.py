import socket
import threading
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# Tạo RSA key pair của server
server_key = RSA.generate(2048)
server_public_key = server_key.publickey()

# Tạo socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen()

print("Server is listening on port 12345...")

clients = []  # Danh sách client đang kết nối
client_keys = {}  # Lưu AES key tương ứng từng client

# Hàm mã hóa tin nhắn với AES
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext

# Hàm giải mã tin nhắn với AES
def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted_message[AES.block_size:]), AES.block_size)
    return decrypted.decode()

# Xử lý một client
def handle_client(client_socket, client_address):
    print(f"[+] New connection from {client_address}")
    try:
        # Gửi public key của server cho client
        client_socket.send(server_public_key.export_key())

        # Nhận public key từ client
        client_pubkey_data = client_socket.recv(2048)
        client_pubkey = RSA.import_key(client_pubkey_data)

        # Sinh AES key và gửi cho client (RSA mã hóa)
        aes_key = get_random_bytes(16)
        cipher_rsa = PKCS1_OAEP.new(client_pubkey)
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)
        client_socket.send(encrypted_aes_key)

        # Lưu lại socket và AES key
        clients.append(client_socket)
        client_keys[client_socket] = aes_key

        # Nhận và phát tán tin nhắn
        while True:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break

            message = decrypt_message(aes_key, encrypted_message)
            print(f"[{client_address}] {message}")

            if message.lower() == "exit":
                break

            # Gửi tin nhắn đến các client khác
            for client in clients:
                if client != client_socket:
                    encrypted = encrypt_message(client_keys[client], f"[{client_address}] {message}")
                    client.send(encrypted)

    except Exception as e:
        print(f"Error with client {client_address}: {e}")
    finally:
        client_socket.close()
        clients.remove(client_socket)
        del client_keys[client_socket]
        print(f"[-] Connection closed with {client_address}")

# Lặp chờ kết nối từ client
while True:
    client_sock, client_addr = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_sock, client_addr))
    thread.start()
