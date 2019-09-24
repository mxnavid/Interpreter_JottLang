import re
import argparse



def checkGrammar(line):
    return True

def main():
    parser = argparse.ArgumentParser(description='Check grammar of Jott file')
    parser.add_argument('file',nargs='?',default='test/prog3.j',help='The location of the Jott file that is being checked. No argument tests one of the provided files in /test')
    args = parser.parse_args()

    #Open the file
    jottFile = open(args.file, "r")
    for line in jottFile:
        if not checkGrammar(line):
            print("Error, wrong Jott syntax detected")
            raise SystemExit

    print("Jott grammar looks good!")

if __name__ == "__main__":
    main()
