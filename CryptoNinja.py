import os
import random
import hashlib
from PIL import Image
from Crypto.Cipher import Salsa20
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes

def salsa20_encrypt(data, password, salt):
    key = scrypt(password.encode(), salt, key_len=32, N=2**14, r=8, p=1)
    cipher = Salsa20.new(key=key)
    checksum = hashlib.md5(data).digest()
    encrypted_data = cipher.nonce + cipher.encrypt(checksum + data)
    return encrypted_data

def salsa20_decrypt(data, password, salt):
    key = scrypt(password.encode(), salt, key_len=32, N=2**14, r=8, p=1)
    nonce = data[:8]
    ciphertext = data[8:]
    cipher = Salsa20.new(key=key, nonce=nonce)
    decrypted_data = cipher.decrypt(ciphertext)
    checksum, plaintext = decrypted_data[:16], decrypted_data[16:]
    eof_index = plaintext.find(bytes([0x04]))
    if eof_index == -1 or hashlib.md5(plaintext[:eof_index + 1]).digest() != checksum:
        raise ValueError("Invalid password or corrupted data.")
    return plaintext[:eof_index]

def embed_data_in_png(image_path, data, output_path, salt):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pixels = list(img.getdata())
    
    data_with_salt = salt + data
    
    max_capacity = len(pixels) * 3
    if len(data_with_salt) * 8 > max_capacity:
        raise ValueError("Data is too large to fit in the image.")
    
    start_position = random.randint(0, max_capacity - len(data_with_salt) * 8)

    for i in range(24):
        bit = (start_position >> (23 - i)) & 1
        pixel_idx, channel = divmod(i, 3)
        pixel = list(pixels[pixel_idx])
        pixel[channel] = (pixel[channel] & ~1) | bit
        pixels[pixel_idx] = tuple(pixel)

    bit_index = 0
    for byte in data_with_salt:
        for i in range(8):
            bit = (byte >> (7 - i)) & 1
            pixel_idx, channel = divmod(start_position + bit_index, 3)
            pixel = list(pixels[pixel_idx])
            pixel[channel] = (pixel[channel] & ~1) | bit
            pixels[pixel_idx] = tuple(pixel)
            bit_index += 1
    
    img.putdata(pixels)
    img.save(output_path)
    print(f"Data successfully embedded in {output_path}")

def extract_data_from_png(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    
    start_position = 0
    for i in range(24):
        pixel_idx, channel = divmod(i, 3)
        start_position = (start_position << 1) | (pixels[pixel_idx][channel] & 1)

    data = []
    bit_buffer = 0
    bit_count = 0
    for i in range(start_position, len(pixels) * 3):
        pixel_idx, channel = divmod(i, 3)
        bit = pixels[pixel_idx][channel] & 1
        bit_buffer = (bit_buffer << 1) | bit
        bit_count += 1
        if bit_count == 8:
            data.append(bit_buffer)
            bit_buffer = 0
            bit_count = 0
    
    return bytes(data)

def main():
    print("Crypto Ninja 1.0 (Steganography and Encryption Tool)")
    print("This tool allows you to hide and extract encrypted data in PNG files.\n")
    print("Instructions:")
    print("1. Choose mode: Hide data (1) or Extract data (2).")
    print("2. Provide the required file paths and a password.")
    print("3. The tool will securely encrypt and embed the data (or extract and decrypt it).\n")
    
    mode = input("Choose mode (1 - Hide Data, 2 - Extract Data): ")
    
    if mode == "1":
        text = input("Enter text to hide: ")
        password = input("Enter password: ")
        image_path = input("Enter path to PNG image: ")
        output_path = input("Enter path for output PNG: ")
        
        if not os.path.exists(image_path):
            print("The provided image file does not exist.")
            return
        
        salt = get_random_bytes(16)

        encrypted_data = salsa20_encrypt(text.encode() + bytes([0x04]), password, salt)

        try:
            embed_data_in_png(image_path, encrypted_data, output_path, salt)
        except ValueError as e:
            print(f"Error: {e}")
    
    elif mode == "2":
        password = input("Enter password: ")
        image_path = input("Enter path to PNG image: ")
        
        if not os.path.exists(image_path):
            print("The provided image file does not exist.")
            return
        
        try:
            encrypted_data = extract_data_from_png(image_path)

            salt = encrypted_data[:16]
            
            decrypted_data = salsa20_decrypt(encrypted_data[16:], password, salt)
            print(f"Decrypted text: {decrypted_data.decode()}")
        except ValueError:
            print("Incorrect password or no hidden data in the file.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Invalid mode selected.")

if __name__ == "__main__":
    main()
