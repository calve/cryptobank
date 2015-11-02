# Usage: ./verify.sh <signed> <original_data> <public_key_to_use>
signed_sha1=`base64 --decode $1 | openssl rsautl -pubin -inkey $3 -encrypt -raw | strings`
original_sha1=`sha1sum $2 | awk '{print $1}' | strings`
[ "$signed_sha1" = "$original_sha1" ]
