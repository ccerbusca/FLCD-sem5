from Lab2 import SymbolTable
import sys
import re

reserved_words = ["var", "val", "def", "for", "while", "if", "else", "println", "print",
"Char", "intinput", "input", "break", "String", "void", "Integer", "Boolean", "Array"]
reserved_ops = ["+", "-", "*", "/", "=", "==", "!=" , "<", "<=", ">", ">=", "+=", "-=", "*=", "/=",
 "%", "..", "@", "||", "&&", "[", "]", "{", "}", ";", ":", "(", ")"]

class PIF:
    def __init__(self):
        self.__data = []

    def __setitem__(self, key, pos):
        self.__data.append((key, pos))
    
    def __str__(self):
        return "\n".join(map(str, self.__data))

def is_constant_or_identifier(token):
    try:
        int(token)
    except:
        return re.match(r"^[0-9]", token) is None and \
                (re.match(r'^".+"$', token) is not None \
                    or re.match(r"^`.+`$", token) is not None \
                    or re.match(r"^'.'$", token) is not None \
                    or re.match(r'^.+$', token))
    return True


pif = PIF()
st = SymbolTable()

if len(sys.argv) != 2:
    raise Exception("Only 1 parameter allowed")
else:
    with open(sys.argv[1]) as f:
        i = 1
        line = f.readline()
        while line:
            print(line)
            split = re.findall(r'`.+`|".+"|\'.\'|[:;()\[\]\.\+\-\*/=!<>%@|&\(\)]|[^:;()\s\[\]\.\+\-\*/=!<>%@|&\(\)]+', line)
            split = list(filter(lambda x: x is not None and x != '', map(lambda x: x.strip(), split)))
            print(split)

            i = 0
            while i < len(split) - 1:
                if split[i] in ('=', '!', '<', '>', '+', '-', '*', '/'):
                    if split[i + 1] == '=':
                        split[i] = '=='
                        del split[i + 1]
                if split[i] == '.' and split[i + 1] == '.':
                    split[i] = '..'
                    del split[i + 1]
                if split[i] == '|' and split[i + 1] == '|':
                    split[i] = '||'
                    del split[i + 1]
                if split[i] == '&' and split[i + 1] == '&':
                    split[i] = '&&'
                    del split[i + 1]
                i += 1


            for token in split:
                if token in reserved_words or token in reserved_ops:
                    pif[token] = 0
                elif is_constant_or_identifier(token):
                    index = st.add(token)
                    pif[token] = index
                else:
                    raise Exception("Lexical error. Invalid token: '{}' on line {}".format(token, i))
            line = f.readline()
            i += 1


print(st, "\n")
print(pif)

print("Valid program!")


