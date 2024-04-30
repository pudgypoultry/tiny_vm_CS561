"""Abstract syntax representation of a sequence of sums."""

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# class ASTNode:
#     """Abstract base class for abstract sequence of sequence of sums"""
#     def __init__(self):
#         """This is an abstract class and should not be instantiated"""
#         this_class = self.__class__.__name__
#         if this_class == "ASTNode":
#             raise NotImplementedError("ASTNode is an abstract class and should not be instantiated")
#         else:
#             raise NotImplementedError(f"{this_class} is missing a constructor method")


class ASTNode:
    """Abstract base class"""
    def __init__(self):
        self.children = []    # Internal nodes should set this to list of child nodes

    # Visitor-like functionality for walking over the AST. Define default methods in ASTNode
    # and specific overrides in node types in which the visitor should do something
    def walk(self, visit_state, pre_visit: Callable =ignore, post_visit: Callable=ignore):
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

    def r_eval(self, buffer: list[str]):
        """Evaluate for value, i.e., generate
        code that will result in evaluating an
        expression of some kind for a value.
        Always increases stack
        depth by 1.  Implement for every node that can be
        evaluated to create a value on the stack.
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


class Plus(MethodCallNode):
    def __init__(self, name, receiver, actuals):
        super.__init__("+", receiver, actuals)


class Minus(MethodCallNode):
    def __init__(self, name, receiver, actuals):
        super.__init__("-", receiver, actuals)


class Multiply(MethodCallNode):
    def __init__(self, name, receiver, actuals):
        super.__init__("*", receiver, actuals)


class Divide(MethodCallNode):
    def __init__(self, name, receiver, actuals):
        super.__init__("/", receiver, actuals)


class Sum(ASTNode):
    pass

# A sum is either an integer or a binary operation

class Number(Sum):
    """Typically some tokens define leaves of the AST.  Leaves of a Sum
    are integer literals.
    """
    def __init__(self, value: int):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)


class AssignmentNode(ASTNode):
    """Need a way to assign a variable and hold it in memory associated with a value"""
    def __init__(self, lhs, decl_type, rhs):
        self.decl_type = decl_type
        self.lhs = lhs
        self.rhs = rhs
        self.children = [self.rhs]

    def __str__(self):
        if self.decl_type is None:
            return f"{self.lhs} = {self.rhs}"
        else:
            return f"{self.lhs}: {self.decl_type} = {self.rhs}"

    def gen_code(self, buffer: list[str]):
        """Evaluate rhs, store in lhs"""
        buffer += self.rhs.r_eval()
        buffer.append(f"store {self.lhs}")


class Seq(ASTNode):
    """A sequence of sums.  We could represent it in a treelike manner
    to better match a left-recursive grammar, but we'll instead represent it
    as a list of sums to illustrate how we can apply a lark transformer to
    reshape it.
    """
    def __init__(self):
        self.sums: list[Sum] = []

    def append(self, sum: Sum):
        self.sums.append(sum)

    def __str__(self) -> str:
        el_strs = ", ".join(str(e) for e in self.sums)
        return f"[{el_strs}]"

    def __repr__(self):
        return f"seq({repr(self.sums)})"

def smoke_test_sums():
    sum1 = Plus(1, Minus(2, 3))
    sum2 = Minus(2, 1)
    sum3 = Multiply(15, 2)
    seq = Seq()
    seq.append(sum1)
    seq.append(sum2)
    seq.append(sum3)
    print(seq)

if __name__ == "__main__":
    smoke_test_sums()
