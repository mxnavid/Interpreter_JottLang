# functions to be called when interpreting from decorated tree

def add(a,b):
    return a + b

def subtract(a,b):
    return a - b

def divideInt(a,b):
    return a // b

def divideDbl(a,b):
    return a / b

def multiply(a,b):
    return a * b

def power(a,b):
    return a ** b

def print(strOrNum):
    print(strOrNum)
    return

def concat(str1,str2):
    return str1 + str2

def charAt(str,index):
    return str[index]
