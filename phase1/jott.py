# main driver file for jott compiler

import sys
import parse_build as pb


def main():
    if len(sys.argv) != 2:
        print("Usage: python jott.py fileToTest.j")
        return

    tokens = pb.parser(sys.argv[1])
    if tokens:
        pb.build_tree(tokens, None)

        # print("GOOD LANGUAGE")
            # for thing in tokens:
            #    print(thing.type)


if __name__ == "__main__":
    main()
