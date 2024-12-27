import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import hashlib

def encrypt_file_aes(file_data, aes_key):
    block_size = algorithms.AES.block_size
    padder = PKCS7(block_size).padder()
    padded_data = padder.update(file_data) + padder.finalize()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv, ciphertext


def decrypt_file_aes(ciphertext, aes_key, iv):
    block_size = algorithms.AES.block_size

    try:
        cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = PKCS7(block_size).unpadder()
        plaintext = unpadder.update(padded_data) + unpadder.finalize()
        return plaintext
    except Exception as e:
        raise ValueError("Decryption failed:", e)
    

def rsa_key_generation():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(b'private')
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    key_path = os.path.join(os.getcwd())
    os.makedirs(key_path, exist_ok=True)

    private_key_path = os.path.join(key_path, "Private_key.pem")
    with open(private_key_path, "wb") as key_file:
        key_file.write(private_pem)

    public_key_path = os.path.join(key_path, "Public_key.pem")
    with open(public_key_path, "wb") as key_file:
        key_file.write(public_pem)


def encrypt_file_rsa(file_data, public_key_path):
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    
    encrypted_file = public_key.encrypt(
        file_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_file


def decrypt_file_rsa(encrypted_data, private_key_path):
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=b'private',
            backend=default_backend()
        )

    decrypted_file = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_file


def sign_file(file_data, private_key_path):
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=b'private',
            backend=default_backend()
        )
    
    signature = private_key.sign(
        file_data,
        padding.PSS(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature


def verify_sign(signature, file_data, public_key_path):
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    
    try:
        public_key.verify(
            signature,
            file_data,
            padding.PSS(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print("Error:", e)


def compute_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256_hash.update(chunk)
    
    return sha256_hash.hexdigest()


def main():
    pubkey_path = "C:\\Users\\USER\\Desktop\\ota\\practice\\Public_key.pem"
    prvkey_path = "C:\\Users\\USER\\Desktop\\ota\\practice\\Private_key.pem"
    test_path = "C:\\Users\\USER\\Desktop\\ota\\practice\\test.txt"

    with open(test_path, "rb") as file:
        file_data = file.read()
        
    # aes_key = os.urandom(16)
    # print("AES Key:", aes_key)
    # with open("test.txt", "rb") as f:
    #     file_data = f.read()
    # print("Plain text:", file_data)

    # iv, ciphertext = encrypt_file_aes(file_data, aes_key)
    # print("Encrypted text:", ciphertext)

    # plaintext = decrypt_file_aes(ciphertext, aes_key, iv)
    # print("Decrypted text:", plaintext)

    # 
    # rsa_key_generation()
    # enc = encrypt_file_rsa(file_data, pubkey_path)
    # print(decrypt_file_rsa(enc, prvkey_path))

    # file_hash = compute_file_hash(test_path)
    # print("File hash:", file_hash)

    sign = sign_file(file_data, prvkey_path)
    print(verify_sign(sign, file_data, pubkey_path))

if __name__ == "__main__":
    main()