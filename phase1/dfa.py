
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

class Token:
    def __init__(self):
        self.type = ""
        self.value = ""
        self.line = []

class Program:
    def __init__(self):
        self.node = "program"
        self.left = Stmt_list()
        self.right = "$$"

class Stmt_list:
    def __init__(self):
        self.node = "stmt_list"
        self.left = None
        self.right = None

class Stmt:
    def __init__(self):
        self.node = "stmt"
        self.left = None
        self.right = None

class End_stmt:
    def __init__(self):
        self.node = "end_stmt"

class Start_paren:
    def __init__(self):
        self.node = "start_paren"
        self.child = "("

class End_paren:
    def __init__(self):
        self.node = "end_paren"
        self.child = ")"

class Char:
    def __init__(self):
        self.node = "char"
        # should be validated by parser beforehand

class L_char:
    def __init__(self):
        self.node = "l_char"
        # should be validated by parser beforehand

class R_char:
    def __init__(self):
        self.node = "r_char"
        # should be validated by parser beforehand

class Digit:
    def __init__(self):
        self.node = "digit"
        # should be validated by parser beforehand

class Space:
    def __init__(self):
        self.node = "space"
        # should be validated by parser beforehand

class Sign:
    def __init__(self):
        self.node = "sign"
        self.child = ["-","+",None]

class Id:
    def __init__(self):
        self.node = "id"
        self.left = L_char()
        self.right = [str(),None]

class Print:
    def __init__(self):
        self.node = "print"
        self.print = "print"
        self.start = Start_paren()
        self.expr = Expr()
        self.stop = End_paren()
        self.end = End_stmt()

class Asmt:
    def __init__(self):
        self.node = "asmt"
        self.type = ["Double","Integer","String"]
        self.id = id()
        self.equals = "="
        self.expression = [D_expr(), I_expr(), S_expr()]
        self.end = End_stmt()

class Expr:
    def __init__(self):
        self.node = "expr"
        self.expr = [I_expr(), D_expr(), S_expr(),id()]

class I_expr:
    def __init__(self):
        self.node = "i_expr"

class I_expr_single(I_expr):
    def __init__(self):
        super().__init__(self)
        self.child = [id(),int()]

class I_expr_triple(I_expr):
    def __init__(self):
        super().__init__(self)
        self.left = [int(), I_expr()]
        self.op = [Op()]
        self.right = [int(), I_expr()]

class D_expr:
    def __init__(self):
        self.node = "d_expr"

class D_expr_single(D_expr):
    def __init__(self):
        super().__init__(self)
        self.child = [id(), Dbl()]

class D_expr_triple(D_expr):
    def __init__(self):
        super().__init__(self)
        self.left = [Dbl(), D_expr()]
        self.op = [Op()]
        self.right = [Dbl(), D_expr()]

class S_expr:
    def __init__(self):
        self.node = "s_expr"

class Op:
    def __init__(self):
        self.node = "op"
        self.op = ["+","-","*","/","^"]

class Dbl:
    #WIP
    def __init__(self):
        self.node = "dbl"
        self.sign = Sign()
        self.left = [Digit(),None]
        self.point = "."
        # self.right [Digit()]

class Int:
    #WIP
    def __init__(self):
        self.node = "int"
        self.sign = Sign()
        self.int = Digit()

class Str:
    #WIP
    def __init__(self):
        self.node = "str"
        self.str = [Char(), Space(), str(), None]

class Str_literal:
    #WIP
    def __init__(self):
        self.node = "str_literal"

def build_tree(tokens,tree):
    if not tree:
        tree = Program()
        tree.left = Stmt_list()
        build_tree(tokens,tree.left)
        tree.right = "$$"
        print(Program)
    if tree.node == "stmt_list":
        if tokens[0].type != "$$":
            tree.left = Stmt()
            build_tree(Token,tree.left)
            tree.right = Stmt_list()
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
    token_i = Token()
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
                    token_i = Token()
                    token_i.value = char
                else:
                    token_i.line = [line_num,line]
                    if token_i.value == "Integer" or token_i.value == "Double" or token_i.value == "String" \
                            or token_i.value == "print"or token_i.value == "concat" or token_i.value == "charat":
                        token_i.type = token_i.value
                    else:
                        token_i.type = term_tokens[last_state]
                    tokens.append(token_i)
                    token_i = Token()
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
                token_i = Token()
                Token.value = ""
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

    token_i = Token()
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
