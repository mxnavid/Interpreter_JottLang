import re
from constants import dfa, term_tokens, follows
import token_classes as tc

def gen_code(tree):
    if tree.node == "program":
        gen_code(tree.left)
    elif tree.node == "stmt_list" and tree.left is not None and tree.right is not None:
        tree.left.eval()
        gen_code(tree.right)
