# parses file and builds tree

import re
from constants import dfa, term_tokens, follows
import token_classes as tc

def build_tree(tokens,tree):
    if not tree:
        tree = tc.Program()
        tree.left = tc.Stmt_list()
        tokens = build_tree(tokens,tree.left)
        print("End of build")
    elif tree.node == "stmt_list":
        if tokens[0].type != "$$":
            tree.left = tc.Stmt_single()
            tokens = build_tree(tokens,tree.left)
            tree.right = tc.Stmt_list()
            tokens = build_tree(tokens,tree.right)
        else:
            print("EOF")
            return tokens[1:]
    elif tree.node == "stmt" and tokens[0].type == "print":
        tree.child = tc.Print()
        tokens = tokens[1:]
        tokens = build_tree(tokens,tree.child.start)
        tokens = build_tree(tokens, tree.child.expr)
        tokens = build_tree(tokens, tree.child.stop)
        tokens = build_tree(tokens, tree.child.end)
        return tokens

    elif tree.node == "stmt" and (tokens[0].type == "Integer" or tokens[0].type == "Double" or tokens[0].type == "String"):
        tree.child = tc.Asmt()
        tree.child.type = tokens[0].type
        tokens = tokens[1:]
        tokens = build_tree(tokens,tree.child.id)
        if(tokens[0].type == "="):
            tokens = tokens[1:]
            tree.child.expr = tc.S_expr()
            tokens = build_tree(tokens, tree.child.expr)
            tokens = build_tree(tokens, tree.child.end)
        return tokens

    elif tree.node == "id" and tokens[0].type == "ID":
        tree.child = tokens[0].value
        return tokens[1:]
    elif tree.node == "start_paren" and tokens[0].type == "(":
        return tokens[1:]

    elif tree.node == "end_paren" and tokens[0].type == ")":
        return tokens[1:]

    elif tree.node == "end_stmt" and tokens[0].type == ";":
        return tokens[1:]

    elif tree.node == "expr" and tokens[0].type == "Str":
        tree.expr = tc.S_expr()
        tokens = build_tree(tokens,tree.expr)

    elif tree.node == "s_expr" and tokens[0].type == "Str":
        tree.child = tc.Str_literal()
        tree.child.child = tokens[0].value
        return tokens[1:]
    elif tree.node == "expr" and tokens[0].type == "ID":
        tree.expr = tc.Id()
        tree.expr.child = tokens[0].value
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
    token_i = tc.Token()
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
                    token_i = tc.Token()
                    token_i.value = char
                else:
                    token_i.line = [line_num,line]
                    if token_i.value == "Integer" or token_i.value == "Double" or token_i.value == "String" \
                            or token_i.value == "print"or token_i.value == "concat" or token_i.value == "charat":
                        token_i.type = token_i.value
                    else:
                        token_i.type = term_tokens[last_state]
                    tokens.append(token_i)
                    token_i = tc.Token()
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
                token_i = tc.Token()
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

    token_i = tc.Token()
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
