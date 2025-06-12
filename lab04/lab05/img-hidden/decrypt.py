import sys
from PIL import Image

def decode_image(encoded_image_path):
    img = Image.open(encoded_image_path)
    width, height = img.size
    binary_message = ""

    # Trích xuất từng bit cuối của mỗi kênh màu
    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))
            for color_channel in range(3):
                binary_message += format(pixel[color_channel], '08b')[-1]

    # Tìm vị trí kết thúc: '1111111111111110' (16 bits)
    end_marker = '1111111111111110'
    end_index = binary_message.find(end_marker)

    if end_index == -1:
        print("Không tìm thấy thông điệp ẩn.")
        return ""

    binary_message = binary_message[:end_index]  # Cắt đến trước marker

    # Chuyển từng 8 bit thành ký tự
    decoded_message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        decoded_message += chr(int(byte, 2))

    return decoded_message

def main():
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return

    encoded_image_path = sys.argv[1]
    decoded_message = decode_image(encoded_image_path)
    print("Decoded message:", decoded_message)

if __name__ == "__main__":
    main()
