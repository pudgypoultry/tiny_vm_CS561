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


    def NUMBER(self, data):
        """Terminal symbol, a regular expression in the grammar"""
        log.debug(f"Processing token NUMBER with {data}")
        val = int(data.value)
        ast_node = grammar_ast.Number(val)
        log.debug(f"Processed token into value {ast_node}")
        return ast_node


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


