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

# now time to implement the actual algorithm
