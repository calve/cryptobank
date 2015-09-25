from monrsa.crypto import generate_keys
import base64
import json


def save_rsa_keys(pub_path, private_path):
    """
    Saves a pair of rsa keys
    """
    myKey = generate_keys()
    public_key    = open(pub_path, "w")
    private_key   = open(private_path, "w")
    public_key.write(str(myKey.get_pub().decode()))
    private_key.write(str(myKey.get_private().decode()))
    public_key.close()
    private_key.close()




def serialize(o):
    """
    Encode a python dictionnary to a printable base64-encoded string
    """
    return base64.b64encode(json.dumps(o).encode())


def unserialize(s):
    """
    Decode a base64-encoded string to a python dictionnary
    """
    return json.loads(base64.b64decode(s).decode())
