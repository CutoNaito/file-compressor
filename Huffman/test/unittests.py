import unittest

from src.Huffman import Huffman


class TestHuffman(unittest.TestCase):
    def test_make_freq_dict(self):
        huffman = Huffman("hello")
        freq_dict = huffman.make_freq_dict()
        self.assertEqual(freq_dict, {'h': 1, 'e': 1, 'l': 2, 'o': 1})

    def test_make_codes(self):
        huffman = Huffman("hello")
        huffman.make_codes()
        self.assertEqual(huffman.codes, {'h': '00', 'e': '01', 'l': '10', 'o': '11'})

    def test_get_encoded_text(self):
        huffman = Huffman("hello")
        huffman.make_codes()
        encoded_text = huffman.get_encoded_text()
        self.assertEqual(encoded_text, '0010101110111')


if __name__ == '__main__':
    unittest.main()
