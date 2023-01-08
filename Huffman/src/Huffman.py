import heapq
import json
import xml.etree.ElementTree as ElementTree


def read_json():
    """
    This method is used to read the json file
    :return: the json file
    """
    with open("./config/config.json", "r") as file:
        x = file.read()
        result = json.loads(x)
    return result


def write_xml(path, comp_time, decomp_time, isSuccessful):
    """
    This method is used to write the xml file
    :param path: the path of the xml file
    :param comp_time: the compression time
    :param decomp_time: the decompression time
    :param isSuccessful: if the decompression is successful
    :return:
    """
    root = ElementTree.Element("root")
    comp_time_element = ElementTree.SubElement(root, "CompressionTime")
    comp_time_element.text = str(comp_time)
    decomp_time_element = ElementTree.SubElement(root, "DecompressionTime")
    decomp_time_element.text = str(decomp_time)
    isSuccessful_element = ElementTree.SubElement(root, "isSuccessful")
    isSuccessful_element.text = str(isSuccessful)
    tree = ElementTree.ElementTree(root)
    tree.write(path)


class Node:
    """
    This class is used to create a node for the huffman tree

    Attributes:
        freq: frequency of the character
        char: character
        left: left child
        right: right child

    Methods:
        __lt__: used to compare two nodes
        __eq__: used to compare two nodes
        __repr__: used to print the node
    """
    def __init__(self, freq, char=None, left=None, right=None):
        """
        The constructor for Node class
        :param freq: frequency of the character
        :param char: character
        :param left: left child
        :param right: right child
        """
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other):
        """
        This method is used to compare two nodes
        :param other: other node
        :return: True if self is less than other, False otherwise
        """
        return self.freq < other.freq

    def __eq__(self, other):
        """
        This method is used to compare two nodes
        :param other: other node
        :return: True if self is equal to other, False otherwise
        """
        return self.freq == other.freq

    def __repr__(self):
        """
        This method is used to print the node
        :return: string representation of the node
        """
        return f"Node({self.freq}, {self.char}, {self.left}, {self.right})"


def remove_padding(padded_encoded_text):
    """
    This method is used to remove the padding from the encoded text
    :param padded_encoded_text: encoded text with padding
    :return: encoded text without padding
    """
    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)

    padded_encoded_text = padded_encoded_text[8:]
    encoded_text = padded_encoded_text[:-1*extra_padding]

    return encoded_text


class Huffman:
    """
    This class is used to perform huffman encoding and decoding

    Attributes:
        text: text to be encoded or decoded
        freq: frequency of each character in the text
        codes: codes for each character
        reverse_codes: reverse of codes
        heap: heap used to create the huffman tree
        root: root of the huffman tree
        encoded_text: encoded text
        decoded_text: decoded text

    Methods:
        make_freq_dict: used to make a dictionary of frequencies of each character
        make_heap: used to make a heap of nodes
        merge_nodes: used to merge nodes in the heap
        make_codes_helper: used to make codes for each character
        make_codes: used to make codes for each character
        get_encoded_text: used to get the encoded text
        pad_encoded_text: used to pad the encoded text
        get_byte_array: used to get the byte array of the encoded text
        compress: used to compress the text
        decompress: used to decompress the text
    """
    def __init__(self, text):
        """
        The constructor for Huffman class
        :param text: text to be encoded or decoded
        """
        self.text = text
        self.freq = {}
        self.codes = {}
        self.reverse_codes = {}
        self.heap = []
        self.root = None
        self.encoded_text = None
        self.decoded_text = None

    def make_freq_dict(self):
        """
        This method is used to make a dictionary of frequencies of each character
        :return:
        """
        for char in self.text:
            if char not in self.freq:
                self.freq[char] = 0
            self.freq[char] += 1

    def make_heap(self):
        """
        This method is used to make a heap of nodes
        :return:
        """
        for key in self.freq:
            node = Node(self.freq[key], key)
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        """
        This method is used to merge nodes in the heap
        :return:
        """
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merged_node = Node(node1.freq + node2.freq, left=node1, right=node2)
            heapq.heappush(self.heap, merged_node)
        self.root = heapq.heappop(self.heap)

    def make_codes_helper(self, root, current_code):
        """
        This method is used to make codes for each character
        :param root: root of the huffman tree
        :param current_code: current code
        :return:
        """
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_codes[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        """
        This method is used to make codes for each character
        :return:
        """
        current_code = ""
        self.make_codes_helper(self.root, current_code)

    def get_encoded_text(self):
        """
        This method is used to get the encoded text
        :return:
        """
        encoded_text = ""
        for char in self.text:
            encoded_text += self.codes[char]
        self.encoded_text = encoded_text

    def pad_encoded_text(self):
        """
        This method is used to pad the encoded text
        :return:
        """
        extra_padding = 8 - len(self.encoded_text) % 8
        for i in range(extra_padding):
            self.encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        self.encoded_text = padded_info + self.encoded_text

    def get_byte_array(self):
        """
        This method is used to get the byte array of the encoded text
        :return:
        """
        if len(self.encoded_text) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(self.encoded_text), 8):
            byte = self.encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b

    def compress(self):
        """
        This method is used to compress the text
        :return: compressed text
        """
        self.make_freq_dict()
        self.make_heap()
        self.merge_nodes()
        self.make_codes()
        self.get_encoded_text()
        self.pad_encoded_text()
        return self.get_byte_array()

    def decode_text(self, encoded_text):
        """
        This method is used to decode the encoded text
        :param encoded_text: encoded text
        :return: decoded text
        """
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_codes:
                character = self.reverse_codes[current_code]
                decoded_text += character
                current_code = ""

        self.decoded_text = decoded_text
        return decoded_text

    def decompress(self, array):
        """
        This method is used to decompress the text
        :param array: compressed text
        :return: decompressed text
        """
        encoded_text = ""

        for byte in array:
            encoded_text += "{0:08b}".format(byte)

        encoded_text = remove_padding(encoded_text)
        return self.decode_text(encoded_text)
