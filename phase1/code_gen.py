import re
from constants import dfa, term_tokens, follows
import token_classes as tc

def verify_code(tree, tokens):
    if tree.node == "program":
        good = verify_code(tree.left, tokens)
        if not good:
            return False
        else:
            return True
    elif tree.node == "stmt_list" and tree.left is not None and tree.right is not None:
        good = tree.left.verify()
        if not good:
            return False
        return verify_code(tree.right, tokens)
    return True

def gen_code(tree, tokens):
    if tree.node == "program":
        gen_code(tree.left, tokens)
    elif tree.node == "stmt_list" and tree.left is not None and tree.right is not None:
        tree.left.eval()
        gen_code(tree.right, tokens)
