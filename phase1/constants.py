# some constants used by parser

term_tokens = {
    1 : "ID", 3 : "Number", 4 : "Number", 5 : "=", 6 : "(", 7 : ")", 8 : ";", 9 : "+",
    10 : "-", 11 : "*", 12 : "/", 13 : "^", 15 : "Str", 16 : ","
}


dfa = {0:{"\n": 0, " ":0, "\t": 0, ".":2, "=":5, "(":6, ")":7,
	  ";": 8, "+":9, "-":10,"*":11, "/":12, "^":13, "\"":14,",":16,"char":1, "digit":3},
       1: {"char":1, "digit":1},
       2: {"digit":4},
	   3: {"digit":3, ".":4},
       4: {"digit":4},
       5: {},
	   6: {},
       7: {},
       8: {},
	   9: {},
       10: {},
	   11: {},
	   12: {},
       13: {},
       14: {"\"":15, "char": 14, "digit": 14, " ": 14},
	   15: {},
       16: {},
}

follows = {
    "Str": {')',';', ','},
    "Number": {'+', '-', '*', '/', '^', ')', ';'},
    ";": {"Integer", "Double", "String", "$$", "print", "concat", "charAt"},
    "Integer": {"ID"},
    "Double": {"ID"},
    "String": {"ID"},
    ")": {"+", "-", "*", "/", "^", ")", ",", ";"},
    "ID": {"+", "-", "*", "/", "^", "=", ")", ",", ";"},
    "print": {"("},
    "concat": {"("},
    ",": {"(", "ID", "Number", "Str", "concat", "charAt", "-"},
    "charAt": {"("},
    "=": {"(", "ID", "Number", "concat", "charAt", "-", "Str"},
    "(": {"(", "ID", "Number", "Str", "concat", "charAt", "-"},
    "^": {"(", "ID", "Number", "-"},
    "/": {"(", "ID", "Number", "-"},
    "*": {"(", "ID", "Number", "-"},
    "-": {"(", "ID", "Number", "-"},
    "+": {"(", "ID", "Number", "-"},
    "$$": {'E'}
}
