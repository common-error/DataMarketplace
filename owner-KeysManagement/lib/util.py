from cryptography.fernet import Fernet
import base64

def crypt(_key,_data):
    f = Fernet(base64.urlsafe_b64encode(bytes.fromhex(_key)))
    return f.encrypt(_data)

def decrypt(_key,_data):
    f = Fernet(base64.urlsafe_b64encode(bytes.fromhex(_key)))

    return f.decrypt(_data)