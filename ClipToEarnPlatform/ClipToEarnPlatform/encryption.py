from cryptography.fernet import Fernet
import os
import base64

# Generate or load encryption key
def get_encryption_key():
    key = os.environ.get('ENCRYPTION_KEY')
    if not key:
        # Generate a new key if not found (for development)
        key = Fernet.generate_key()
        print(f"Generated new encryption key: {key.decode()}")
        print("Add this to your environment variables as ENCRYPTION_KEY")
    else:
        key = key.encode()
    return key

# Initialize cipher
def get_cipher():
    return Fernet(get_encryption_key())

def encrypt_iban(iban):
    """Encrypt IBAN for secure storage"""
    if not iban:
        return None
    cipher = get_cipher()
    return cipher.encrypt(iban.encode()).decode()

def decrypt_iban(encrypted_iban):
    """Decrypt IBAN for display/processing"""
    if not encrypted_iban:
        return None
    try:
        cipher = get_cipher()
        return cipher.decrypt(encrypted_iban.encode()).decode()
    except Exception:
        # Return the original value if decryption fails (might be unencrypted)
        return encrypted_iban

def mask_iban(iban):
    """Mask IBAN for display purposes (show only first 4 and last 4 characters)"""
    if not iban:
        return None
    if len(iban) < 8:
        return iban
    return iban[:4] + '*' * (len(iban) - 8) + iban[-4:]