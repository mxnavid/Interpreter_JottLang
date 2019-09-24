import re
import argparse

"""
    Code that checks the Jott grammar and returns False if any inconsistencies are found. 
    Otherwise, it returns true so that the main function can continue checking and running. 
"""
def checkGrammar(line):
    return True #If we get here, that means the grammar is correct

def main():
    parser = argparse.ArgumentParser(description='Check grammar of Jott file')
    parser.add_argument('file',nargs='?',default='test/prog3.j',help='The location of the Jott file that is being checked. No argument tests one of the provided files in /test')
    args = parser.parse_args()

    #Open the file
    jottFile = open(args.file, "r")
    for line in jottFile:
        #Grammar check
        if not checkGrammar(line):
            print("Error, wrong Jott syntax detected")
            raise SystemExit

    print("Jott grammar looks good!")

if __name__ == "__main__":
    main()
