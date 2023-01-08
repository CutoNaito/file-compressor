from Huffman import *
import math
import os
import time
import sys


def main():
    """
    This is the main function
    :return:
    """
    start = time.time()
    path = read_json()["path"]
    with open(path, 'r') as file:
        text = file.read()
    h = Huffman(text)
    array = h.compress()
    filename, file_extension = os.path.splitext(path)
    output_path = filename + ".bin"
    with open(output_path, 'wb') as output:
        output.write(bytes(array))
    end = time.time()
    compression_time = end - start
    start = time.time()
    with open(output_path, 'rb') as file:
        array = bytearray(file.read())
    decompressed_text = h.decompress(array)
    end = time.time()
    decompression_time = end - start
    print("Original and decompressed are the same:", text == decompressed_text)
    write_xml(read_json()["xml"], compression_time, decompression_time, text == decompressed_text)


if __name__ == "__main__":
    main()
