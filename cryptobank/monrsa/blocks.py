def split(rawdata, size):
    """
    Split rawdata in block of size bytes
    """
    result = []
    for i in range(0, len(rawdata), size):
        if i + size <= len(rawdata):
            result.append(rawdata[i:i+size])
        else:
            # Looks likes we need to add padding
            modulo = len(rawdata) % size
            padd = size - modulo
            padded = rawdata[i:i+modulo] + (bytes([padd]) * padd)
            # print("padded : {}".format(padded))
            result.append(padded)
            # print("need to pad")
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
    if result[-1] < ord(" "):
        number_of_bytes = result[-1]
        # Verify that all padded bytes are actually padded bytes
        padding = result[-number_of_bytes:]
        if padding != bytes([number_of_bytes]) * number_of_bytes:
            raise Exception("Error un-padding")
        return result[:-number_of_bytes]
    return result
