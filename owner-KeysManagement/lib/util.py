from cryptography.fernet import Fernet
import base64

def crypt(_key,_data):
    f = Fernet(base64.urlsafe_b64encode(bytes.fromhex(_key)))
    return f.encrypt(_data)

def decrypt(_key,_data):
    f = Fernet(base64.urlsafe_b64encode(bytes.fromhex(_key)))

    return f.decrypt(_data)

"""
Function used to find which tokens have been modified during an update
"""
def modifiedResources(_oldCatalogue,_newCatalogue):
    common_el = (_newCatalogue & _oldCatalogue)

    to_remove = _oldCatalogue - common_el
    to_add = list(_newCatalogue - common_el)
    for fr,to,tok in to_remove:
        to_add.append((fr,to,""))

    return to_add