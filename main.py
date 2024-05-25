"""Simple example: Read a sequence of sums,
parse with Lark to form concrete syntax tree,
transform to form abstract syntax tree.
"""

import sys
import lark
import grammar_ast
import grammar_reshape


def main():
    # Step 1:  Process the grammar to create a parser (and lexer)
    if(len(sys.argv) != 2 and len(sys.argv) != 3):
        print("Correct usage is:")
        print("\t'main.py [file you wish to parse]' to print output to terminal")
        print("\tor")
        print("\t'main.py [file you wish to parse] [name of output .asm file]' to write output as .asm file")

<<<<<<< Updated upstream
=======
        print("Intiating test case")
        gram_file = open("grammar.lark", "r")
        parser = lark.Lark(gram_file, parser="lalr")
        src_file = open("example_grammar.txt", "r")
        src_text = "".join(src_file.readlines())
        concrete = parser.parse(src_text)
        print("Parse tree (concrete syntax):")
        print(concrete.pretty())
>>>>>>> Stashed changes
        return

    gram_file = open("grammar.lark", "r")
    parser = lark.Lark(gram_file, parser="lalr")

    # Step 2: Use the parser (and lexer) to create a parse tree
    # (concrete syntax)
    src_file = open(sys.argv[1], "r")
    src_text = "".join(src_file.readlines())
    concrete = parser.parse(src_text)
    print("Parse tree (concrete syntax):")
    print(concrete.pretty())

    # Step 3: Transform the concrete syntax tree into
    # an abstract tree, starting from the leaves and working
    # up.
    # Warning:  Lousy exceptions because of the way Lark applies these.

    if(len(sys.argv) != 3):
        transformer = grammar_reshape.SumsTransformer(False, "lol")
        ast = transformer.transform(concrete)
        print(ast)
        print(f"as {repr(ast)}")

    else:
        transformer = grammar_reshape.SumsTransformer(True, sys.argv[2])
        ast = transformer.transform(concrete)
        #out_file = open(f"{sys.argv[2]}.asm", "w")
        #out_file.write(f".class {sys.argv[2]}:Obj\n.method $constructor\n")
        #out_file.write(f"{ast}")

if __name__ == '__main__':
    main()