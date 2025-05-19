import heapq
import os
from collections import defaultdict, Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_tree(text):
    frequency = Counter(text)
    heap = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

def build_codes(root):
    codes = {}

    def generate_code(node, current_code):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = current_code
        generate_code(node.left, current_code + "0")
        generate_code(node.right, current_code + "1")

    generate_code(root, "")
    return codes

def compress(input_path, output_path):
    with open(input_path, 'r') as file:
        text = file.read()

    root = build_tree(text)
    codes = build_codes(root)

    encoded_text = ''.join(codes[char] for char in text)
    padded_text = encoded_text + '0' * ((8 - len(encoded_text) % 8) % 8)

    b = bytearray()
    for i in range(0, len(padded_text), 8):
        byte = padded_text[i:i+8]
        b.append(int(byte, 2))

    with open(output_path, 'wb') as out:
        out.write((str(codes) + '\n').encode())
        out.write(b)

def decompress(input_path, output_path):
    with open(input_path, 'rb') as file:
        lines = file.readlines()

    codes = eval(lines[0].decode())
    reversed_codes = {v: k for k, v in codes.items()}
    bit_string = ''.join(f'{byte:08b}' for byte in b''.join(lines[1:]))

    decoded_text = ''
    current_bits = ''
    for bit in bit_string:
        current_bits += bit
        if current_bits in reversed_codes:
            decoded_text += reversed_codes[current_bits]
            current_bits = ''

    with open(output_path, 'w') as out:
        out.write(decoded_text)
