
import re


term_tokens = {
    1 : "ID", 3 : "Number", 4 : "Number", 5 : "=", 6 : "(", 7 : ")", 8 : ";", 9 : "+",
    10 : "-", 11 : "*", 12 : "/", 13 : "^", 15 : "Str", 16 : ","
}

dfa = {0:{"\n": 0, " ":0, "\t": 0, ".":2, "=":5, "(":6, ")":7,
	  ";":8, "+":9, "-":10,"*":11, "/":12, "^":13, "\"":14,",":16,"char":1, "digit":3},
       1:{"char":1, "digit":1},
       2:{"digit":4},
	   3:{"digit":3, ".":4},
       4:{"digit":4},
       5:{},
	   6:{},
       7:{},
       8:{},
	   9:{},
       10:{},
	   11:{},
	   12:{},
       13:{},
       14:{"\"":15, "char":14, "digit":14, " ":14},
	   15:{},
       16:{},
}

follows = {
    "Str":{')',';',','},
    "Number":{'+','-','*','/','^',')',';'},
    ";":{"Integer","Double","String","$$","print","concat", "charAt"},
    "Integer":{"ID"},
    "Double":{"ID"},
    "String":{"ID"},
    ")":{"+","-","*","/","^",")",",",";"},
    "ID":{"+","-","*","/","^","=",")",",",";"},
    "print":{"("},
    "concat":{"("},
    "charAt":{"("},
    "=":{"(","ID","Number", "concat", "charAt","-"},
    "(":{"(","ID","Number","Str","concat","charAt","-"},
    "^":{"(","ID","Number","-"},
    "/":{"(","ID","Number","-"},
    "*":{"(","ID","Number","-"},
    "-":{"(","ID","Number","-"},
    "+":{"(","ID","Number","-"},
    "$$":{'E'}
}

class token:
    def __init__(self):
        self.type = ""
        self.value = ""
        self.line = []

class program:
    def __init__(self):
        self.node = "program"
        self.left = stmt_list()
        self.right = "$$"

class stmt_list:
    def __init__(self):
        self.node = "stmt_list"
        self.left = None
        self.right = None

class stmt:
    def __init__(self):
        self.node = "stmt"
        self.left = None
        self.right = None

def build_tree(tokens,tree):
    if not tree:
        tree = program()
        tree.left = stmt_list()
        build_tree(tokens,tree.left)
        tree.right = "$$"
        print(program)
    if tree.node == "stmt_list":
        if tokens[0].type != "$$":
            tree.left = stmt()
            build_tree(token,tree.left)
            tree.right = stmt_list()
            #build_tree(token,tree.right)
        else:
            tree.node = "EMPTY"




def accepts(transitions,initial,s):
    state = initial
    if len(transitions[state])==0:
         return "break_b"

    if s in transitions[state]:
        state = transitions[state][s]

    else:
        if len(transitions[state])>0:
            if re.match("\d",s):
                state = transitions[state]["digit"]
            elif re.match("[A-Za-z]",s):
                state = transitions[state]["char"]
            else:
                state = "break_b"
        else:
            state = "break_a"

    return state

def parser(fileName):

    state = 0
    tokens = []
    token_i = token()
    line_num = 0
    line = ""
    for line in open(fileName,"r"):
        line_num += 1
        for char in line:
            if char != " " and char != "\n":
                token_i.value += char
            last_state = state
            state = accepts(dfa,state,char)
            if state == "break_b":
                if char != " " and char != "\n":
                    token_i.value = token_i.value[:-1]
                    token_i.line = [line_num,line]
                    if(last_state == 14):
                        print(line)
                        print("vlaa")
                    if token_i.value == "Integer" or token_i.value == "Double" or token_i.value == "String" \
                            or token_i.value == "print"or token_i.value == "concat" or token_i.value == "charat":
                        token_i.type = token_i.value
                    else:
                        token_i.type = term_tokens[last_state]
                    tokens.append(token_i)
                    token_i = token()
                    token_i.value = char
                else:
                    token_i.line = [line_num,line]
                    if token_i.value == "Integer" or token_i.value == "Double" or token_i.value == "String" \
                            or token_i.value == "print"or token_i.value == "concat" or token_i.value == "charat":
                        token_i.type = token_i.value
                    else:
                        token_i.type = term_tokens[last_state]
                    tokens.append(token_i)
                    token_i = token()
                    token_i.value = ''
                state = 0
                last_state = state
                state= accepts(dfa,state,char)
            if state == "break_a":
                if token_i.value == "Integer" or token_i.value == "Double" or token_i.value == "String" \
                        or token_i.value == "print" or token_i.value == "concat" or token_i.value == "charat":
                    token_i.type = token_i.value
                else:
                    token_i.type = term_tokens[last_state]
                token_i.line = [line_num,line]
                tokens.append(token_i)
                token_i = token()
                token.value = ""
                state = 0
                last_state = state

    last_state = state
    state = accepts(dfa,state,'EOF')
    if state == "break_b":
        token_i.line = [line_num,line]
        if token_i.value == "Integer" or token_i.value == "Double" or token_i.value == "String":
            token_i.type = token_i.value
        else:
            token_i.type = term_tokens[last_state]
        tokens.append(token_i)

    token_i = token()
    token_i.value = "$$"
    token_i.line = [line_num,line]
    token_i.type = "$$"
    tokens.append(token_i)
    return tokens

def token_check(tokens):
    past_token = None
    for token in tokens:
        if(past_token):
            if not(token.type in follows[past_token]):
                print("INVALID LANGUAGE")
                print(f"LINE: {token.line[0]}")
                print(token.line[1])
                print(token.type)
                print(follows[past_token])
                return 0
        past_token = token.type
    return 1

tokens = parser('test/prog_easy.j')
if(token_check(tokens)):
    print("GOOD LANGUAGE")
    for thing in tokens:
        print(thing.type)
    build_tree(tokens,None)
