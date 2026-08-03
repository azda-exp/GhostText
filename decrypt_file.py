from cryptography.fernet import Fernet

with open("filekey.key", "rb") as f:
    key = f.read()

cipher = Fernet(key)

with open("secret.txt.enc", "rb") as f:
    encrypted_data = f.read()

decrypted = cipher.decrypt(encrypted_data)

print(decrypted)
print("Length:", len(decrypted))

with open("secret_decrypted.txt", "wb") as f:
    f.write(decrypted)