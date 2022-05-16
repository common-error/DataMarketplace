import hashlib

def _byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def _hash(_data):
    return hashlib.sha3_256(_data.encode('utf-8')).hexdigest()

K_from = bytes.fromhex("a96158bfb7d7efd093e4750c62c6652a510eff9ad027a5c5ebea5600292fe6a4")
K_to = bytes.fromhex("e7c41af5a5a346bae4611c592bc95689ff71fae2adf32a807e599c0c50c0fbdb")
l_to = bytes.fromhex("ce2e711b2b8991ca05c595f17b7fd2f9452d32211dea37dc40c7467c684232be")
xor_Kl = _byte_xor(K_from,l_to)

hash_kl = bytes.fromhex(_hash(xor_Kl.hex()))

token = _byte_xor(K_to,hash_kl).hex()

print(token)