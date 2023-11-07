import token
from tokenize import tokenize

def find_definitions(filename):
    with open(filename, 'rb') as f:
        gen = tokenize(f.readline)
        for tok in gen:               
            if tok.type == token.NAME and tok.string == 'def':
                # function definition, read until next colon outside
                # parentheses.
                definition, last_line = [tok.line], tok.end[0]
                parens = 0
                while tok.exact_type != token.COLON or parens > 0:
                    if last_line != tok.end[0]:
                        definition.append(tok.line)
                        last_line = tok.end[0]
                    if tok.exact_type == token.LPAR:
                        parens += 1
                    elif tok.exact_type == token.RPAR:
                        parens -= 1
                    tok = next(gen)
                if last_line != tok.end[0]:
                    definition.append(tok.line)
                yield ''.join(definition)

if __name__ == '__main__':
    # This program takes an argument which is a Python source file.
    # It prints all the function definitions in that file.
    import sys
    for definition in find_definitions(sys.argv[1]):
        print(definition)
