
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

#class Stmt:
#    def __init__(self):
#        self.node = "stmt"
#        self.left = None
#        self.right = None

class Stmt_Print:
    def __init__(self):
        self.node = "stmt"
        self.child = None

class End_stmt:
    def __init__(self):
        self.node = "end_stmt"
        self.child = ";"

class Start_paren:
    def __init__(self):
        self.node = "start_paren"
        self.child = "("

class End_paren:
    def __init__(self):
        self.node = "end_paren"
        self.child = ")"

class Print:
    def __init__(self):
        self.node = "print"
        self.print = "print"
        self.start = Start_paren()
        self.expr = Expr()
        self.stop = End_paren()
        self.end = End_stmt()

class Expr:
    def __init__(self):
        self.node = "expr"
        #self.expr = [i_expr(),d_expr(),s_expr(),id()]
        self.expr = None

class S_expr_test:
    def __init__(self):
        self.node = "s_expr"
        self.child = None

class Str_literal:
    def __init__(self):
        self.node = "str_literal"
        self.child = None
'''

class char:
    def __init__(self):
        self.node = "char"
        # should be validated by parser beforehand

class l_char:
    def __init__(self):
        self.node = "l_char"
        # should be validated by parser beforehand

class r_char:
    def __init__(self):
        self.node = "r_char"
        # should be validated by parser beforehand

class digit:
    def __init__(self):
        self.node = "digit"
        # should be validated by parser beforehand

class space:
    def __init__(self):
        self.node = "space"
        # should be validated by parser beforehand

class sign:
    def __init__(self):
        self.node = "sign"
        self.child = ["-","+",None]

class id:
    def __init__(self):
        self.node = "id"
        self.left = l_char()
        self.right = [str(),None]


class asmt:
    def __init__(self):
        self.node = "asmt"
        self.type = ["Double","Integer","String"]
        self.id = id()
        self.equals = "="
        self.expression = [d_expr(),i_expr(),s_expr()]
        self.end = end_stmt()

class expr:
    def __init__(self):
        self.node = "expr"
        self.expr = [i_expr(),d_expr(),s_expr(),id()]

class i_expr:
    def __init__(self):
        self.node = "i_expr"

class i_expr_single(i_expr):
    def __init__(self):
        super().__init__(self)
        self.child = [id(),int()]

class i_expr_triple(i_expr):
    def __init__(self):
        super().__init__(self)
        self.left = [int(),i_expr()]
        self.op = [op()]
        self.right = [int(),i_expr()]

class d_expr:
    def __init__(self):
        self.node = "d_expr"

class d_expr_single(d_expr):
    def __init__(self):
        super().__init__(self)
        self.child = [id(),dbl()]

class d_expr_triple(d_expr):
    def __init__(self):
        super().__init__(self)
        self.left = [dbl(),d_expr()]
        self.op = [op()]
        self.right = [dbl(),d_expr()]

class s_expr:
    def __init__(self):
        self.node = "s_expr"

class op:
    def __init__(self):
        self.node = "op"
        self.op = ["+","-","*","/","^"]

class dbl:
    #WIP
    def __init__(self):
        self.node = "dbl"
        self.sign = sign()
        self.left = [digit(),None]
        self.point = "."
        self.right [digit()]

class int:
    #WIP
    def __init__(self):
        self.node = "int"
        self.sign = sign()
        self.int = digit()

class str:
    #WIP
    def __init__(self):
        self.node = "str"
        self.str = [char(),space(),str(),None]

class str_literal:
    #WIP
    def __init__(self):
        self.node = "str_literal"
'''
def build_tree(tokens,tree):
    if not tree:
        tree = Program()
        tree.left = Stmt_list()
        tokens = build_tree(tokens,tree.left)
        tree.right = "$$"
    elif tree.node == "stmt_list":
        if tokens[0].type != "$$":
            tree.left = Stmt_Print()
            tokens = build_tree(tokens,tree.left)
            tree.right = Stmt_list()
            tokens = build_tree(tokens,tree.right)
        else:
            print("EOF")
            return tokens[1:]
    elif tree.node == "stmt" and tokens[0].type == "print":
        tree.child = Print()
        tokens = tokens[1:]
        tokens = build_tree(tokens,tree.child.start)
        tokens = build_tree(tokens, tree.child.expr)
        tokens = build_tree(tokens, tree.child.stop)
        tokens = build_tree(tokens, tree.child.end)
    elif tree.node == "start_paren" and tokens[0].type == "(":
        return tokens[1:]

    elif tree.node == "end_paren" and tokens[0].type == ")":
        return tokens[1:]

    elif tree.node == "end_stmt" and tokens[0].type == ";":
        return tokens[1:]

    elif tree.node == "expr" and tokens[0].type == "Str":
        tree.expr = S_expr_test()
        tokens = build_tree(tokens,tree.expr)

    elif tree.node == "s_expr" and tokens[0].type == "Str":
        tree.child = Str_literal()
        tree.child.child = tokens[0].value
        return tokens[1:]

    return tokens


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

''' MOVED TO JOTT.PY
tokens = parser('test/prog_easy.j')

if(token_check(tokens)):
    print("GOOD LANGUAGE")
    for thing in tokens:
        print(thing.type)
    tokens = build_tree(tokens,None)
'''