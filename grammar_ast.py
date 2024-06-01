"""Abstract syntax representation of a sequence of sums."""

import logging
from typing import Callable
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

LB = "{"
RB = "}"

class ASTNode:
    """Abstract base class"""
    def __init__(self):
        self.children = []    # Internal nodes should set this to list of child nodes

    # Visitor-like functionality for walking over the AST. Define default methods in ASTNode
    # and specific overrides in node types in which the visitor should do something
    def walk(self, visit_state, pre_visit: Callable, post_visit: Callable):
        pre_visit(self, visit_state)
        for child in flatten(self.children):
            log.debug(f"Visiting ASTNode of class {child.__class__.__name__}")
            try:
                child.walk(visit_state, pre_visit, post_visit)
            except Exception as e:
                log.error(f"Failed walking {self.__class__.__name__} to  {child.__class__.__name__}")
        post_visit(self, visit_state)

    # Example walk to gather method signatures
    def method_table_visit(self, visit_state: dict):
        ignore(self, visit_state)

    # def ignore():
    #     pass

    def r_eval(self, buffer: list[str]):
        """Evaluate for value, i.e., generate
        code that will result in evaluating an
        expression of some kind for a value.
        Always increases stack
        depth by 1.  Implement for every node that can be
        evaluated to create a value on the stack.

        Assign will leave me with a net increase of zero
        Leaf nodes must move back up the tree
        """
        raise NotImplementedError(f"r_eval not implemented for node type {self.__class__.__name__}")

    def c_eval(self, true_branch: str, false_branch: str, buffer: list[str]):
        raise NotImplementedError(f"c_eval not implemented for node type {self.__class__.__name__}")

    def gen_code(self, buffer: list[str]):
        """Gen code should be implemented for program, class,
        method, block, and each kind of statement.
        These methods generally do not change the depth of the stack.
        """
        raise NotImplementedError(f"No gen_code method for class {self.__class__.__name__}")

    # Leaving this untouched, useful for graphing
    ### Visualization ###
    def dot_id(self) -> str:
        """Python's built-in "id" function let's us create unique node IDs"""
        return f"node_{id(self)}"

    def dot_label(self) -> str:
        """By default, we use the class as a node label.
        Override to place other attributes within the node.
        """
        return self.__class__.__name__

    def to_dot(self, buffer: list[str]):
        """Add relevant dot code to this node"""
        this_node = self.dot_id()
        buffer.append(f'{this_node}[label="{LB}{self.dot_label()}{RB}"]')
        for child in flatten(self.children):
            buffer.append(f"{this_node} -> {child.dot_id()};")
            child.to_dot(buffer)


class ProgramNode(ASTNode):

    def __init__(self, classes: list[ASTNode], main_block: ASTNode):
        super().__init__()
        self.classes = classes
        main_class = ClassNode("$Main", [], "Obj", [], main_block)
        self.classes.append(main_class)
        self.children = self.classes

    def __str__(self) -> str:
        return "\n".join([str(c) for c in self.classes])

    def gen_code(self, buffer: list[str]):
        for clazz in self.classes:
            clazz.gen_code(buffer)


class ClassNode(ASTNode):

    def __init__(self, name: str, formals: list[ASTNode],
                 super_class: str,
                 methods: list[ASTNode],
                 block: ASTNode):
        self.name = name
        self.super_class = super_class
        self.methods = methods
        self.constructor = MethodNode("$constructor", formals, name, block)
        self.children = methods +  [self.constructor]

    def __str__(self):
        formals_str = ", ".join([str(fm) for fm in self.constructor.formals])
        methods_str = "\n".join([f"{method}\n" for method in self.methods])
        return f"""
        class {self.name}({formals_str}){LB}
        {methods_str}
        /* statements as a constructor */
        {self.constructor}
        {RB} /* end class {self.name} */
        """

    # Example walk to gather method signatures
    def method_table_visit(self, visit_state: dict):
        """Create class entry in symbol table (as a preorder visit)"""
        if self.name in visit_state:
            raise Exception(f"Shadowing class {self.name} is not permitted")
        visit_state["current_class"] = self.name
        visit_state[self.name] = {
            "super": self.super_class,
            "fields": [],
            "methods": {}
        }


class BlockNode(ASTNode):

    def __init__(self, stmts: list[ASTNode]):
        self.stmts = stmts
        self.children = stmts

    def __str__(self):
        return "".join([str(stmt) + ";\n" for stmt in self.stmts])


class FormalNode(ASTNode):
    def __init__(self, var_name: str, var_type: str):
        self.var_name = var_name
        self.var_type = var_type
        self.children = []

    def __str__(self):
        return f"{self.var_name}: {self.var_type}"


class ExprNode(ASTNode):
    """Just identifiers in this stub"""
    def __init__(self, e):
        self.e = e
        self.children = [e]

    def __str__(self):
        return str(self.e)


class IfNode(ASTNode):

    def __init__(self,
                 cond: ASTNode,
                 thenpart: ASTNode,
                 elsepart: ASTNode):
        self.cond = cond
        self.thenpart = thenpart
        self.elsepart = elsepart
        self.children = [cond, thenpart, elsepart]

    def __str__(self):
        return f"""if {self.cond} {LB}\n
                {self.thenpart}
             {RB} else {LB}
                {self.elsepart} {LB}
            {RB}
            """

    def c_eval(self, true_branch: str, false_branch: str, buffer: list[str]):
        """We could be evaluating a comparison or other boolean method
        for control flow.  In that case we generate code as if for value,
        then use it to control the jump.
        """
        self.r_eval(buffer)
        buffer.append(f"\tjump_ifnot {false_branch}")
        buffer.append(f"\tjump {true_branch}")


    def gen_code(self, buffer: list[str]):
        """An If statement generates control flow to
        execute either the `then` or the `else` part.
        """
        thenpart_label = gen_label("then")
        elsepart_label = gen_label("else")
        endif_label = gen_label("endif")
        self.cond.c_eval(thenpart_label, elsepart_label, buffer)
        buffer.append(f"{thenpart_label}: ")
        self.thenpart.gen_code(buffer)
        buffer.append(f"\tjump {endif_label}")
        buffer.append(f"{elsepart_label}: ")
        self.elsepart.gen_code(buffer)
        buffer.append(f"{endif_label}: ")


class MethodNode(ASTNode):

    def __init__(self, name: str, arguments: list[ASTNode], return_type: str, block: ASTNode):
        self.name = name 
        self.formals = arguments
        self.return_type = return_type
        self.block = block

    #TODO: Fill out

class MethodCallNode(ASTNode):

    def __init__(self,
                 name: str,
                 receiver: ASTNode,
                 actuals: list[ASTNode]):
        self.name = name
        self.receiver = receiver
        self.actuals = actuals
        self.children = [ self.receiver ] + self.actuals

    def __str__(self):
        actuals = ",".join(str(actual)
                           for actual in self.actuals)
        return f"{self.receiver}.{self.name}({actuals})"

    def dot_label(self) -> str:
        return f"Method Call|{self.name}"

    def r_eval(self, buffer: list[str]):
        for actual in self.actuals:
            actual.r_eval(buffer)
        self.receiver.r_eval(buffer)
        buffer.append(f"call Int:{self.name}")
        # FIXME:  We need to infer type from expression,
        # not just assume it's Int.  To do this, we need to
        # use the inferred type of the receiver object, which
        # could itself be an expression.



class AssignmentNode(ASTNode):
    
    def __init__(self, name_assigning_to: str, expression_assigned: ASTNode):
        self.name_assigning_to = name_assigning_to
        self.expression_assigned = expression_assigned
        self.children = []

    def __str__(self):
        actuals = ",".join(str(actual) for actual in self.actuals)
        return f"{name_assigning_to} = {expression_assigned.__str__()}"

    def gen_code(self, buffer: list[str]):
        buffer.append(f"find out how to assign \"{self.expression_assigned}\" to {self.name}")



class ExpressionNode(ASTNode):
    """Just identifiers in this stub"""
    def __init__(self, e):
        self.e = e
        self.children = [e]

    def __str__(self):
        return str(self.e)


class BareExpressionNode(ASTNode):
    
    def __init__(self, e):
        self.e = e
        self.children = [e]

    def __str__(self):
        return str(self.e)


class ConstNode(ASTNode):
    pass


class VariableReferenceNode(ASTNode):
    """Reference to a variable in an expression.
    This will typically evaluate to a 'load' operation.
    """
    def __init__(self, name: str):
        assert isinstance(name, str)
        self.name = name
        self.children = []

    def __str__(self):
        return self.name


class BooleanConditionNode(ASTNode):
    """Boolean condition. It can evaluate to jumps,
    but in this grammar it's just a placeholder.
    """
    def __init__(self, cond: str):
        self.cond = cond

    def __str__(self):
        return f"{self.cond}"




if __name__ == "__main__":
    pass