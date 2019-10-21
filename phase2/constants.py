# some constants used by parser
import re


dfa = {0:{"\n": 0, " ":0, "\t": 0, ".":2, "=":5, "(":6, ")":7,
	  ";": 8, "+":9, "-":10,"*":11, "/":12, "^":13, "\"":14,",":22,"char":1, "digit":3},
       1: {"char":1, "digit":1},
       2: {"digit":4},
	   3: {"digit":3, ".":4},
       4: {"digit":4},
       5: {"=": 22},
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
       16: {"=": 19},
       17: {"=": 20},
       18: {"=": 21},
       20: {},
       21: {},
       22: {}
}






term_tokens = {
    1 : "ID", 3 : "Number", 4 : "Number", 5 : "=", 6 : "(", 7 : ")", 8 : ";", 9 : "+",
    10 : "-", 11 : "*", 12 : "/", 13 : "^", 15 : "Str", 16: "<", 17: ">", 18: "!", 19: "<=", 20: ">=", 21: "!=", 22: ","
}


dfa_old = {0:{"\n": 0, " ":0, "\t": 0, ".":2, "=":5, "(":6, ")":7,
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