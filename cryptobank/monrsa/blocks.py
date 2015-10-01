def split(rawdata, size):
    """
    Split rawdata in block of size bytes.
    Padd the last bytes with ``\00<total_padding_size>\00\00``
    """
    result = []
    assert(size <= 256)
    for i in range(0, len(rawdata), size):
        if i + size <= len(rawdata):
            result.append(rawdata[i:i+size])
        else:
            # Looks likes we need to add padding
            modulo = len(rawdata) % size
            padd = size - modulo
            padded = rawdata[i:i+modulo] + _compute_padding(padd)
            result.append(padded)
    return result


def assemble(blocks):
    """
    Reassemble blocks
    """
    result = bytearray()
    for block in blocks:
        for byte in block:
            result.append(byte)
    # Was it padded ?
    if result[-1] <= 2:
        for i in range(1, len(result)):
            if result[-i] != 0:
                number_of_bytes = result[-i]
                break
        # Verify that all padded bytes are actually padded bytes
        padding = result[-number_of_bytes:]

        if padding != _compute_padding(number_of_bytes):
            raise Exception("Error un-padding : {} != {}".format(
                padding,
                _compute_padding(number_of_bytes)
            ))
        return result[:-number_of_bytes]
    return result


def _compute_padding(n):
    if n == 1:
        return bytes([1])
    try:
        return bytes([0, n]) + bytes(n-2)
    except ValueError:
        return bytes([0, n])
