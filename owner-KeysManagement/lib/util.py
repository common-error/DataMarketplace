from cryptography.fernet import Fernet
import base64

def crypt(_key,_data):
    f = Fernet(base64.urlsafe_b64encode(bytes.fromhex(_key)))
    return f.encrypt(_data).decode()

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

    ret = []
    for fr,to,token,label in to_remove:
        ret.append((fr,to,"",""))

    
    ret.extend(to_add)
    print("{},{}".format(len(to_remove),len(to_add)))
    return to_add,len(to_remove),len(to_add)

def saveResult(_text,_path):
    with open(_path, "a+") as f:
        f.write(_text)