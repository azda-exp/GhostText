
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64

def encrypt_message():

    message = input("Enter message: ")

    with open("public.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    encrypted_message = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open("message.enc", "wb") as f:
        f.write(encrypted_message)

    encoded = base64.b64encode(encrypted_message).decode()

    print("\nOriginal Message:")
    print(message)

    print("\nEncrypted Message:")
    print(encoded)

    print("\n[+] Message encrypted!")

def decrypt_message():

    with open("private.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    with open("message.enc", "rb") as f:
        encrypted_message = f.read()

    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    print("\nDecrypted Message:")
    print(decrypted_message.decode())

def decrypt_file():

    filename = input("Enter encrypted filename: ")

    with open("private.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    with open("encrypted_key.bin", "rb") as f:
        encrypted_key = f.read()

    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    cipher = Fernet(aes_key)

    with open(filename, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = cipher.decrypt(encrypted_data)

    output_file = "recovered_" + filename.replace(".enc", "")

    with open(output_file, "wb") as f:
        f.write(decrypted_data)

    print(f"[+] File recovered as {output_file}")

def encrypt_file():

    filename = input("Enter filename: ")

    with open("public.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    aes_key = Fernet.generate_key()
    cipher = Fernet(aes_key)

    with open(filename, "rb") as f:
        data = f.read()

    encrypted_data = cipher.encrypt(data)

    with open(filename + ".enc", "wb") as f:
        f.write(encrypted_data)

    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open("encrypted_key.bin", "wb") as f:
        f.write(encrypted_key)

    print(f"[+] {filename} encrypted successfully!")

def generate_keys():

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    with open("private.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    with open("public.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    print("[+] Keys generated successfully!")

def menu():
    print("\n====================")
    print("      GhostText")
    print("====================")
    print("1. Generate Keys")
    print("2. Encrypt Message")
    print("3. Decrypt Message")
    print("4. Encrypt File")
    print("5. Decrypt File")
    print("6. Exit")

while True:
    menu()

    choice = input("\nChoose: ")

    if choice == "1":
        generate_keys()

    elif choice == "2":
        encrypt_message()

    elif choice == "3":
        decrypt_message()

    elif choice == "4":
        encrypt_file()

    elif choice == "5":
        decrypt_file()

    elif choice == "6":
        print("Goodbye!")
        break

    else:
        print("Invalid option!")