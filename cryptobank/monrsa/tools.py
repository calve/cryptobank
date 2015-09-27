from monrsa.crypto import generate_keys
import base64
import json


def _deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()

def generate_database(db_name):
    """
    Generates a blank file for the bank to use as a database
    """
    with open(db_name, "w") as file_:
        file_.write("")


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

def import_key(path):
    """
    The object "Key" only deals with bytes. We therefore have to make sure that anything we import pass to the object is a byte
    """
    with open("ex2_key", "r") as file_:
        key_import = file_.read()
    return key_import.encode()

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
