import sys
from monrsa.crypto import *

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
