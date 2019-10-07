# parses file and builds tree
import re
from constants import dfa, term_tokens, follows
import token_classes as tc

variables = {}


def build_tree(tokens, tree):
    if not tree:
        tree = tc.Program()
        tree.left = tc.Stmt_list()
        tokens = build_tree(tokens, tree.left)
        print("End of build")
    elif tree.node == "stmt_list":
        if tokens[0].type != "$$":
            tree.left = tc.Stmt_single()
            tokens = build_tree(tokens, tree.left)
            tree.right = tc.Stmt_list()
            tokens = build_tree(tokens, tree.right)
        else:
            print("EOF")
            return tokens[1:]
    elif tree.node == "stmt" and tokens[0].type == "print":
        tree.child = tc.Print()
        tokens = tokens[1:]
        tokens = build_tree(tokens, tree.child.start)
        tokens = build_tree(tokens, tree.child.expr)
        tokens = build_tree(tokens, tree.child.stop)
        tokens = build_tree(tokens, tree.child.end)
        return tokens

    elif tree.node == "stmt" and (tokens[0].type == "Integer" or tokens[0].type == "Double" or
                                  tokens[0].type == "String"):
        tree.child = tc.Asmt()
        tree.child.type = tokens[0].type
        variables[tokens[1].value] = tokens[0].type
        tokens = tokens[1:]
        tokens = build_tree(tokens, tree.child.id)
        if tokens[0].type == "=":
            tokens = tokens[1:]
            if tree.child.type == "String":
                tree.child.expr = tc.S_expr()
                tokens = build_tree(tokens, tree.child.expr)
                tokens = tokens[1:]
            elif tree.child.type == "Integer":
                if tokens[1].type == "+" or tokens[1].type == "-" or tokens[1].type == "*" or tokens[1].type == "/" or\
                        tokens[1].type == "^":
                    if tokens[3].type == "+" or tokens[3].type == "-" or tokens[3].type == "*" or tokens[3].type == "/"\
                            or tokens[3].type == "^":
                        print("iexpr op iexpr")
                        tree.child.expr = tc.I_expr_triple()
                        tree.child.expr.left = tc.I_expr_triple()
                        tokens = build_tree(tokens, tree.child.expr.left)
                        tree.child.expr.op = tc.Op()
                        tokens = build_tree(tokens, tree.child.expr.op)
                        if tokens[1].value == ';':
                            tree.child.expr.right = tc.Int()
                            tokens = build_tree(tokens, tree.child.expr.right)
                        else:
                            tree.child.expr.right = tc.I_expr_triple()
                            tokens = build_tree(tokens, tree.child.expr.right)
                    else:
                        print("int op int")
                        tree.child.expr = tc.I_expr_triple()
                        tree.child.expr.left = tc.Int()
                        tokens = build_tree(tokens, tree.child.expr.left)
                        tree.child.expr.op = tc.Op()
                        tokens = build_tree(tokens, tree.child.expr.op)
                        tree.child.expr.right = tc.Int()
                        tokens = build_tree(tokens, tree.child.expr.right)
                    tokens = tokens[1:]

                else:
                    tree.child.expr = tc.I_expr_single()
                    tokens = build_tree(tokens, tree.child.expr)
                    tokens = build_tree(tokens, tree.child.end)

            elif tree.child.type == "Double":
                if tokens[1].type == "+" or tokens[1].type == "-" or tokens[1].type == "*" or tokens[1].type == "/" or \
                        tokens[1].type == "^":
                    if tokens[3].type == "+" or tokens[3].type == "-" or tokens[3].type == "*" or tokens[3].type == "/"\
                            or tokens[3].type == "^":
                        print("dexpr op dexpr")
                        tree.child.expr = tc.D_expr_triple()
                        tree.child.expr.left = tc.D_expr_triple()
                        tokens = build_tree(tokens, tree.child.expr.left)
                        tree.child.expr.op = tc.Op()
                        tokens = build_tree(tokens, tree.child.expr.op)
                        if tokens[1].value == ';':
                            tree.child.expr.right = tc.Dbl()
                            tokens = build_tree(tokens, tree.child.expr.right)
                        else:
                            tree.child.expr.right = tc.D_expr_triple()
                            tokens = build_tree(tokens, tree.child.expr.right)
                    else:
                        print("dbl op dbl")
                        tree.child.expr = tc.D_expr_triple()
                        tree.child.expr.left = tc.Dbl()
                        tokens = build_tree(tokens, tree.child.expr.left)
                        tree.child.expr.op = tc.Op()
                        tokens = build_tree(tokens, tree.child.expr.op)
                        tree.child.expr.right = tc.Dbl()
                        tokens = build_tree(tokens, tree.child.expr.right)
                    tokens = tokens[1:]
                else:
                    tree.child.expr = tc.D_expr_single()
                    tokens = build_tree(tokens, tree.child.expr)
                    tokens = build_tree(tokens, tree.child.end)

        return tokens

    elif tree.node == "id" and tokens[0].type == "ID":
        tree.child = tokens[0].value
        return tokens[1:]

    elif tree.node == "s_expr" and tokens[0].type == "ID":
        tree.child = tc.Id()
        tree.child.child = tokens[0].value
        tokens = tokens[1:]
        return tokens

    elif tree.node == "stmt" and tokens[0].type == "concat":
        tree.left = tc.Expr()
        tokens = build_tree(tokens, tree.left)
        tree.right = tc.End_stmt()
        tokens = build_tree(tokens, tree.right)
        return tokens

    elif tree.node == "expr" and tokens[0].type == 'concat':
        tree.expr = tc.S_Expr_Concat()
        tokens = tokens[1:]
        tokens = build_tree(tokens, tree.expr.start)
        tokens = build_tree(tokens, tree.expr.expr1)
        tokens = tokens[1:]
        tokens = build_tree(tokens, tree.expr.expr2)
        tokens = build_tree(tokens, tree.expr.stop)
        tokens = build_tree(tokens, tree.expr.end)
        return tokens

    elif tree.node == "stmt" and tokens[0].type == "ID":
        tree.left = tc.Expr()
        tokens = build_tree(tokens, tree.left)
        tree.right = tc.End_stmt()
        tokens = build_tree(tokens, tree.right)
        return tokens

    elif tree.node == "expr" and tokens[0].type == "ID":
        type = variables[tokens[0].value]  # Gets variable type for expression assignment
        if type == "Integer":
            if (tokens[1].type == "+" or tokens[1].type == "-" or tokens[1].type == "*" or tokens[1].type == "/" or
                    tokens[1].type == "^"):
                # Create integer expression
                tree.expr = tc.I_expr_triple()
                tree.expr = tc.I_expr_triple()
                tree.expr.left = tc.Id()
                tokens = build_tree(tokens, tree.expr.left)
                tree.expr.op = tc.Op()
                tokens = build_tree(tokens, tree.expr.op)

                if tokens[1].value == ';' or tokens[1].value == ')' or tokens[1].value == '(':
                    if tokens[0].type == "ID":
                        tree.expr.right = tc.Id()
                    else:
                        tree.expr.right = tc.Int()
                    tokens = build_tree(tokens, tree.expr.right)
                else:
                    tree.expr.right = tc.I_expr_triple()
                    tokens = build_tree(tokens, tree.expr.right)
            else:
                tree.expr = tc.I_expr_single()
                tokens = build_tree(tokens, tree.expr)

        elif type == "Double":
            # Create double expression
            if tokens[1].type == "+" or tokens[1].type == "-" or tokens[1].type == "*" or tokens[1].type == "/" or \
                    tokens[1].type == "^":
                tree.expr = tc.D_expr_triple()
                tree.expr = tc.D_expr_triple()
                tree.expr.left = tc.Id()
                tokens = build_tree(tokens, tree.expr.left)
                tree.expr.op = tc.Op()
                tokens = build_tree(tokens, tree.expr.op)
                if tokens[1].value == ';' or tokens[1].value == ')' or tokens[1].value == '(':
                    if tokens[0].type == "ID":
                        tree.expr.right = tc.Id()
                    else:
                        tree.expr.right = tc.Dbl()
                    tokens = build_tree(tokens, tree.expr.right)
                else:
                    tree.expr.right = tc.D_expr_triple()
                    tokens = build_tree(tokens, tree.expr.right)
            else:
                tree.expr = tc.D_expr_single()
                tokens = build_tree(tokens, tree.expr)

        elif type == "String":
        # Create string expression
            if tokens[1].type == ")":
                tree.expr = tc.Id()
                tokens = build_tree(tokens, tree.expr)
        else:
            print("We shouldn't be here")
        return tokens
     
    elif tree.node == "s_expr" and tokens[0].type == 'concat':
        tree.expr = tc.S_Expr_Concat()
        tokens = tokens[1:]
        tokens = build_tree(tokens, tree.expr.start)
        tokens = build_tree(tokens, tree.expr.expr1)
        tokens = tokens[1:]
        tokens = build_tree(tokens, tree.expr.expr2)
        tokens = build_tree(tokens, tree.expr.stop)
        tokens = build_tree(tokens, tree.expr.end)
        return tokens

    elif tree.node == "stmt" and tokens[0].type == "charAt":
        tree.left = tc.Expr()
        tokens = build_tree(tokens, tree.left)
        tree.right = tc.End_stmt()
        tokens = build_tree(tokens, tree.right)
        return tokens

    elif tree.node == "expr" and tokens[0].type == 'charAt':
        tree.expr = tc.S_Expr_CharAt()
        tokens = tokens[1:]
        tokens = build_tree(tokens, tree.expr.start)
        tokens = build_tree(tokens, tree.expr.expr1)
        tokens = tokens[1:]
        tokens = build_tree(tokens, tree.expr.expr2)
        tokens = build_tree(tokens, tree.expr.stop)
        tokens = build_tree(tokens, tree.expr.end)
        return tokens

    elif tree.node == "start_paren" and tokens[0].type == "(":
        return tokens[1:]

    elif tree.node == "end_paren" and tokens[0].type == ")":
        return tokens[1:]

    elif tree.node == "end_stmt" and tokens[0].type == ";":
        return tokens[1:]

    elif tree.node == "op" and (tokens[0].type == "+" or tokens[0].type == "-" or tokens[0].type == "*" or
                                tokens[0].type == "/" or tokens[0].type == "^"):
        tree.op = tokens[0].type
        return tokens[1:]

    elif tree.node == "expr" and tokens[0].type == "Str":
        tree.expr = tc.S_expr()
        tokens = build_tree(tokens, tree.expr)

    elif tree.node == "expr" and tokens[0].type == "ID":
        tree.expr = tc.Id()
        tree.expr.child = tokens[0].value
        return tokens[1:]

    elif tree.node == "i_expr" and tokens[0].type == "Number":
        if tokens[1].value == ";" or tokens[1].value == ")" or tokens[1].value == "(":
            tree.child = tc.Int()
            tokens = build_tree(tokens, tree.child)
        else:
            tree.left = tc.Int()
            tokens = build_tree(tokens, tree.left)
            tree.op = tc.Op()
            tokens = build_tree(tokens, tree.op)
            if (tokens[1].type == "+" or tokens[1].type == "-" or tokens[1].type == "*" or tokens[1].type == "/" or
                    tokens[1].type == "^"):
                tree.right = tc.I_expr_triple()
            else:
                tree.right = tc.Int()
            tokens = build_tree(tokens, tree.right)
        return tokens

    elif tree.node == "d_expr" and tokens[0].type == "Number":
        # tree.expr = tc.D_expr_triple()
        if tokens[1].value == ";" or tokens[1].value == ")" or tokens[1].value == "(":
            tree.child = tc.Dbl()
            tokens = build_tree(tokens, tree.child)
        else:
            tree.left = tc.Dbl()
            tokens = build_tree(tokens, tree.left)
            tree.op = tc.Op()
            tokens = build_tree(tokens, tree.op)
            if (tokens[1].type == "+" or tokens[1].type == "-" or tokens[1].type == "*" or tokens[1].type == "/" or
                    tokens[1].type == "^"):
                tree.right = tc.D_expr_triple()
            else:
                tree.right = tc.Dbl()
            tokens = build_tree(tokens, tree.right)
        return tokens

    elif tree.node == "expr" and tokens[0].type == "Number" and '.' not in tokens[0].value:
        if tokens[1].type == "+" or tokens[1].type == "-" or tokens[1].type == "*" or tokens[1].type == "/" or \
                tokens[1].type == "^":
            tree.expr = tc.I_expr_triple()
            tree.expr.left = tc.Int()
            tokens = build_tree(tokens, tree.expr.left)
            tree.expr.op = tc.Op()
            tokens = build_tree(tokens, tree.expr.op)
            if tokens[1].type == "+" or tokens[1].type == "-" or tokens[1].type == "*" or tokens[1].type == "/" or \
                    tokens[1].type == "^":
                tree.expr.right = tc.I_expr_triple()
            else:
                tree.expr.right = tc.Int()
            tokens = build_tree(tokens, tree.expr.right)
        else:
            tree.expr = tc.I_expr_single()
            tokens = build_tree(tokens, tree.expr)

    elif tree.node == "expr" and tokens[0].type == "Number" and '.' in tokens[0].value:
        if tokens[1].type == "+" or tokens[1].type == "-" or tokens[1].type == "*" or tokens[1].type == "/" or \
                tokens[1].type == "^":
            tree.expr = tc.D_expr_triple()
            tree.expr.left = tc.Dbl()
            tokens = build_tree(tokens, tree.expr.left)
            tree.expr.op = tc.Op()
            tokens = build_tree(tokens, tree.expr.op)
            if tokens[1].type == "+" or tokens[1].type == "-" or tokens[1].type == "*" or tokens[1].type == "/"\
                    or tokens[1].type == "^":
                tree.expr.right = tc.D_expr_triple()
            else:
                tree.expr.right = tc.Dbl()
            tokens = build_tree(tokens, tree.expr.right)

        else:
            tree.expr = tc.D_expr_single()
            tokens = build_tree(tokens, tree.expr)

    elif tree.node == 'int':
        if tokens[0].type == "-" or tokens[0].type == "+":
            tree.sign.child = tokens[0].value
            tokens = tokens[1:]
        tree.int = tokens[0].value
        return tokens[1:]

    elif tree.node == "i_expr":
        if tokens[0].type == "ID":
            tree.child = tc.Id()
            tree.child.child = tokens[0].value
        else:
            tree.child = tc.Int()
            if tokens[0].type == "-" or tokens[0].type == "+":
                tree.child.sign.child = tokens[0].value
                tokens = tokens[1:]
            tree.child.int = tokens[0].value
        return tokens[1:]

    elif tree.node == 'dbl':
        if tokens[0].type == "ID":
            tree.child = tc.Id()
            tree.child.child = tokens[0].value
        else:
            if tokens[0].type == "-" or tokens[0].type == "+":
                tree.sign.child = tokens[0].value
                tokens = tokens[1:]
            tree.dbl = tokens[0].value
        return tokens[1:]

    elif tree.node == "d_expr":
        tree.child = tc.Dbl()
        if tokens[0].type == "-" or tokens[0].type == "+":
            tree.child.sign.child = tokens[0].value
            tokens = tokens[1:]
        tree.child.dbl = tokens[0].value
        return tokens[1:]

    elif tree.node == "s_expr" and tokens[0].type == "Str":
        tree.child = tc.Str_literal()
        tree.child.child = tokens[0].value
        return tokens[1:]

    return tokens


def accepts(transitions, initial, s):
    state = initial
    if len(transitions[state]) == 0:
        return "break_b"

    if s in transitions[state]:
        state = transitions[state][s]

    else:
        if len(transitions[state]) > 0:
            if re.match("\d", s):
                state = transitions[state]["digit"]
            elif re.match("[A-Za-z]", s):
                state = transitions[state]["char"]
            else:
                state = "break_b"
        else:
            state = "break_a"

    return state


def parser(file_name):
    state = 0
    tokens = []
    token_i = tc.Token()
    line_num = 0
    line = ""
    for line in open(file_name, "r"):
        line_num += 1
        if len(line) >= 2 and line[0:2] == "//":  # ignore comments
            continue
        for char in line:
            if char != " " and char != "\n":
                token_i.value += char
            last_state = state
            state = accepts(dfa, state, char)
            if state == "break_b":
                if char != " " and char != "\n":
                    token_i.value = token_i.value[:-1]
                    token_i.line = [line_num, line]
                    if last_state == 14:
                        print(line)
                    if token_i.value == "Integer" or token_i.value == "Double" or token_i.value == "String" \
                            or token_i.value == "print"or token_i.value == "concat" or token_i.value == "charAt":
                        token_i.type = token_i.value
                    else:
                        token_i.type = term_tokens[last_state]
                    tokens.append(token_i)
                    token_i = tc.Token()
                    token_i.value = char
                else:
                    token_i.line = [line_num, line]
                    if token_i.value == "Integer" or token_i.value == "Double" or token_i.value == "String" \
                            or token_i.value == "print"or token_i.value == "concat" or token_i.value == "charAt":
                        token_i.type = token_i.value
                    else:
                        token_i.type = term_tokens[last_state]
                    tokens.append(token_i)
                    token_i = tc.Token()
                    token_i.value = ''
                state = 0
                last_state = state
                state = accepts(dfa, state, char)
            if state == "break_a":
                if token_i.value == "Integer" or token_i.value == "Double" or token_i.value == "String" \
                        or token_i.value == "print" or token_i.value == "concat" or token_i.value == "charAt":
                    token_i.type = token_i.value
                else:
                    token_i.type = term_tokens[last_state]
                token_i.line = [line_num, line]
                tokens.append(token_i)
                token_i = tc.Token()
                token_i.value = ""
                state = 0

    last_state = state
    state = accepts(dfa, state, 'EOF')
    if state == "break_b":
        token_i.line = [line_num, line]
        if token_i.value == "Integer" or token_i.value == "Double" or token_i.value == "String":
            token_i.type = token_i.value
        else:
            token_i.type = term_tokens[last_state]
        tokens.append(token_i)

    token_i = tc.Token()
    token_i.value = "$$"
    token_i.line = [line_num, line]
    token_i.type = "$$"
    tokens.append(token_i)
    return tokens


def token_check(tokens):
    past_token = None
    for token in tokens:
        if past_token:
            if not(token.type in follows[past_token]):
                print("INVALID LANGUAGE")
                print("LINE: " + str(token.line[0]))
                print(token.line[1])
                print(token.type)
                print(follows[past_token])
                return 0
        past_token = token.type
    return 1
