def verify_code(tree, tokens):
    if tree.node == "program":
        good = verify_code(tree.left, tokens)
        if not good and good is False:  # have to differentiate between 0 and false due to comparators
            return False
        else:
            return True
    elif tree.node == "stmt_list" and tree.left is not None and tree.right is not None:
        good = tree.left.verify()
        if not good and good is False:  # have to differentiate between 0 and false due to comparators
            print("\""+tokens[0].line[1].rstrip() + "\" Line: " + str(tokens[0].line[0]))
            return False
        if tokens[0].value == "if" or tokens[0].value == "for" or tokens[0] == "while":
            tokens.pop(0)
            bracket_ctr = 1
            while bracket_ctr:
                if tokens[0].value == "if" or tokens[0].value == "for" or tokens[0].value == "while" or tokens[0].value == "else":
                    bracket_ctr += 1
                elif tokens[0].value == '}':
                    bracket_ctr -= 1
                tokens.pop(0)
        else:
            while tokens:
                if tokens.pop(0).type == ';':
                    if tokens[0].type == "}":
                        tokens.pop(0)
                        break
                    else:
                        break
        return verify_code(tree.right, tokens)
    return True


def gen_code(tree):
    if tree.node == "program":
        gen_code(tree.left)
    elif tree.node == "stmt_list" and tree.left is not None and tree.right is not None:
        tree.left.eval()
        gen_code(tree.right)
