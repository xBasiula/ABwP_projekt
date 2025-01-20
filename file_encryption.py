import os
from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import zipfile
import itertools
import string

app = Flask(__name__)

# AES Szyfrowanie plików
def encrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        data = f.read()
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    with open(output_file, 'wb') as f:
        f.write(cipher.iv + ciphertext)

def decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        data = f.read()
    iv = data[:AES.block_size]
    ciphertext = data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    with open(output_file, 'wb') as f:
        f.write(plaintext)

# Brute Force na ZIP
def brute_force_zip(zip_file, max_length=4):
    charset = string.ascii_lowercase
    with zipfile.ZipFile(zip_file) as zf:
        for length in range(1, max_length + 1):
            for password in map(''.join, itertools.product(charset, repeat=length)):
                try:
                    zf.extractall(pwd=password.encode('utf-8'))
                    return password
                except (RuntimeError, zipfile.BadZipFile):
                    continue
    return None

# Endpointy API
@app.route('/encrypt', methods=['POST'])
def encrypt_endpoint():
    file_path = request.json['file_path']
    output_path = request.json['output_path']
    key = request.json['key'].encode('utf-8')
    if len(key) != 16:
        return jsonify({'error': 'Key must be 16 bytes long'}), 400
    encrypt_file(file_path, output_path, key)
    return jsonify({'message': f'File encrypted and saved to {output_path}'})

@app.route('/decrypt', methods=['POST'])
def decrypt_endpoint():
    file_path = request.json['file_path']
    output_path = request.json['output_path']
    key = request.json['key'].encode('utf-8')
    if len(key) != 16:
        return jsonify({'error': 'Key must be 16 bytes long'}), 400
    decrypt_file(file_path, output_path, key)
    return jsonify({'message': f'File decrypted and saved to {output_path}'})

@app.route('/bruteforce', methods=['POST'])
def brute_force_endpoint():
    zip_file = request.json['zip_file']
    max_length = request.json.get('max_length', 4)
    password = brute_force_zip(zip_file, max_length)
    if password:
        return jsonify({'password': password})
    else:
        return jsonify({'error': 'Password not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)