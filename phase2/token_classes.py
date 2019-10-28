# token classes
variables = {}

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
    def verify(self):
        return self.left.verify()

    def eval(self):
        return self.left.eval()


class Stmt_list:
    def __init__(self):
        self.node = "stmt_list"
        self.left = None
        self.right = None
    def verify(self):
        if self.left and self.right:
            return self.left.verify()
    def eval(self):
        if self.left and self.right:
            return self.left.eval()


class Stmt:
    def __init__(self):
        self.node = "stmt"
        self.left = None
        self.right = None
    def verify(self):
        return self.left.verify()
    def eval(self):
        self.left.eval()


class Stmt_single:
    def __init__(self):
        self.node = "stmt"
        self.child = None
    def verify(self):
        return self.child.verify()

    def eval(self):
        self.child.eval()


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
    def verify(self):
        return self.child.verify()
    def eval(self):
        return self.child.eval()
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
    def verify(self):
        return self.expr.verify()

    def eval(self):
        print(self.expr.eval())

class S_Expr_Concat:
    def __init__(self):
        self.node = "s_expr"
        self.concat = "concat"
        self.start = Start_paren()
        self.expr1 = S_expr()
        self.expr2 = S_expr()
        self.comma = ","
        self.stop = End_paren()

    def verify(self):
        return self.expr1.verify()+self.expr2.verify()

    def eval(self):
        return self.expr1.eval()+self.expr2.eval()




class S_Expr_CharAt:
    def __init__(self):
        self.node = "s_expr"
        self.concat = "charAt"
        self.start = Start_paren()
        self.expr1 = S_expr()
        self.expr2 = Expr()
        self.comma = ","
        self.stop = End_paren()

    def verify(self):
        pos = int(self.expr2.verify())
        given_string = str(self.expr1.verify())
        return given_string[pos]

    def eval(self):
        pos = int(self.expr2.eval())
        given_string = str(self.expr1.eval())
        return given_string[pos]

class Asmt:
    def __init__(self):
        self.node = "asmt"
        self.type = None
        self.id = Id()
        self.equals = "="
        self.expr = None
        self.end = End_stmt()

    def verify(self):
        var = self.id.verify()
        val = self.expr.verify()
        if val:
            variables[var] = val
        return True

    def eval(self):
        variables[self.id.eval()] =  self.expr.eval()


class While_loop:
    def __init__(self):
        self.node = "while"
        self.type = None
        self.left = I_expr
        self.right = Stmt_list

    def verify(self):
        return "true"

    def eval(self):
        return 1



class Id:
    def __init__(self):
        self.node = "id"
        self.child = None

    def verify(self):
        if self.child in variables:
            return variables[self.child]
        else:
            return self.child

    def eval(self):
        if self.child in variables:
            return variables[self.child]
        else:
            return self.child

class Expr:
    def __init__(self):
        self.node = "expr"
        #self.expr = [i_expr(),d_expr(),s_expr(),id()]
        self.expr = None

    def verify(self):
        return self.expr.verify()

    def eval(self):
        return self.expr.eval()

class I_expr:
    def __init__(self):
        self.node = "i_expr"


class I_expr_single(I_expr):
    def __init__(self):
        super().__init__()
        self.child = None
    def verify(self):
        return self.child.verify()

    def eval(self):
        return self.child.eval()

class I_expr_triple(I_expr):
    def __init__(self):
        super().__init__()
        self.left = None
        self.op = None
        self.right = None

    def verify(self):
        left = self.left.verify()
        right = self.right.verify()
        if right != "-":
            if self.op.op == "/" and right == 0:
                print("Runtime Error: Divide by zero",end =", ")
                return False
            if type(left) != type(right):
                print("Syntax Error: Type mismatch: Expected " + str(type(left).__name__).upper() + " got " + str(type(right).__name__).upper(),end =", ")
                return False
            else:
                if self.op.op == "+":
                    return left + right
                elif self.op.op == "-":
                    return left - right
                elif self.op.op == "*":
                    return left * right
                elif self.op.op == "/":
                    return left // right  # floor division
                elif self.op.op == ">":
                    if left > right:
                        return "true"
                    else:
                        return "false"
                elif self.op.op == "<":
                    if left < right:
                        return "true"
                    else:
                        return "false"
                elif self.op.op == "<=":
                    if left <= right:
                        return "true"
                    else:
                        return "false"
                elif self.op.op == ">=":
                    if left >= right:
                        return "true"
                    else:
                        return "false"
                elif self.op.op == "!=":
                    if left != right:
                        return "true"
                    else:
                        return "false"
                else:  # op == ^
                    return left ** right
        else:
            return False

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()

        if self.op.op == "+":
            return left + right
        elif self.op.op == "-":
            return left - right
        elif self.op.op == "*":
            return left * right
        elif self.op.op == "/":
            return left // right  # floor division
        elif self.op.op == ">":
            if left > right:
                return 1
            else:
                return 0
        elif self.op.op == "<":
            if left < right:
                return 1
            else:
                return 0
        elif self.op.op == "<=":
            if left <= right:
                return 1
            else:
                return 0
        elif self.op.op == ">=":
            if left >= right:
                return 1
            else:
                return 0
        elif self.op.op == "!=":
            if left != right:
                return 1
            else:
                return 0
        else:  # op == ^
            return left ** right

class D_expr:
    def __init__(self):
        self.node = "d_expr"


class D_expr_single(D_expr):
    def __init__(self):
        super().__init__()
        self.child = None

    def verify(self):
        return self.child.verify()

    def eval(self):
        return self.child.eval()

class D_expr_triple(D_expr):
    def __init__(self):
        super().__init__()
        self.left = None
        self.op = None
        self.right = None

    def verify(self):
        left = self.left.verify()
        right = self.right.verify()
        if right != "-":
            if self.op.op == "/" and right == 0:
                print("Runtime Error: Divide by zero",end =", ")
                return False
            if type(left) != type(right):
                print("Syntax Error: Type mismatch: Expected " + str(type(left).__name__).upper() + " got " + str(
                    type(right).__name__).upper(),end =", ")
                return False
            else:
                if self.op.op == "+":
                    return left + right
                elif self.op.op == "-":
                    return left - right
                elif self.op.op == "*":
                    return left * right
                elif self.op.op == "/":
                    return left // right  # floor division
                elif self.op.op == ">":
                    if left > right:
                        return "true"
                    else:
                        return "false"
                elif self.op.op == "<":
                    if left < right:
                        return "true"
                    else:
                        return "false"
                elif self.op.op == "<=":
                    if left <= right:
                        return "true"
                    else:
                        return "false"
                elif self.op.op == ">=":
                    if left >= right:
                        return "true"
                    else:
                        return "false"
                elif self.op.op == "!=":
                    if left != right:
                        return "true"
                    else:
                        return "false"
                else:  # op == ^
                    return left ** right
        else:
            return False

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()

        if self.op.op == "+":
            return left + right
        elif self.op.op == "-":
            return left - right
        elif self.op.op == "*":
            return left * right
        elif self.op.op == "/":
            return left / right
        elif self.op.op == ">":
            if left > right:
                return 1
            else:
                return 0
        elif self.op.op == "<":
            if left < right:
                return 1
            else:
                return 0
        elif self.op.op == "<=":
            if left <= right:
                return 1
            else:
                return 0
        elif self.op.op == ">=":
            if left >= right:
                return 1
            else:
                return 0
        elif self.op.op == "!=":
            if left != right:
                return 1
            else:
                return 0
        else:  # op == ^
            return left ** right


class S_expr:
    def __init__(self):
        self.node = "s_expr"
        self.child = None

    def verify(self):
        return self.child.verify()

    def eval(self):
        return self.child.eval()

class Op:
    def __init__(self):
        self.node = "op"
        self.op = None

    def eval(self):
        return self.op.eval()

class Dbl:
    #WIP
    def __init__(self):
        self.node = "dbl"
        self.sign = Sign()
        self.dbl = None

    def verify(self):

        try:
            if "." in self.dbl:
                if self.sign.child == "-":
                    return float(self.dbl) * -1
                return float(self.dbl)
            else:
                raise ValueError
        except ValueError:
            try:
                temp = int(self.dbl)
                print("Syntax Error: Type mismatch: Expected Float got: Integer", end=", ")
            except ValueError:
                print("Syntax Error: Type mismatch: Expected Float got: String",end =", ")

            return "-"
    def eval(self):
        if self.sign.child == "-":
            return float(self.dbl) * -1
        return float(self.dbl)


class Int:
    #WIP
    def __init__(self):
        self.node = "int"
        self.sign = Sign()
        self.int = None

    def verify(self):

        try:
            if self.sign.child == "-":
                return int(self.int) * -1
            return int(self.int)
        except ValueError:
            if "." in self.int:
                print("Syntax Error: Type mismatch: Expected Integer got: Float",end =", ")
            else:
                print("Syntax Error: Type mismatch: Expected Integer got: String",end =", ")
            return "-"

    def eval(self):
        if self.sign.child == "-":
            return int(self.int) * -1
        return int(self.int)


class Str:
    #WIP
    def __init__(self):
        self.node = "str"
        self.str = [Char(), Space(), str(), None]

    def eval(self):
        return self.str


class Str_literal:
    #WIP
    def __init__(self):
        self.node = "str_literal"
        self.child = None

    def verify(self):
        return self.child.replace("\"", "")

    def eval(self):
        return self.child.replace("\"", "")
