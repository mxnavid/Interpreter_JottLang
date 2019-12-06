# parses file and builds tree
import re
import sys
from constants import dfa, term_tokens, math_operators, comp_operators
import token_classes as tc
from code_gen import gen_code, verify_code
variables = {}
token_copy = {}


def build_tree(tokens, tree):
    if not tree:
        tree = tc.Program()
        tree.left = tc.Stmt_list()
        tokens = build_tree(tokens, tree.left)
        if verify_code(tree, token_copy):
            gen_code(tree)
    elif tree.node == "stmt_list":
        if tokens[0].type != "$$":
            if tokens[0].type == 'concat' or tokens[0].type == 'charAt':
                tree.left = tc.Stmt()
                tokens = build_tree(tokens, tree.left)
            elif tokens[0].value == "}":
                return tokens
            else:
                tree.left = tc.Stmt_single()
                tokens = build_tree(tokens, tree.left)

            tree.right = tc.Stmt_list()
            tokens = build_tree(tokens, tree.right)
        else:
            return tokens[1:]
    elif tree.node == "func_stmt":
            if tokens[0].type == 'concat' or tokens[0].type == 'charAt':
                tree.left = tc.Stmt()
                tokens = build_tree(tokens, tree.left)
            elif tokens[0].value == "}":
                return tokens
            else:
                tree.left = tc.Stmt_single()
                tokens = build_tree(tokens, tree.left)

            tree.right = tc.func_stmt()
            tokens = build_tree(tokens, tree.right)

    elif tree.node == "stmt" and tokens[0].type == "print":
        tree.child = tc.Print()
        tokens = tokens[1:]
        tokens = build_tree(tokens, tree.child.start)
        tokens = build_tree(tokens, tree.child.expr)
        tokens = build_tree(tokens, tree.child.stop)
        tokens = build_tree(tokens, tree.child.end)
        return tokens
    elif tree.node == "stmt" and tokens[0].type == "ID" and tokens[0].value == "if":
        tree.child = tc.If_expr()
        tokens = tokens[1:]
        tokens = build_tree(tokens, tree.child.startparen)
        tokens = build_tree(tokens, tree.child.comp)
        tokens = build_tree(tokens, tree.child.stopparen)
        tokens = build_tree(tokens, tree.child.startblk)
        tokens = build_tree(tokens, tree.child.stmtlist)
        tokens = build_tree(tokens, tree.child.stopblk)

        if tokens[0].value == "else":
            tokens = tokens[1:]               # so I pop of else term
            tree.child.elseblk = tc.Start_blk()
            tokens = build_tree(tokens, tree.child.elseblk)
            tree.child.elsestmt = tc.Stmt_list()
            tokens = build_tree(tokens, tree.child.elsestmt)
            tree.child.elseblkend = tc.End_blk()
            tokens = build_tree(tokens, tree.child.elseblkend)
        return tokens

    elif tree.node == "stmt" and tokens[0].type == "ID" and tokens[1].value == "(" \
            and tokens[0].value != "while" and tokens[0].value != "for":
        tree.child = tc.F_Call()
        tokens = build_tree(tokens, tree.child.f_id)
        tokens = build_tree(tokens, tree.child.startParen)
        tokens = build_tree(tokens, tree.child.fc_p_list)
        tokens = build_tree(tokens, tree.child.endParen)
        tokens = build_tree(tokens, tree.child.end)

        return tokens
    elif tree.node == "stmt" and (tokens[0].type == "String" or tokens[0].type == "Integer" or tokens[0].type == "Void") and tokens[2].value == "(":
        tree.child = tc.Func()
        tokens = tokens[1:]
        tokens = build_tree(tokens, tree.child.f_id)
        tokens = build_tree(tokens, tree.child.startParen)
        tokens = build_tree(tokens, tree.child.p_list)
        tokens = build_tree(tokens, tree.child.endParen)
        tokens = build_tree(tokens, tree.child.startblk)
        tokens = build_tree(tokens, tree.child.func_stmt)
        tokens = build_tree(tokens, tree.child.endblk)
        return tokens

    elif tree.node == "stmt" and tokens[0].type == "ID" and tokens[0].value == "else":
        print("ERROR: There is no corresponding if with this else statement")
        sys.exit()

    elif tree.node == "stmt" and tokens[0].type == "ID" and tokens[0].value == "while":
        tree.child = tc.While_loop()
        tokens = tokens[1:]
        tokens = build_tree(tokens, tree.child.startparen)
        tokens = build_tree(tokens, tree.child.comp)
        tokens = build_tree(tokens, tree.child.endparen)
        tokens = build_tree(tokens, tree.child.startblk)
        tokens = build_tree(tokens, tree.child.stmtlist)
        tokens = build_tree(tokens, tree.child.endblk)
        return tokens

    elif tree.node == "stmt" and tokens[0].type == "ID" and tokens[0].value == "for":
        tree.child = tc.For_loop()
        tokens = tokens[1:]
        tokens = build_tree(tokens, tree.child.startparen)
        tokens = build_tree(tokens, tree.child.asmt)
        tokens = build_tree(tokens, tree.child.iexpr)
        tokens = build_tree(tokens, tree.child.endIexpr)
        tokens = build_tree(tokens, tree.child.reasmt)
        tokens = build_tree(tokens, tree.child.startblk)
        tokens = build_tree(tokens, tree.child.stmtlist)
        tokens = build_tree(tokens, tree.child.endblk)
        return tokens

    elif tree.node == "stmt" and (tokens[0].type == "Integer" or tokens[0].type == "Double" or
                                          tokens[0].type == "String" or tokens[0].value in variables):
        tree.child = tc.Asmt()
        if tokens[0].value not in variables:
            tree.child.type = tokens[0].type
            variables[tokens[1].value] = tokens[0].type
            tokens = tokens[1:]
        else:
            tree.child.type = variables[tokens[0].value]
        tokens = build_tree(tokens, tree.child.id)
        if tokens[0].type == "=":
            tokens = tokens[1:]
            if tree.child.type == "String":
                if tokens[0].type == "Number":
                    if '.' in tokens[0].value:
                        print("Syntax Error: Invalid type in re-assignment: Expected String got Float, \"" +
                              tokens[0].line[
                                  1].replace('\n', '"') + " Line: " + str(tokens[0].line[0]))
                    else:
                        print("Syntax Error: Invalid type in re-assignment: Expected String got Integer, \"" +
                              tokens[0].line[
                                  1].replace('\n', '"') + " Line: " + str(tokens[0].line[0]))
                    sys.exit()
                tree.child.expr = tc.S_expr()
                tokens = build_tree(tokens, tree.child.expr)
                tokens = tokens[1:]
            elif tree.child.type == "Integer":
                if tokens[0].type == "Str":
                    if tokens[1].type in comp_operators:
                        tree.child.expr = tc.I_expr_triple_comp()
                        tree.child.expr.left = tc.Str()
                        tokens = build_tree(tokens, tree.child.expr.left)
                        tree.child.expr.op = tc.Op()
                        tokens = build_tree(tokens, tree.child.expr.op)
                        tree.child.expr.right = tc.Str()
                        tokens = build_tree(tokens, tree.child.expr.right)
                        tokens = tokens[1:]
                    else:
                        if tokens[1].type == ';':
                            print("Syntax Error: Invalid type in re-assignment: Expected Integer got String, \"" + tokens[0].line[
                                1].replace('\n','"') + " Line: " + str(tokens[0].line[0]))
                        else:
                            print("Syntax Error: Expected , got " + str(tokens[0].value) + ", \"" + tokens[0].line[
                                1] + "\" Line: " + str(tokens[0].line[0]))
                        sys.exit()
                elif tokens[0].type == "Number" and '.' in tokens[0].value:
                    if tokens[1].type in comp_operators:
                        tree.child.expr = tc.I_expr_triple_comp()
                        tree.child.expr.left = tc.Dbl()
                        tokens = build_tree(tokens, tree.child.expr.left)
                        tree.child.expr.op = tc.Op()
                        tokens = build_tree(tokens, tree.child.expr.op)
                        tree.child.expr.right = tc.Dbl()
                        tokens = build_tree(tokens, tree.child.expr.right)
                        tokens = tokens[1:]
                    else:
                        if tokens[1].type == ';':
                            print("Syntax Error: Invalid type in re-assignment: Expected Integer got Float, \"" + tokens[0].line[
                                1].replace('\n','"') + " Line: " + str(tokens[0].line[0]))
                        else:
                            print("Syntax Error: Expected , got " + str(tokens[0].value) + ", \"" + tokens[0].line[
                                1] + "\" Line: " + str(tokens[0].line[0]))
                        sys.exit()
                else:
                    if tokens[1].type in math_operators:
                        if tokens[3].type in math_operators:
                            tree.child.expr = tc.I_expr_triple()
                            last = next(i for i, v in enumerate(tokens) if (v.type == ")" or v.type == ";")) - 1
                            tree.child.expr.right = tc.Int()
                            tree.child.expr.right.int = tokens.pop(last).value
                            tree.child.expr.op = tc.Op()
                            tree.child.expr.op.op = tokens.pop(last - 1).value
                            if tokens[1].type in math_operators:
                                tree.child.expr.left = tc.I_expr_triple()
                            else:
                                tree.child.expr.left = tc.Int()
                            tokens = build_tree(tokens, tree.child.expr.left)
                        else:
                            tree.child.expr = tc.I_expr_triple()
                            if(tokens[0].value in variables):
                                tree.child.expr.left = tc.Id()
                            else:
                                tree.child.expr.left = tc.Int()
                            tokens = build_tree(tokens, tree.child.expr.left)
                            tree.child.expr.op = tc.Op()
                            tokens = build_tree(tokens, tree.child.expr.op)
                            tree.child.expr.right = tc.Int()
                            tokens = build_tree(tokens, tree.child.expr.right)
                        tokens = tokens[1:]
                    elif tokens[1].type in comp_operators:
                        tree.child.expr = tc.I_expr_triple_comp()
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
                if tokens[1].type in math_operators:
                    if tokens[3].type in math_operators:
                        tree.child.expr = tc.D_expr_triple()
                        last = next(i for i, v in enumerate(tokens) if (v.type == ")" or v.type == ";")) - 1
                        tree.child.expr.right = tc.Dbl()
                        tree.child.expr.right.dbl = tokens.pop(last).value
                        tree.child.expr.op = tc.Op()
                        tree.child.expr.op.op = tokens.pop(last - 1).value
                        if tokens[1].type in math_operators:
                            tree.child.expr.left = tc.D_expr_triple()
                        else:
                            tree.child.expr.left = tc.Dbl()
                        tokens = build_tree(tokens, tree.child.expr.left)
                    else:
                        tree.child.expr = tc.D_expr_triple()
                        tree.child.expr.left = tc.Dbl()
                        tokens = build_tree(tokens, tree.child.expr.left)
                        tree.child.expr.op = tc.Op()
                        tokens = build_tree(tokens, tree.child.expr.op)
                        tree.child.expr.right = tc.Dbl()
                        tokens = build_tree(tokens, tree.child.expr.right)
                    tokens = tokens[1:]
                else:
                    if '.' in tokens[0].value:
                        tree.child.expr = tc.D_expr_single()
                        tokens = build_tree(tokens, tree.child.expr)
                        tokens = build_tree(tokens, tree.child.end)
                    else:
                        try:
                            int(tokens[0].value)
                            print("Syntax Error: Invalid type in re-assignment: Expected Float got Integer, \"" + tokens[0].line[
                                1].replace('\n','"') + " Line: " + str(tokens[0].line[0]))

                        except ValueError:
                            print("Syntax Error: Invalid type in re-assignment: Expected Float got String, \"" + tokens[0].line[
                                1].replace('\n','"') + " Line: " + str(tokens[0].line[0]))
                        sys.exit()

        return tokens
    elif tree.node == "asmt" and (tokens[0].type == "Integer" or tokens[0].type == "Double" or
                                          tokens[0].type == "String" or tokens[0].value in variables):
        if tokens[0].value not in variables:
            tree.type = tokens[0].type
            variables[tokens[1].value] = tokens[0].type
            tokens = tokens[1:]
        else:
            tree.type = variables[tokens[0].value]
        tokens = build_tree(tokens, tree.id)
        if tokens[0].type == "=":
            tokens = tokens[1:]
            if tree.type == "String":
                if tokens[0].type == "Number":
                    if '.' in tokens[0].value:
                        print("Syntax Error: Invalid type in re-assignment: Expected String got Float, \"" +
                              tokens[0].line[
                                  1].replace('\n', '"') + " Line: " + str(tokens[0].line[0]))
                    else:
                        print("Syntax Error: Invalid type in re-assignment: Expected String got Integer, \"" +
                              tokens[0].line[
                                  1].replace('\n', '"') + " Line: " + str(tokens[0].line[0]))
                    sys.exit()
                tree.expr = tc.S_expr()
                tokens = build_tree(tokens, tree.expr)
                tokens = tokens[1:]
            elif tree.type == "Integer":
                if tokens[0].type == "Str":
                    if tokens[1].type in comp_operators:
                        tree.expr = tc.I_expr_triple_comp()
                        tree.expr.left = tc.Str()
                        tokens = build_tree(tokens, tree.expr.left)
                        tree.expr.op = tc.Op()
                        tokens = build_tree(tokens, tree.expr.op)
                        tree.expr.right = tc.Str()
                        tokens = build_tree(tokens, tree.expr.right)
                        tokens = tokens[1:]
                    else:
                        if tokens[1].type == ';':
                            print("Syntax Error: Invalid type in re-assignment: Expected Integer got String, \"" + tokens[0].line[
                                1].replace('\n','"') + " Line: " + str(tokens[0].line[0]))
                        else:
                            print("Syntax Error: Expected , got " + str(tokens[0].value) + ", \"" + tokens[0].line[
                                1] + "\" Line: " + str(tokens[0].line[0]))
                        sys.exit()
                elif tokens[0].type == "Number" and '.' in tokens[0].value:
                    if tokens[1].type in comp_operators:
                        tree.expr = tc.I_expr_triple_comp()
                        tree.expr.left = tc.Dbl()
                        tokens = build_tree(tokens, tree.expr.left)
                        tree.expr.op = tc.Op()
                        tokens = build_tree(tokens, tree.expr.op)
                        tree.expr.right = tc.Dbl()
                        tokens = build_tree(tokens, tree.expr.right)
                        tokens = tokens[1:]
                    else:
                        if tokens[1].type == ';':
                            print("Syntax Error: Invalid type in re-assignment: Expected Integer got Float, \"" + tokens[0].line[
                                1].replace('\n','"') + " Line: " + str(tokens[0].line[0]))
                        else:
                            print("Syntax Error: Expected , got " + str(tokens[0].value) + ", \"" + tokens[0].line[
                                1] + "\" Line: " + str(tokens[0].line[0]))
                        sys.exit()
                else:
                    if tokens[1].type in math_operators:
                        if tokens[3].type in math_operators:
                            tree.expr = tc.I_expr_triple()
                            last = next(i for i, v in enumerate(tokens) if (v.type == ")" or v.type == ";")) - 1
                            tree.expr.right = tc.Int()
                            tree.expr.right.int = tokens.pop(last).value
                            tree.expr.op = tc.Op()
                            tree.expr.op.op = tokens.pop(last - 1).value
                            if tokens[1].type in math_operators:
                                tree.expr.left = tc.I_expr_triple()
                            else:
                                tree.expr.left = tc.Int()
                            tokens = build_tree(tokens, tree.expr.left)
                        else:
                            tree.expr = tc.I_expr_triple()
                            if(tokens[0].value in variables):
                                tree.expr.left = tc.Id()
                            else:
                                tree.expr.left = tc.Int()
                            tokens = build_tree(tokens, tree.expr.left)
                            tree.expr.op = tc.Op()
                            tokens = build_tree(tokens, tree.expr.op)
                            tree.expr.right = tc.Int()
                            tokens = build_tree(tokens, tree.expr.right)
                        tokens = tokens[1:]
                    elif tokens[1].type in comp_operators:
                        tree.expr = tc.I_expr_triple_comp()
                        tree.expr.left = tc.Int()
                        tokens = build_tree(tokens, tree.expr.left)
                        tree.expr.op = tc.Op()
                        tokens = build_tree(tokens, tree.expr.op)
                        tree.expr.right = tc.Int()
                        tokens = build_tree(tokens, tree.expr.right)
                        tokens = tokens[1:]
                    else:
                        tree.expr = tc.I_expr_single()
                        tokens = build_tree(tokens, tree.expr)
                        tokens = build_tree(tokens, tree.end)

            elif tree.type == "Double":
                if tokens[1].type in math_operators:
                    if tokens[3].type in math_operators:
                        tree.expr = tc.D_expr_triple()
                        last = next(i for i, v in enumerate(tokens) if (v.type == ")" or v.type == ";")) - 1
                        tree.expr.right = tc.Dbl()
                        tree.expr.right.dbl = tokens.pop(last).value
                        tree.expr.op = tc.Op()
                        tree.expr.op.op = tokens.pop(last - 1).value
                        if tokens[1].type in math_operators:
                            tree.expr.left = tc.D_expr_triple()
                        else:
                            tree.expr.left = tc.Dbl()
                        tokens = build_tree(tokens, tree.expr.left)
                    else:
                        tree.expr = tc.D_expr_triple()
                        tree.expr.left = tc.Dbl()
                        tokens = build_tree(tokens, tree.expr.left)
                        tree.expr.op = tc.Op()
                        tokens = build_tree(tokens, tree.expr.op)
                        tree.expr.right = tc.Dbl()
                        tokens = build_tree(tokens, tree.expr.right)
                    tokens = tokens[1:]
                else:
                    if '.' in tokens[0].value:
                        tree.expr = tc.D_expr_single()
                        tokens = build_tree(tokens, tree.expr)
                        tokens = build_tree(tokens, tree.end)
                    else:
                        try:
                            int(tokens[0].value)
                            print("Syntax Error: Invalid type in re-assignment: Expected Float got Integer, \"" + tokens[0].line[
                                1].replace('\n','"') + " Line: " + str(tokens[0].line[0]))

                        except ValueError:
                            print("Syntax Error: Invalid type in re-assignment: Expected Float got String, \"" + tokens[0].line[
                                1].replace('\n','"') + " Line: " + str(tokens[0].line[0]))
                        sys.exit()

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

    elif tree.node == "expr" and (tokens[0].type == "Number" or
                                  tokens[0].type == "Str") and tokens[1].type in comp_operators:
        tree.expr = tc.I_expr_triple_comp()
        if tokens[0].type == "Number" and '.' not in tokens[0].value:
            tree.expr.left = tc.Int()
            tokens = build_tree(tokens, tree.expr.left)
            tree.expr.op = tc.Op()
            tokens = build_tree(tokens, tree.expr.op)
            tree.expr.right = tc.Int()
            tokens = build_tree(tokens, tree.expr.right)
        elif tokens[0].type == "Number" and '.' in tokens[0].value:
            tree.expr.left = tc.Dbl()
            tokens = build_tree(tokens, tree.expr.left)
            tree.expr.op = tc.Op()
            tokens = build_tree(tokens, tree.expr.op)
            tree.expr.right = tc.Dbl()
            tokens = build_tree(tokens, tree.expr.right)
        elif tokens[0].type == "Str":
            tree.expr.left = tc.Str()
            tokens = build_tree(tokens, tree.expr.left)
            tree.expr.op = tc.Op()
            tokens = build_tree(tokens, tree.expr.op)
            tree.expr.right = tc.Str()
            tokens = build_tree(tokens, tree.expr.right)
        return tokens

    elif tree.node == "expr" and tokens[0].type == 'concat':
        tree.expr = tc.S_Expr_Concat()
        tokens = tokens[1:]
        tokens = build_tree(tokens, tree.expr.start)
        tokens = build_tree(tokens, tree.expr.expr1)
        if(tokens[0].value != ","):
            print("Syntax Error: Expected , got " + str(tokens[0].value) + ", \""+tokens[0].line[1]+"\" Line: " + str(tokens[0].line[0]))
            sys.exit()

        else:
            tokens = tokens[1:]
        tokens = build_tree(tokens, tree.expr.expr2)
        tokens = build_tree(tokens, tree.expr.stop)
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
            if tokens[1].type in math_operators:
                # Create integer expression
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
            elif tokens[1].type in comp_operators:
                tree.expr = tc.I_expr_triple_comp()
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
            if tokens[1].type in math_operators:
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
        # else:
            # print("We shouldn't be here")

        return tokens

    elif tree.node == "s_expr" and tokens[0].type == 'concat':
        tree.child = tc.S_Expr_Concat()
        tokens = tokens[1:]
        tokens = build_tree(tokens, tree.child.start)
        tokens = build_tree(tokens, tree.child.expr1)
        tokens = tokens[1:]
        tokens = build_tree(tokens, tree.child.expr2)
        tokens = build_tree(tokens, tree.child.stop)
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
        if(tokens[0].value != ","):
            print("Syntax Error: Expected , got " + str(tokens[0].value) + ", \""+tokens[0].line[1]+"\" Line: " + str(tokens[0].line[0]))
            sys.exit()
        else:
            tokens = tokens[1:]
        tokens = build_tree(tokens, tree.expr.expr2)
        tokens = build_tree(tokens, tree.expr.stop)
        return tokens

    elif tree.node == "start_paren" :
        if tokens[0].type == "(":
            return tokens[1:]
        else:
            print("Syntax Error: Expected ( got " + str(tokens[0].value) + ", \""+tokens[0].line[1]+"\" Line: " + str(tokens[0].line[0]))
            sys.exit()


    elif tree.node == "end_paren":
        if tokens[0].type == ")":
            return tokens[1:]
        else:
            print("Syntax Error: Expected ) got " + str(tokens[0].value) + ", \""+tokens[0].line[1]+"\" Line: " + str(tokens[0].line[0]))
            sys.exit()


    elif tree.node == "start_blk":
        if tokens[0].type == "{":
            return tokens[1:]
        else:
            print("Syntax Error: Expected { got " + str(tokens[0].value) + ", \""+tokens[0].line[1]+"\" Line: " + str(tokens[0].line[0]))

    elif tree.node == "end_blk":
        if tokens[0].type == "}":
            return tokens[1:]
        else:
            print("Syntax Error: Expected } got " + str(tokens[0].value) + ", \""+tokens[0].line[1]+"\" Line: " + str(tokens[0].line[0]))

    elif tree.node == "end_stmt":
        if tokens[0].type == ";":
            return tokens[1:]
        else:
            print("Syntax Error: Expected ; got " + str(tokens[0].value) + ", \""+tokens[0].line[1]+"\" Line: " + str(tokens[0].line[0]))
            sys.exit()


    elif tree.node == "op" and (tokens[0].type in math_operators or tokens[0].type in comp_operators):
        tree.op = tokens[0].type
        return tokens[1:]

    elif tree.node == "expr" and tokens[0].type == "Str":
        tree.expr = tc.S_expr()
        tokens = build_tree(tokens, tree.expr)

    elif tree.node == "expr" and tokens[0].type == "ID":
        tree.expr = tc.Id()
        tree.expr.child = tokens[0].value
        return tokens[1:]

    elif tree.node == "i_expr" \
            and (tokens[0].type == "Number" or (tokens[0].type == "-" and tokens[1].type == "Number")):
        if (tokens[1].value == ";" or tokens[1].value == ")" or tokens[1].value == "(") \
                or ((tokens[0].type == "-" and tokens[1].type == "Number")
                    and (tokens[2].value == ";" or tokens[2].value == ")" or tokens[2].value == "(")):
            tree.child = tc.Int()
            tokens = build_tree(tokens, tree.child)
        else:
            last = next(i for i, v in enumerate(tokens) if (v.type == ")" or v.type == ";")) - 1
            tree.right = tc.Int()
            tree.right.int = tokens.pop(last).value
            tree.op = tc.Op()
            if tokens[last-1].value == "-" and (tokens[last-2].value in math_operators):
                tree.right.sign.child = tokens.pop(last-1).value
                tree.op.op = tokens.pop(last - 2).value
            else:
                tree.op.op = tokens.pop(last - 1).value
            #  pay no attention to these disgusting if statements
            if (tokens[0].type == "Number" and (tokens[1].type in math_operators)) or \
                    ((tokens[0].type == "-" and tokens[1].type == "Number") and (tokens[2].type in math_operators)):
                tree.left = tc.I_expr_triple()
            else:
                tree.left = tc.Int()
            tokens = build_tree(tokens, tree.left)

        return tokens

    elif tree.node == "d_expr" \
            and (tokens[0].type == "Number" or (tokens[0].type == "-" and tokens[1].type == "Number")):
        # tree.expr = tc.D_expr_triple()
        if (tokens[1].value == ";" or tokens[1].value == ")" or tokens[1].value == "(") \
                or ((tokens[0].type == "-" and tokens[1].type == "Number")
                    and (tokens[2].value == ";" or tokens[2].value == ")" or tokens[2].value == "(")):
            tree.child = tc.Dbl()
            tokens = build_tree(tokens, tree.child)
        else:
            last = next(i for i, v in enumerate(tokens) if (v.type == ")" or v.type == ";")) - 1
            tree.right = tc.Dbl()
            tree.right.dbl = tokens.pop(last).value
            tree.op = tc.Op()
            if tokens[last - 1].value == "-" and (tokens[last - 2].value in math_operators):
                tree.right.sign.child = tokens.pop(last - 1).value
                tree.op.op = tokens.pop(last - 2).value
            else:
                tree.op.op = tokens.pop(last - 1).value
            if (tokens[0].type == "Number" and (tokens[1].type in math_operators)) or \
                    ((tokens[0].type == "-" and tokens[1].type == "Number") and (tokens[2].type in math_operators)):
                tree.left = tc.D_expr_triple()
            else:
                tree.left = tc.Dbl()
            tokens = build_tree(tokens, tree.left)
        return tokens


    elif tree.node == "expr" and tokens[0].type == "Number" and '.' not in tokens[0].value:
        if tokens[1].type in math_operators:
            tree.expr = tc.I_expr_triple()
            last = next(i for i, v in enumerate(tokens) if (v.type == ")" or v.type == ";")) - 1
            tree.expr.right = tc.Int()
            tree.expr.right.int = tokens.pop(last).value
            tree.expr.op = tc.Op()
            if tokens[last - 1].value == "-" and (tokens[last - 2].value in math_operators):
                tree.expr.right.sign.child = tokens.pop(last - 1).value
                tree.expr.op.op = tokens.pop(last - 2).value
            else:
                tree.expr.op.op = tokens.pop(last - 1).value
            if tokens[1].type in math_operators:
                tree.expr.left = tc.I_expr_triple()
            else:
                tree.expr.left = tc.Int()
            tokens = build_tree(tokens, tree.expr.left)
        else:
            tree.expr = tc.I_expr_single()
            tokens = build_tree(tokens, tree.expr)

    elif tree.node == "expr" and tokens[0].type == "-" and tokens[1].type == "Number" and '.' not in tokens[1].value:
        if tokens[2].type in math_operators:
            tree.expr = tc.I_expr_triple()
            last = next(i for i, v in enumerate(tokens) if (v.type == ")" or v.type == ";")) - 1
            tree.expr.right = tc.Int()
            tree.expr.right.int = tokens.pop(last).value
            tree.expr.op = tc.Op()
            if tokens[last - 1].value == "-" and (tokens[last - 2].value in math_operators):
                tree.expr.right.sign.child = tokens.pop(last - 1).value
                tree.expr.op.op = tokens.pop(last - 2).value
            else:
                tree.expr.op.op = tokens.pop(last - 1).value
            if tokens[2].type in math_operators:
                tree.expr.left = tc.I_expr_triple()
            else:
                tree.expr.left = tc.Int()
            tokens = build_tree(tokens, tree.expr.left)
        else:
            tree.expr = tc.I_expr_single()
            tokens = build_tree(tokens, tree.expr)

    elif tree.node == "expr" and tokens[0].type == "Number" and '.' in tokens[0].value:
        if tokens[1].type in math_operators:
            tree.expr = tc.D_expr_triple()
            last = next(i for i, v in enumerate(tokens) if (v.type == ")" or v.type == ";")) - 1
            tree.expr.right = tc.Dbl()
            tree.expr.right.dbl = tokens.pop(last).value
            tree.expr.op = tc.Op()
            if tokens[last - 1].value == "-" and (tokens[last - 2].value in math_operators):
                tree.expr.right.sign.child = tokens.pop(last - 1).value
                tree.expr.op.op = tokens.pop(last - 2).value
            else:
                tree.expr.op.op = tokens.pop(last - 1).value
            if tokens[1].type in math_operators:
                tree.expr.left = tc.D_expr_triple()
            else:
                tree.expr.left = tc.Dbl()
            tokens = build_tree(tokens, tree.expr.left)

        else:
            tree.expr = tc.D_expr_single()
            tokens = build_tree(tokens, tree.expr)

    elif tree.node == "expr" and tokens[0].type == "-" and tokens[1].type == "Number" and '.' in tokens[1].value:
        if tokens[2].type in math_operators:
            tree.expr = tc.D_expr_triple()
            last = next(i for i, v in enumerate(tokens) if (v.type == ")" or v.type == ";")) - 1
            tree.expr.right = tc.Dbl()
            tree.expr.right.dbl = tokens.pop(last).value
            tree.expr.op = tc.Op()
            if tokens[last - 1].value == "-" and (tokens[last - 2].value in math_operators):
                tree.expr.right.sign.child = tokens.pop(last - 1).value
                tree.expr.op.op = tokens.pop(last - 2).value
            else:
                tree.expr.op.op = tokens.pop(last - 1).value
            if tokens[2].type in math_operators:
                tree.expr.left = tc.D_expr_triple()
            else:
                tree.expr.left = tc.Dbl()
            tokens = build_tree(tokens, tree.expr.left)

        else:
            tree.expr = tc.D_expr_single()
            tokens = build_tree(tokens, tree.expr)

    elif tree.node == 'int':
        if tokens[0].type == "-" or tokens[0].type == "+":
            tree.sign.child = tokens[0].value
            tokens = tokens[1:]
        tree.int = tokens[0].value
        return tokens[1:]

    elif tree.node == "str":
        tree.str = tokens[0].value
        return tokens[1:]


    elif tree.node == "i_expr":
        if tokens[0].type == "ID":
            if tokens[1].type in comp_operators:
                tree.expr = tc.I_expr_triple_comp()
                tree.expr.left = tc.Id()
                tokens = build_tree(tokens, tree.expr.left)
                tree.expr.op = tc.Op()
                tokens = build_tree(tokens, tree.expr.op)
                tree.expr.right = tc.Int()
                tokens = build_tree(tokens, tree.expr.right)
            else:
                tree.child = tc.Id()
                tree.child.child = tokens[0].value
                return tokens[1:]
        else:
            tree.child = tc.Int()
            if tokens[0].type == "-" or tokens[0].type == "+":
                tree.child.sign.child = tokens[0].value
                tokens = tokens[1:]
            tree.child.int = tokens[0].value
            return tokens[1:]
        # return tokens[1:]

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
        if tokens[0].type == "ID":
            tree.child = tc.Id()
            tree.child.child = tokens[0].value
        else:
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
    elif tree.node == "p_list":
        if tokens[0].value == "String" or tokens[0].value == "Integer" or tokens[0].value == "Double":
            tree.type = tokens[0].value
            tokens = tokens[1:]
            tree.p_id.child = tokens[0].value
            variables[tokens[0].value] = tree.type
            tokens = tokens[1:]
            if tokens[0].value == ',':
                tree.p_list = tc.P_List()
                tokens = tokens[1:]
                tokens = build_tree(tokens, tree.p_list)
        return tokens
    elif tree.node == 'fc_p_list':
        raw_val = tokens[0].value.replace("\'","")
        tree.expr.append(raw_val.replace("\"",""))
        tokens = tokens[1:]
        if tokens[0].value == ',':
            tokens = tokens[1:]
            tokens = build_tree(tokens,tree)
        return tokens

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
            if (char != " " and char != "\n") or (state ==14 and char != "\n"):
                token_i.value += char
            last_state = state
            state = accepts(dfa, state, char)
            if state == "break_b":
                if (char != " " and char != "\n") or (state ==14 and char != "\n"):
                    token_i.value = token_i.value[:-1]
                    token_i.line = [line_num, line]
                    if last_state == 14:
                        print("Syntax Error: Missing \", \"" + token_i.line[1] + "\" Line: " + str(token_i.line[0]))
                        return False
                    if token_i.value == "Integer" or token_i.value == "Double" or token_i.value == "Void" or token_i.value == "String" \
                            or token_i.value == "print" or token_i.value == "concat" or token_i.value == "charAt":
                        token_i.type = token_i.value
                    else:
                        token_i.type = term_tokens[last_state]
                    tokens.append(token_i)
                    token_i = tc.Token()
                    token_i.value = char
                else:
                    token_i.line = [line_num, line]
                    if token_i.value == "Integer" or token_i.value == "Double"or token_i.value == "Void" or token_i.value == "String" \
                            or token_i.value == "print" or token_i.value == "concat" or token_i.value == "charAt":
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
                if token_i.value == "Integer" or token_i.value == "Double" or token_i.value == "Void" or token_i.value == "String" \
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
        if token_i.value == "Integer" or token_i.value == "Double" or token_i.value == "String"or token_i.value == "Void":
            token_i.type = token_i.value
        else:
            token_i.type = term_tokens[last_state]
        tokens.append(token_i)

    token_i = tc.Token()
    token_i.value = "$$"
    token_i.line = [line_num, line]
    token_i.type = "$$"
    tokens.append(token_i)
    global token_copy
    token_copy = tokens
    return tokens
