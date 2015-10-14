# Usage: ./sign.sh <data_to_sign> <private_key_to_use>
sha1sum $1 | awk '{print $1}' | openssl rsautl -inkey $2 -decrypt -raw | base64 -w0


