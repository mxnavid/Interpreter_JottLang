# token classes
variables = {}
func_dict = {}
func_params = {}

scope = "_global"

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
            self.left.eval()
            return self.right.eval()


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


class Start_blk:
    def __init__(self):
        self.node = "start_blk"
        self.child = "{"


class End_blk:
    def __init__(self):
        self.node = "end_blk"
        self.child = "}"


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
        if self.id.child+scope in variables:
            return True
        else:
            var = self.id.verify()
            val = self.expr.verify()
            if val != None:
                variables[var+scope] = val
        return val

    def eval(self):
        if self.id.child+scope in variables:
            variables[self.id.child + scope] = self.expr.eval()
        elif self.id.child+'_global' in variables:
            variables[self.id.child + '_global'] = self.expr.eval()


class While_loop:
    def __init__(self):
        self.node = "while"
        self.startparen = Start_paren()
        self.comp = I_expr()
        self.endparen = End_paren()
        self.startblk = Start_blk()
        self.stmtlist = Stmt_list()
        self.endblk = End_blk()

    def verify(self):
        if self.stmtlist.verify():
            return True
        return False

    def eval(self):
        while self.comp.expr.eval():
            self.stmtlist.eval()


class For_loop:
    def __init__(self):
        self.node = "for"
        self.startparen = Start_paren()
        self.asmt = Asmt()
        self.endAsmt = End_stmt()
        self.iexpr = I_expr()
        self.endIexpr = End_stmt()
        self.reasmt = Asmt()
        self.endparen = End_paren()
        self.startblk = Start_blk()
        self.stmtlist = Stmt_list()
        self.endblk = End_blk()

    def verify(self):
        if self.asmt.verify() and self.iexpr.expr.verify() and self.reasmt.verify():
            if self.stmtlist.verify():
                return True

        return False

    def eval(self):
        while self.iexpr.expr.eval():
            self.stmtlist.eval()
            self.reasmt.eval()


class Id:
    def __init__(self):
        self.node = "id"
        self.child = None

    def verify(self):
        if self.child+scope in variables:
            return variables[self.child+scope]
        else:
            return self.child

    def eval(self):
        if self.child+scope in variables:
            return variables[self.child+scope]
        elif self.child+'_global' in variables:
            return variables[self.child+'_global']
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


class I_expr_triple_comp(I_expr):
    def __init__(self):
        super().__init__()
        self.node = "comp_expr"
        self.left = None
        self.op = None
        self.right = None

    def verify(self):
        left = self.left.verify()
        right = self.right.verify()
        if type(left) != type(right):
            print("Syntax Error: Type mismatch: Expected " + str(type(left).__name__).upper() + " got " + str(
                type(right).__name__).upper(), end=", ")
            return False
        else:
            if self.op.op == ">":
                if left > right:
                    return 1
                else:
                    return 0
            elif self.op.op == "<":
                if left < right:
                    return 1
                else:
                    return 0
            elif self.op.op == ">=":
                if left >= right:
                    return 1
                else:
                    return 0
            elif self.op.op == "<=":
                if left <= right:
                    return 1
                else:
                    return 0
            elif self.op.op == "==":
                if left == right:
                    return 1
                else:
                    return 0
            elif self.op.op == "!=":
                if left != right:
                    return 1
                else:
                    return 0

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if self.op.op == ">":
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
        else:  # ==
            if left == right:
                return 1
            else:
                return 0


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

    def verify(self):
        return self.str  # should probably make this actually do something

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


class If_expr:
    #WIP
    def __init__(self):
        self.node = "if"
        self.startparen = Start_paren()
        self.comp = Expr()
        self.stopparen= End_paren()
        self.startblk = Start_blk()
        self.stmtlist = Stmt_list()
        self.stopblk = End_blk()
        self.elseblk = None
        self.elsestmt = None
        self.elseblkend = None

    def verify(self):
        if self.stmtlist.verify():
            if self.elseblk == Start_paren():      # so if there is else statement we will verify it
                if self.elsestmt.verify():
                    return True
                return False
            else:
                return True
        return False

    def eval(self):
        if self.comp.eval() > 0:
            return self.stmtlist.eval()
        else:
            if self.elsestmt is not None:
                return self.elsestmt.eval()

class P_List():
    def __init__(self):
        self.node = "p_list"
        self.type = None
        self.p_id = Id()
        self.p_list = None

    def verify(self, func_id):
        if self.p_id.child:
            if not self.p_id.child + scope in variables:
                variables[self.p_id.child+scope] = None
            func_params[func_id].append(self.p_id.child)
            if self.p_list:
                self.p_list.verify(func_id)
    def eval(self):
        return 1

class FC_P_List():
    def __init__(self):
        self.node = "fc_p_list"
        self.expr = []
        #self.fc_p_list = None

    def verify(self):
        self.expr.verify()
        self.fc_p_list.verify()

    def eval(self):
        self.expr.eval()
        self.fc_p_list.eval()

class Func():
    def __init__(self):
        self.node = "func"
        self.type = None
        self.f_id = Id()
        self.startParen = Start_paren()
        self.p_list = P_List()
        self.endParen = End_paren()
        self.startblk = Start_blk()
        self.func_stmt = func_stmt()
        self.endblk = End_blk()

    def verify(self):
        global scope
        scope = "_local"
        func_params[self.f_id.child] = []
        self.p_list.verify(self.f_id.child)
        func_dict[self.f_id.child] = self.func_stmt
       #self.func_stmt.verify()
        scope = "_global"
        return True

    def eval(self):
        return 1

class func_stmt:
    def __init__(self):
        self.node = "func_stmt"
        self.left = None
        self.right = None
        self.rtrn = None

    def verify(self):
        if self.left and self.right:
            return True if self.left.verify() and self.right.verify() else False
        elif self.rtrn:
            pass
        return True

    def eval(self):
        if self.left and self.right:
            self.left.eval()
            return self.right.eval()
        elif self.rtrn:
            return self.rtrn.eval()


class F_Call:
    def __init__(self):
        self.node = "f_call"
        self.f_id = Id()
        self.startParen = Start_paren()
        self.fc_p_list = FC_P_List()
        self.endParen = End_paren()
        self.end = End_stmt()

    def verify(self):
        return self.f_id.child in func_dict

    def eval(self):
        global scope
        scope = "_local"
        index = 0
        for var in func_params[self.f_id.child]:
            if (isinstance(self.fc_p_list.expr[index], F_Call)):
                val = self.fc_p_list.expr[index].eval()
                variables[var + scope] = val
            else:
                if str(self.fc_p_list.expr[index])+"_global" in variables:
                    variables[var+scope] = variables[self.fc_p_list.expr[index]+"_global"]
                else:
                    variables[var+scope] = self.fc_p_list.expr[index]
            index += 1
        temp = func_dict[self.f_id.child].eval()
        scope = "_global"
        return temp




class rtrn:
    def __init__(self):
        self.node = "rtrn"
        self.print = "rtrn"
        self.expr = Expr()
        self.end = End_stmt()
    def verify(self):
        return self.expr.verify()

    def eval(self):
        return (self.expr.eval())