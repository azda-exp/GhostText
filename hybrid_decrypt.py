from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Load RSA private key
with open("private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

# Load encrypted AES key
with open("encrypted_key.bin", "rb") as f:
    encrypted_key = f.read()

# Recover AES key
aes_key = private_key.decrypt(
    encrypted_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

cipher = Fernet(aes_key)

# Load encrypted file
with open("secret.txt.enc", "rb") as f:
    encrypted_data = f.read()

decrypted_data = cipher.decrypt(encrypted_data)

with open("recovered_secret.txt", "wb") as f:
    f.write(decrypted_data)

print("Hybrid decryption completed.")