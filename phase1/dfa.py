import re

class token:
    def __init__(self):
        self.type = ""
        self.value = ""
        self.line = []


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

term_tokens = {
    1 : "id", 3 : "number", 4 : "number", 5 : "assign", 6 : "start_paren", 7 : "end_paren", 8 : "end_stmt", 9 : "plus",
    10 : "minus", 11 : "mult", 12 : "divide", 13 : "power", 15 : "string", 16 : "comma"
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

state = 0
tokens = []
token_i = token()
line_num = 0
for line in open('test/prog3.j',"r"):
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
                token_i.type = term_tokens[last_state]
                tokens.append(token_i)
                token_i = token()
                token_i.value = char
            else:
                token_i.line = [line_num,line]
                token_i.type = term_tokens[last_state]
                tokens.append(token_i)
                token_i = token()
                token_i.value = ''
            state = 0
            last_state = state
            state= accepts(dfa,state,char)
        if state == "break_a":
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
    token_i.type = term_tokens[last_state]
    tokens.append(token_i)

token_i = token()
token_i.value = "EOF"
token_i.line = [line_num,line]
token_i.type = "EOF"
tokens.append(token_i)
#print(tokens)
for entry in tokens:
    print(f"> {entry.value} - {entry.type} - {entry.line}")