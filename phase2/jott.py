# main driver file for jott compiler

import sys

import parse_build as pb


def main():
    if len(sys.argv) != 2:
        print("Usage: python jott.py fileToTest.j")
        return

    tokens = pb.parser(sys.argv[1])
    #  tokens = pb.parser("test\secondPhase\instructor_samples\input\prog12.j")
    if tokens:
        #  for thing in tokens:
        #      print(thing.type)
        pb.build_tree(tokens, None)


if __name__ == "__main__":
    main()
