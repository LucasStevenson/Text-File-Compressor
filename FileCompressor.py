from collections import Counter # this is for creating the frequency table
import argparse
import sys

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

inputFile = args.input
extension = inputFile.split(".")[1]

if extension != "txt":
    print("Please only pass in a text file")
    sys.exit()

'''TODO
- make sure the filename they passed in exists in the cwd and try to read in the file 
- save the text into a string
- implement the actual algorithm 
'''
