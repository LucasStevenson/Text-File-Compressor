from collections import Counter # this is for creating the frequency table
import argparse
import sys, os
import heapq # for creating the priority queue
import pickle # for serializing the huffman code dict

'''How this program is going to work
User is going to run the program, with the only other arg being the text file they want to compress
example:
    python3 FileCompressor.py [--decompress|--compress] --input file.[txt|bin]

When compressing, the program is going to read in that text file, perform text compression using Huffman coding, and then write the result to a binary file
Output will be a message that everything went good, and the user should see a new file in their current working directory. The new file is the compressed file

When decompressing, the program is going to read in the huffman code table and data from the binary file and get the original text back
Output will be a message that everything went good, and the user shuold see a new file in their current working directory called 'decompressed.txt'
'''

# first, we need a node class to represent the nodes that will be in the huffman tree
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    def __lt__(self, other):
        # magic method that allows us to compare frequencies between nodes
        # this is important for implementing the priority queue
        return self.freq < other.freq
    def __str__(self):
        return repr(f"{self.char}: {self.freq}")

class Compressor:
    def __init__(self, text):
        self.text = text

    def __build_huffman_tree(self):
        freq_table = Counter(self.text) # the frequency table that maps each character to how often it appears in the text
        nodes = [ Node(char, freq) for char, freq in freq_table.items() ]
        heapq.heapify(nodes) # convert `nodes` to a min-heap
        while len(nodes) > 1:
            # keep popping off the first two elements, joining them, and inserting back into the heap 
            lNode = heapq.heappop(nodes)
            rNode = heapq.heappop(nodes)
            newNode = Node(None, lNode.freq+rNode.freq)
            newNode.left = lNode
            newNode.right = rNode
            heapq.heappush(nodes, newNode)
        return nodes[0]

    def __create_huffman_codes(self, node, s="", d={}):
        # returns a dictionary that maps each letter to its huffman code
        # going left on the huffman tree represents a 0 bit
        # going right on the huffman tree represents a 1 bit
        if node.char != None:
            d[node.char] = s
            return
        self.__create_huffman_codes(node.left, s+"0")
        self.__create_huffman_codes(node.right, s+"1")
        return d

    def compress(self):
        root = self.__build_huffman_tree() 
        codes = self.__create_huffman_codes(root)  
        # convert text to compressed binary data
        bits = "".join([ codes[c] for c in self.text ])
        # convert the "bits" string into bytes
        compressed_data = bytearray([int(bits[i:i+8], 2) for i in range(0, len(bits), 8)])
        with open("compressed.bin", "wb") as f:
            # in the compressed binary, we need to store the compressed data alongside the huffman codes dictionary
            # this is so that we can actually decompress the file
            pickle.dump(codes, f)
            f.write(compressed_data)
        print("Compression complete. Output written to 'compressed.bin'")


class Decompressor:
    def __init__(self, codes, compressed_data):
        self.codes = { v: k for k,v in codes.items() }
        self.compressed_data = compressed_data

    def decompress(self):
        # we want to pad every single byte except for the last one
        # if we pad the last byte, we might be adding extra bits, which will add an extra character at the end when decompressing
        bits = "".join([ bin(byte)[2:].zfill(8) if i != len(self.compressed_data)-1 else bin(byte)[2:] for i,byte in enumerate(self.compressed_data) ])
        binString = ""
        originalString = ""
        for bit in bits:
            binString += bit
            if binString in self.codes:
                originalString += self.codes[binString]
                binString = ""
        with open("decompressed.txt", "w") as f:
            f.write(originalString)
        print("Decompression complete. Output written to 'decompressed.txt'")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input text file to be compressed", required=True)
    parser.add_argument("-c", "--compress", help="compress file option", action="store_true")
    parser.add_argument("-d", "--decompress", help="decompress file option", action="store_true")
    args = parser.parse_args()

    filename = args.input
    # check that the file exists
    if not os.path.exists(filename):
        print(f"'{filename}' does not exist")
        sys.exit()
    # make sure that the user either specified whether to compress or decompress the input file
    if not (args.compress ^ args.decompress):
        print("Must specify whether you are compressing or decompressing this file using the '--compress' option or '--decompress' option (but not both)")
        sys.exit()

    if args.compress: # we are compressing a file
        # check that the file is a txt file
        if not filename.endswith(".txt"): 
            print("Please only pass in a text file and make sure the extension is '.txt'")
            sys.exit()
        # read the text in the file and save to a variable
        with open(filename) as f:
            text = f.read()
            assert len(text) > 0, "Please provide a text file with text in it"
        # compress the text
        Compressor(text).compress()
    elif args.decompress: # we are decompressing a file
        # check that the file is a bin file
        if not filename.endswith(".bin") or len(filename) < 5:
            print("Please only pass in a binary file and make sure that the extension is '.bin'")
            sys.exit()
        with open(filename, "rb") as f:
            huffman_codes = pickle.load(f)
            compressed_data = f.read()
            assert len(compressed_data) > 0, "Please provide a binary file with data in it"
        # decompress the data
        Decompressor(huffman_codes, compressed_data).decompress()

if __name__ == "__main__":
    main()
