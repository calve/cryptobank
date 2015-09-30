import unittest
from cryptobank.monrsa.blocks import split, assemble
from cryptobank.test.unittests import randomword


class TestBlocks(unittest.TestCase):

    def test_random_words(self):
        word = randomword(4096)
        self.assertEquals(assemble(split(word, 16)), word)
