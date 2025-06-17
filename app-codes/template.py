#!/usr/bin/env python
# coding: utf-8

# To run: python nameofprog.py --infile /tmp/in.file --outfile /tmp/out.file

# ensure no unused imports
import argparse

# Place any helper functions here, eg:
# def helper():
#    code

# The main function -- always name as main 
def main():

    # Command line arguments parser code goes first
    parser = argparse.ArgumentParser(description="Process command-line arguments.")
    parser.add_argument("--infile", help="Path to the input file.")
    parser.add_argument("--outfile", help="Path to the output file.")
    
    args = parser.parse_args()
    
    print(f"Input file: {args.infile}")
    print(f"Output file: {args.outfile}")

    # Code for the program core logic goes here
    # Make sure the code receives user
    # provided arguments and uses them
    # see the example provided as well.


# These following two lines will ensure 
# the code execution will start at main function
if __name__=="__main__":
    main()
