# IMPORTS
import hashlib
import binascii
import secrets
from unicodedata import normalize
import base64
import base58

# Recovery Phrase Generation - set up by default for 24 word recovery phrase, with passphrase as optional
def generate_recovery_phrase(bits:int=256, iterations:int=256, key_bytes:int=64, hash_name:str='sha512', passphrase:str="") -> str:

    with open("wordlist/english.txt", 'r') as file:
        wordlist = file.read().splitlines()

    # Check that the number of bits is divisible by 32
    if bits % 32 != 0:
        raise ValueError("The number of bits must be divisible by 32")

    # Generate a random number
    entropy = secrets.token_bytes(bits // 8)

    # Calculate the checksum
    checksum = hashlib.sha256(entropy).digest()

    # Add the checksum to the entropy
    bits = bin(int(binascii.hexlify(entropy + checksum[:(bits // 32) // 8]), 16))[2:].zfill(bits + bits // 32)

    # Convert to mnemonic
    phrase = []
    for i in range(len(bits) // 11):
        idx = int(bits[i * 11:(i + 1) * 11], 2)
        phrase.append(wordlist[idx])
    
    
    salt = str("".join(phrase)) + normalize('NFKD', passphrase)
    seed = hashlib.pbkdf2_hmac(hash_name, normalize('NFKD', " ".join(phrase)).encode(), salt.encode(), iterations, key_bytes)

    return {
        "phrase": " ".join(phrase),
        "entropy": entropy,
        "entropy_hex": binascii.hexlify(entropy).decode(),
        "entropy_base64": base64.b64encode(entropy).decode(),
        "entropy_base58": base58.b58encode(entropy).decode(),
        "entropy_int": int.from_bytes(entropy, 'big'),
        "seed": seed,
        "seed_hex": binascii.hexlify(seed).decode(),
        "seed_base64": base64.b64encode(seed).decode(),
        "seed_base58": base58.b58encode(seed).decode(),
        "seed_int": int.from_bytes(seed, 'big'),
    }

