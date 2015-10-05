import unittest
from cryptobank.monrsa.blocks import split, assemble
from cryptobank.test.unittests import randomword


class TestBlocks(unittest.TestCase):

    def test_long_word(self):
        rawdata = bytes(randomword(30).encode())
        blocks = split(rawdata, 15)
        self.assertEqual(assemble(blocks), rawdata)
        self.assertNotEqual(assemble(blocks[:-1]), rawdata)

    def test_long_word_long_split(self):
        rawdata = bytes(randomword(4098).encode())
        blocks = split(rawdata, 256)
        self.assertEqual(assemble(blocks), rawdata)
        self.assertNotEqual(assemble(blocks[:-1]), rawdata)

    def test_all_word(self):
        for i in range(1, 2**10):
            rawdata = bytes(randomword(i).encode())
            blocks = split(rawdata, 15)
            self.assertEqual(assemble(blocks), rawdata)

    def test_padd_one(self):
        rawdata = bytes(randomword(29).encode())
        blocks = split(rawdata, 10)
        self.assertEqual(assemble(blocks), rawdata)

    def test_padd_two(self):
        rawdata = bytes(randomword(28).encode())
        blocks = split(rawdata, 10)
        self.assertEqual(assemble(blocks), rawdata)

    def test_no_padd(self):
        rawdata = bytes(randomword(30).encode())
        blocks = split(rawdata, 10)
        self.assertEqual(assemble(blocks), rawdata)

    def test_split(self):
        rawdata = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        blocks = split(rawdata, 16)
        self.assertEqual(b"ABCDEFGHIJKLMNOP", blocks[0])
        self.assertEqual(b"QRSTUVWXYZ\0\6\0\0\0\0", blocks[1])

    def test_resplit(self):
        rawdata = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        blocks = split(rawdata, 5)
        self.assertEqual([b'ABCDE', b'FGHIJ', b'KLMNO', b'PQRST', b'UVWXY', b'Z\0\4\0\0'], blocks)
