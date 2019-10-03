# main driver file for jott compiler
import sys
import first_table as ft

def main():
    if len(sys.argv) != 2:
        print("Usage: python jott.py fileToTest.j")
        return

    tokens = ft.parser(sys.argv[1])

    if(ft.token_check(tokens)):
        print("GOOD LANGUAGE")
        for thing in tokens:
            print(thing.type)
        tokens = ft.build_tree(tokens,None)

if __name__ == "__main__":
    main()
