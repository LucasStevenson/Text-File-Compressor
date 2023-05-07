from collections import Counter # this is for creating the frequency table
import argparse
import sys, os
import heapq # for creating the priority queue

'''How this program is going to work
User is going to run the program, with the only other arg being the text file they want to compress
example:
    python3 FileCompressor.py --input words.txt

The program is going to read in that text file, perform text compression using Huffman coding, and then write the result to a binary file
Output will be a message that everything went good, and the user should see a new file in their current working directory. The new file is the compressed file
'''

# even though we are only using one arg, argparser makes sure the user uses it right and also prints out a usage message so that we don't have to, which is nice
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input text file to be compressed", required=True)
args = parser.parse_args()

filename = args.input
# check that the file exists
if not os.path.exists(filename):
    print(f"'{filename}' does not exist")
    sys.exit()
# check that the file is a txt file
if not filename.endswith(".txt"): 
    print("Please only pass in a text file and make sure the extension is '.txt'")
    sys.exit()

# read the text in the file and save to a variable
with open(filename) as f:
    text = f.read()
    assert len(text) > 0, "Please provide a text file with text in it"

# now time to implement the actual algorithm
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


# haven't ran tests on the method below yet. Only implemented it according to the rules of the algorithm so far
# TODO: make sure this code actually works like how its supposed to.
def build_huffman_tree(text):
    freq_table = Counter(text) # the frequency table that maps each character to how often it appears in the text
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

def create_huffman_codes(node, s="", d={}):
    # returns a dictionary that maps each letter to its huffman code
    # going left on the huffman tree represents a 0 bit
    # going right on the huffman tree represents a 1 bit
    if node.char != None:
        d[node.char] = s
        return
    create_huffman_codes(node.left, s+"0")
    create_huffman_codes(node.right, s+"1")
    return d

root = build_huffman_tree(text)
codes = create_huffman_codes(root)
print(codes)
