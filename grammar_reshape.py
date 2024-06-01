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
#log.setLevel(logging.DEBUG)

class QuackTransformer(lark.Transformer):
    """We write a transformer for each node in the parse tree
    (concrete syntax) by writing a method with the same name.
    Non-terminal symbols are passed a list of their children
    after transformation, which proceeds from leaves to root
    recursively. Terminal symbols (like NUMBER) are instead
    passed a lark.Token structure.
    """

    def __init__(self, write_to_file: bool, file_name: str):
        self.buffer = [""]
        self.file_name = file_name
        self.variables = {}
        self.buffer[0] += f".class {file_name}:Obj\n.method $constructor\n"

    def Number(self, data):
        #Terminal symbol, a regular expression in the grammar
        log.debug(f"Processing token NUMBER with {data}")
        val = int(data.value)
        ast_node = grammar_ast.Number(val)
        log.debug(f"Processed token into value {ast_node}")
        return ast_node

    def program(self, e):
        log.debug("-> program")
        # log.debug(f"---{len(e)}")
        # log.debug(f"---{e}")
        # for i in range(len(e)):
        #     log.debug(f"\n\n-----{e[i]}")

        classes = []
        main_block = []
        i = 0
        while type(e[i]) == lark.Tree:
            classes.append(e[i])
            i += 1

        while i < len(e):
            main_block.append(e[i])
            i += 1
        

        return grammar_ast.ProgramNode(classes, main_block)

    def classes(self, e):
        return e

    def clazz(self, e):
        log.debug("->clazz")
        name, formals, super, methods, constructor = e
        return grammar_ast.ClassNode(name, formals, super, methods, constructor)

    def methods(self, e):
        return e

    def method(self, e):
        #def __init__(self, name: str, arguments: list[ASTNode], return_type: str, block: ASTNode)
        log.debug("-> method")
        log.debug(f"---{e}")
        log.debug(f"---{len(e)}")
        def_string, name, formals, returns, body = e
        #return grammar_ast.MethodNode(name, formals, returns, body)

    def statement(self, e):
        log.debug("-> statement")
        return e

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
        return grammar_ast.FormalNode(var_name, var_type)


    def expr(self, e):
        log.debug("->expr")
        return grammar_ast.ExpressionNode(e[0])


    def ident(self, e):
        """A terminal symbol """
        log.debug(f"-> ident, name: {e[0]}")
        return e[0]


    def variable_ref(self, e):
        """A reference to a variable"""
        log.debug("->variable_ref")
        return grammar_ast.VariableRefNode(e[0])


    def block(self, e) -> grammar_ast.ASTNode:
        log.debug("->block")
        stmts = e
        return grammar_ast.BlockNode(stmts)


    def assignment(self, e) -> grammar_ast.ASTNode:
        log.debug("->assignment")
        # Structure of e is [Token('BLAH','blah')]
        blah = str(e[0])
        return grammar_ast.AssignmentNode(blah)


    def if_statement(self, e) -> grammar_ast.ASTNode:
        log.debug("->ifstmt")
        cond, thenpart, elsepart = e
        return grammar_ast.IfStmtNode(cond, thenpart, elsepart)


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
        left, operand, right = e
        log.debug(f"-> adding {left} {operand} {right}")
        return grammar_ast.MethodCallNode("PLUS", left, [ right ])


    def minus(self, e):
        log.debug("-> minus")
        left, operand, right = e
        log.debug(f"-> subtracting {left} {operand} {right}")
        return grammar_ast.MethodCallNode("MINUS", left, [ right ])


    def multiply(self, e):
        left, operand, right = e
        log.debug(f"-> multiplying {left} {operand} {right}")
        return grammar_ast.MethodCallNode("MULTIPLY", left, [ right ])


    def divide(self, e):
        left, operand, right = e
        log.debug(f"-> dividing {left} {operand} {right}")
        return grammar_ast.MethodCallNode("DIVIDE", left, [ right ])


    def boolean_and(self, e):
        left, operand, right = e
        log.debug(f"-> and {left} {operand} {right}")
        return grammar_ast.MethodCallNode("BOOLEAN_AND", left, [ right ])


    def boolean_or(self, e):
        left, operand, right = e
        log.debug(f"-> or {left} {operand} {right}")
        return grammar_ast.MethodCallNode("BOOLEAN_OR", left, [ right ])


    def boolean_not(self, e):
        operand, right = e
        log.debug(f"-> not {operand} {right}")
        return grammar_ast.MethodCallNode("BOOLEAN_NOT", [ right ])


    def times_negative_one(self, e):
        operand, right = e
        log.debug(f"-> negating/multiplying -1 {operand} {right}")
        return grammar_ast.MethodCallNode("MULTIPLY", -1, [ right ])


