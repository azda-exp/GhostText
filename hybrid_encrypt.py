from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Load RSA public key
with open("public.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# Generate AES key
aes_key = Fernet.generate_key()

cipher = Fernet(aes_key)

# Encrypt file
with open("secret.txt", "rb") as f:
    data = f.read()

encrypted_data = cipher.encrypt(data)

with open("secret.txt.enc", "wb") as f:
    f.write(encrypted_data)

# Encrypt AES key with RSA
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

print("Hybrid encryption completed.")