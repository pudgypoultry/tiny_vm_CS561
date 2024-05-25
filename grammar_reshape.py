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

<<<<<<< Updated upstream
class SumsTransformer(lark.Transformer):
=======
class QuackTransformer(lark.Transformer):
>>>>>>> Stashed changes
    """We write a transformer for each node in the parse tree
    (concrete syntax) by writing a method with the same name.
    Non-terminal symbols are passed a list of their children
    after transformation, which proceeds from leaves to root
    recursively. Terminal symbols (like NUMBER) are instead
    passed a lark.Token structure.
    """

    def __init__(self, write_to_file: bool, file_name: str):
<<<<<<< Updated upstream
        self.write_to_file = write_to_file
        self.file_name = file_name
        self.file_to_write_to = "lol"
        self.variables = {}
        if(self.write_to_file):
            self.file_to_write_to = open(f"unit_tests/{file_name}.asm", "w")
            self.file_to_write_to.write(f".class {file_name}:Obj\n.method $constructor\n")
            self.file_to_write_to.close()
            self.file_to_write_to = open(f"unit_tests/{file_name}.asm", "a")
=======
        self.buffer = [""]
        self.file_name = file_name
        self.variables = {}
        self.buffer[0] += f".class {file_name}:Obj\n.method $constructor\n"
>>>>>>> Stashed changes


    def NUMBER(self, data):
        """Terminal symbol, a regular expression in the grammar"""
        log.debug(f"Processing token NUMBER with {data}")
        val = int(data.value)
        ast_node = grammar_ast.Number(val)
        log.debug(f"Processed token into value {ast_node}")
        return ast_node

<<<<<<< Updated upstream
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

    def assign(self, children):
        log.debug(f"Processing 'assign' with {children}")
        log.debug(f"Assigning variable")
        #if(self.write_to_file):
            #self.file_to_write_to.write(f"\tcall Int:plus\n\tpop\n")
        # Note the token '+' is not one of the children;
        # that's why I told Lark to represent the node as 'plus'
        self.variables[children[0]] = children[1]
        left, right = children
        return grammar_ast.Assign(left, right)

    # Arithmetic operations that are translated to method calls
    def plus(self, e):
        log.debug("-> plus")
        left, right = e
        return ast.MethodCallNode("PLUS", left, [ right ])

    # Arithmetic operations that are translated to method calls
    def minus(self, e):
        log.debug("-> minus")
        left, right = e
        return ast.MethodCallNode("MINUS", left, [ right ])

    # Arithmetic operations that are translated to method calls
    def multiply(self, e):
        log.debug("-> multiply")
        left, right = e
        return ast.MethodCallNode("MULTIPLY", left, [ right ])

    # Arithmetic operations that are translated to method calls
    def divide(self, e):
        log.debug("-> divide")
        left, right = e
        return ast.MethodCallNode("DIVIDE", left, [ right ])

    def sum(self, children):
        """Note we have renamed the recursive cases to 'plus' and 'minus',
        so this method will be called only for a 'sum' node representing
        the base case, sum -> number.
        """
        log.debug(f"Processing sum base case {children}")
        return children[0]

    def product(self, children):
        log.debug(f"Processing product base case {children}")
        return children[0]

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
=======

    def program(self, e):
        log.debug("->program")
        classes, main_block = e
        return ProgramNode(classes, main_block)

    def classes(self, e):
        return e

    def clazz(self, e):
        log.debug("->clazz")
        name, formals, super, methods, constructor = e
        return ClassNode(name, formals, super, methods, constructor)

    def methods(self, e):
        return e

    def method(self, e):
        log.debug("->method")
        name, formals, returns, body = e
        return MethodNode(name, formals, returns, body)

    def returns(self, e):
        if not e:
            return "Nothing"
        return e

    def formals(self, e):
        if e[0] is None:
            return []
        return e


    def formal(self, e):
        log.debug("->formal")
        var_name, var_type = e
        return FormalNode(var_name, var_type)


    def expr(self, e):
        log.debug("->expr")
        return ExpressionNode(e[0])


    def ident(self, e):
        """A terminal symbol """
        log.debug("->ident")
        return e[0]


    def variable_ref(self, e):
        """A reference to a variable"""
        log.debug("->variable_ref")
        return VariableRefNode(e[0])


    def block(self, e) -> grammar_ast.ASTNode:
        log.debug("->block")
        stmts = e
        return BlockNode(stmts)


    def assignment(self, e) -> grammar_ast.ASTNode:
        log.debug("->assignment")
        # Structure of e is [Token('BLAH','blah')]
        blah = str(e[0])
        return AssignmentNode(blah)


    def ifstmt(self, e) -> grammar_ast.ASTNode:
        log.debug("->ifstmt")
        cond, thenpart, elsepart = e
        return IfStmtNode(cond, thenpart, elsepart)


    def otherwise(self, e) -> grammar_ast.ASTNode:
        log.debug("->otherwise")
        return e


    def elseblock(self, e) -> grammar_ast.ASTNode:
        log.debug("->elseblock")
        return e[0]  # Unwrap one level of block


    def cond(self, e) -> grammar_ast.ASTNode:
        log.debug("->cond")
        return e


    def plus(self, e):
        log.debug("-> plus")
        left, right = e
        return grammar_ast.MethodNode("PLUS", left, [ right ])


    def minus(self, e):
        log.debug("-> minus")
        left, right = e
        return grammar_ast.MethodNode("MINUS", left, [ right ])


    def multiply(self, e):
        log.debug("-> multiply")
        left, right = e
        return grammar_ast.MethodNode("MULTIPLY", left, [ right ])


    def divide(self, e):
        log.debug("-> divide")
        left, right = e
        return grammar_ast.MethodNode("DIVIDE", left, [ right ])


    def boolean_and(self, e):
        log.debug("-> and")
        left, right = e
        return grammar_ast.MethodNode("BOOLEAN_AND", left, [ right ])


    def boolean_or(self, e):
        log.debug("-> or")
        left, right = e
        return grammar_ast.MethodNode("BOOLEAN_OR", left, [ right ])


    def boolean_not(self, e):
        log.debug("-> not")
        left, right = e
        return grammar_ast.MethodNode("BOOLEAN_NOT", left, [ right ])


    def times_negative_one(self, e):
        log.debg(" -> -1 *")
        right = e
        return grammar_ast.MethodNode("MULTIPLY", -1, [ right ])


>>>>>>> Stashed changes
