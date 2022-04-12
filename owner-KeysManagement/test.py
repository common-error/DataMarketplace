from cryptography.fernet import Fernet
import secrets
import hashlib
import base64


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

"""

ka = base64.urlsafe_b64decode(Fernet.generate_key())
kc = base64.urlsafe_b64decode(Fernet.generate_key())
lc = secrets.token_bytes(32)

f = Fernet(base64.urlsafe_b64encode(kc))
token = f.encrypt(b"my deep dark secret")

print(token)


hash_ka = hashlib.sha3_256(ka).digest()
hash_lc = hashlib.sha3_256(lc).digest()

print(type(hash_ka))

T_ac = byte_xor(kc,hashlib.sha3_256(hash_ka + hash_lc).digest())


new_kc = byte_xor(T_ac,hashlib.sha3_256(hash_ka + hash_lc).digest())


if kc == new_kc:
    print("true")
    f = Fernet(base64.urlsafe_b64encode(new_kc))

    print(f.decrypt(token))
else:
    print("false")

"""

x = ["x","x"]
y = ["y","y","y"]
z = ["r1","r5"]

hash = bytearray(32)
hash1 = bytearray(32)
hash2 = bytearray(32)

for el in x:
    hash = byte_xor(hash, hashlib.sha3_256(el.encode('utf-8')).digest())

for el in y:
    hash1 = byte_xor(hash1, hashlib.sha3_256(el.encode('utf-8')).digest())

for el in z:
    hash2 = byte_xor(hash2, hashlib.sha3_256(el.encode('utf-8')).digest())

print(hash == hash1)
print(hash == hash2)