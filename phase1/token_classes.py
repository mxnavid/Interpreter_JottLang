# token classes

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


class Stmt_single:
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
        self.child = None
"""
class Id:
    def __init__(self):
        self.node = "id"
        self.left = L_char()
        self.right = [str(),None]
"""

class Print:
    def __init__(self):
        self.node = "print"
        self.print = "print"
        self.start = Start_paren()
        self.expr = Expr()
        self.stop = End_paren()
        self.end = End_stmt()


class S_Expr_Concat:
    def __init__(self):
        self.node = "s_expr"
        self.concat = "concat"
        self.start = Start_paren()
        self.expr1 = S_expr()
        self.expr2 = S_expr()
        self.comma = ","
        self.stop = End_paren()
        self.end = End_stmt()

class S_Expr_CharAt:
    def __init__(self):
        self.node = "s_expr"
        self.concat = "charAt"
        self.start = Start_paren()
        self.expr1 = S_expr()
        self.expr2 = Expr()
        self.comma = ","
        self.stop = End_paren()
        self.end = End_stmt()

class Addition:
    def __init__(self):
        self.node = "addition"
        self.type = "addition"
        self.start = Digit()
        self.end = End_stmt()


class Asmt:
    def __init__(self):
        self.node = "asmt"
        self.type = None
        self.id = Id()
        self.equals = "="
        self.expr = None
        self.end = End_stmt()


class Id:
    def __init__(self):
        self.node = "id"
        self.child = None


class Expr:
    def __init__(self):
        self.node = "expr"
        #self.expr = [i_expr(),d_expr(),s_expr(),id()]
        self.expr = None


class I_expr:
    def __init__(self):
        self.node = "i_expr"


class I_expr_single(I_expr):
    def __init__(self):
        super().__init__()
        self.child = None


class I_expr_triple(I_expr):
    def __init__(self):
        super().__init__()
        self.left = None
        self.op = None
        self.right = None


class D_expr:
    def __init__(self):
        self.node = "d_expr"


class D_expr_single(D_expr):
    def __init__(self):
        super().__init__()
        self.child = None


class D_expr_triple(D_expr):
    def __init__(self):
        super().__init__()
        self.left = None
        self.op = None
        self.right = None


class S_expr:
    def __init__(self):
        self.node = "s_expr"
        self.child = None


class Op:
    def __init__(self):
        self.node = "op"
        self.op = None


class Dbl:
    #WIP
    def __init__(self):
        self.node = "dbl"
        self.sign = Sign()
        self.dbl = None


class Int:
    #WIP
    def __init__(self):
        self.node = "int"
        self.sign = Sign()
        self.int = None


class Str:
    #WIP
    def __init__(self):
        self.node = "str"
        self.str = [Char(), Space(), str(), None]


class Str_literal:
    #WIP
    def __init__(self):
        self.node = "str_literal"
        self.child = None