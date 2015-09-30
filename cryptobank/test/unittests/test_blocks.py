import unittest
from cryptobank.monrsa.blocks import split, assemble
from cryptobank.test.unittests import randomword


class TestBlocks(unittest.TestCase):

    def test_long_word(self):
        rawdata = bytes(randomword(4096).encode())
        blocks = split(rawdata, 15)
        self.assertEqual(assemble(blocks), rawdata)
        self.assertNotEqual(assemble(blocks[:-1]), rawdata)

    def test_short_word(self):
        rawdata = bytes(randomword(40).encode())
        blocks = split(rawdata, 15)
        self.assertEqual(assemble(blocks), rawdata)
        self.assertNotEqual(assemble(blocks[:-1]), rawdata)

    def test_padding(self):
        rawdata = bytes(randomword(18).encode())
        blocks = split(rawdata, 16)
        self.assertEqual(blocks[-1][-1], 14)

    def test_split(self):
        rawdata = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        blocks = split(rawdata, 16)
        self.assertEqual(b"ABCDEFGHIJKLMNOP", blocks[0])
        self.assertEqual(b"QRSTUVWXYZ\6\6\6\6\6\6", blocks[1])

    def test_resplit(self):
        rawdata = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        blocks = split(rawdata, 5)
        self.assertEqual([b'ABCDE', b'FGHIJ', b'KLMNO', b'PQRST', b'UVWXY', b'Z\4\4\4\4'], blocks)
