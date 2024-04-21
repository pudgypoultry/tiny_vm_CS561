"""Reshaping the concrete syntax or parse tree of a sequence of sums
into the desired abstract syntax tree.

Typically I would put this in the AST source file, but have separated it out
for this example so there is no confusion about the parts.
"""

import grammar_ast
import lark

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class SumsTransformer(lark.Transformer):
    """We write a transformer for each node in the parse tree
    (concrete syntax) by writing a method with the same name.
    Non-terminal symbols are passed a list of their children
    after transformation, which proceeds from leaves to root
    recursively. Terminal symbols (like NUMBER) are instead
    passed a lark.Token structure.
    """

    def __init__(self, write_to_file: bool, file_name: str):
        self.write_to_file = write_to_file
        self.file_name = file_name
        self.file_to_write_to = "lol"
        if(self.write_to_file):
<<<<<<< Updated upstream
            self.file_to_write_to = open(f"{file_name}.asm", "w")
=======
            self.file_to_write_to = open(f"unit_tests/{file_name}.asm", "w")
>>>>>>> Stashed changes
            self.file_to_write_to.write(f".class {file_name}:Obj\n.method $constructor\n")
            self.file_to_write_to.close()
            self.file_to_write_to = open(f"{file_name}.asm", "a")


    def NUMBER(self, data):
        """Terminal symbol, a regular expression in the grammar"""
        log.debug(f"Processing token NUMBER with {data}")
        val = int(data.value)
        ast_node = grammar_ast.Number(val)
        log.debug(f"Processed token into value {ast_node}")
        return ast_node

    def number(self, children):
        """number, unlike NUMBER, is a non-terminal symbol.
        It has a single child, which will have been transformed
        by the NUMBER method above.
        """
        log.debug(f"Processing 'number' with {children}")
        log.debug(f"const {children[0]}")
        if(self.write_to_file):
            self.file_to_write_to.write(f"\tconst {children[0]}\n")
        return children[0]

    def plus(self, children):
        log.debug(f"Processing 'plus' with {children}")
        log.debug(f"call Int:plus")
        if(self.write_to_file):
            self.file_to_write_to.write(f"\tcall Int:plus\n")
        # Note the token '+' is not one of the children;
        # that's why I told Lark to represent the node as 'plus'
        left, right = children
        return grammar_ast.Plus(left, right)

    def minus(self, children):
        log.debug(f"Processing 'minus' with {children}")
        log.debug(f"call Int:minus")
        if(self.write_to_file):
            self.file_to_write_to.write(f"\tcall Int:minus\n")
        # See 'plus' above.  Same deal.
        left, right = children
        return grammar_ast.Minus(left, right)

    def multiply(self, children):
        log.debug(f"Processing 'multiply' with {children}")
        log.debug(f"call Int:multiply")
        if(self.write_to_file):
            self.file_to_write_to.write(f"\tcall Int:multiply\n")
        # See 'plus' above.  Same deal.
        left, right = children
        return grammar_ast.Multiply(left, right)

    def divide(self, children):
        log.debug(f"Processing 'divide' with {children}")
        log.debug(f"call Int:divide")
        if(self.write_to_file):
            self.file_to_write_to.write(f"\tcall Int:divide\n")
        # See 'plus' above.  Same deal.
        left, right = children
        return grammar_ast.Divide(left, right)

    def sum(self, children):
        """Note we have renamed the recursive cases to 'plus' and 'minus',
        so this method will be called only for a 'sum' node representing
        the base case, sum -> number.
        """
        log.debug(f"Processing sum base case {children}")
        return children[0]

<<<<<<< Updated upstream
=======
    def product(self, children):
        log.debug(f"Processing sum base case {children}")
        return children[0]

>>>>>>> Stashed changes
    def seq_one(self, children):
        """This will always be the first reduction to seq"""
        log.debug(f"Processing sequence (base case) with {children}")
        seq = grammar_ast.Seq()
        seq.append(children[0])
        log.debug(f"Sequence is now {seq}")
        return seq

    def seq_more(self, children):
        """This left-recursive production will always be reduced AFTER
        the base case has been reduced.
        """
        log.debug(f"Processing seq (recursive case) with {children}")
        seq, sum = children
        seq.append(sum)
        return seq