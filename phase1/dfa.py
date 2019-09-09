
import re
'''
def accepts(transitions,initial,accepting,s):
    state = initial
    for c in s:
        if c in transitions[state]:
            state = transitions[state][c]
            print(c)
        else:
            if len(transitions[state])>0:
                if re.match("\d",c):
                    state = transitions[state]["digit"]
                    print("DIGIT")
                elif re.match("[^\d\s:]",c):
                    state = transitions[state]["char"]
                    print("CHAR")
                else:
                    print("BREAKSTATE")
            else:
                print("BREAKSTATE")

    return state in accepting

dfa = {0:{"\n": 0, " ":0, "\t": 0, "char":1, ".":2, "digit":3, "=":5, "(":6, ")":7,
	  ";":8, "+":9, "-":10,"*":11, "/":12, "^":13, "\"":14},
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
}

initial = 0
accepting = {1,3,4,5,6,7,8,9,10,11,12,13,15}
print(accepts(dfa,initial,accepting,'varible_1 '))

'''
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

dfa = {0:{"\n": 0, " ":0, "\t": 0, ".":2, "=":5, "(":6, ")":7,
	  ";":8, "+":9, "-":10,"*":11, "/":12, "^":13, "\"":14,"char":1, "digit":3},
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
}

state = 0
tokens = []
token = ''
accepting = {1,3,4,5,6,7,8,9,10,11,12,13,15}
for line in open('test/prog1.j',"r"):
    for char in line:
        token += char
        state = accepts(dfa,state,char)
        #print(token)
        #print(state)
        if state == "break_b":
            tokens.append(token[:-1])
            token = char
            state = 0
            state= accepts(dfa,state,char)
        if state == "break_a":
            tokens.append(token)
            token = ""
            state = 0
state = accepts(dfa,state,'')
if state == "break_b":
    tokens.append(token)

print(tokens)
for entry in tokens:
    print(f"> {entry}")