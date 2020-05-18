from lark import Lark
from lark.visitors import Visitor_Recursive

from oppen_pretty_printer.pretty_oppen import pprint, Begin, String, Break, End, Eof, BreakType

odata_parse = Lark.open("odata_pretty_printer/odata.lark")

def block(content):
    return [Begin(breakType=BreakType.consistent)] + content + [End()]

class PrettyPrint(Visitor_Recursive):
    def __init__(self, debug=False):
        self.result = ""
        self.stack = []
        self.debug = debug

    def variable(self, tree):
        tok = String(f'{tree.children[0]}')
        self.stack.append([tok])

    def constant(self, tree):
        tok = String(f'{tree.children[0]}')
        self.stack.append([tok])

    # comparison_expression: variable_or_function COMPARISON_OPERATOR constant
    #     | constant COMPARISON_OPERATOR variable_or_function

    def comparison_expression(self, tree):
        right = self.stack.pop()
        left = self.stack.pop()
        COMPARISON_OPERATOR = String(f' {tree.children[1]} ')
        exp = block(left + [COMPARISON_OPERATOR] + right)
        self.stack.append(exp)

    # logical_expression: boolean_expression AND_OR boolean_expression
    #     | NOT boolean_expression

    def logical_expression(self, tree):
        right = self.stack.pop()
        left = self.stack.pop()
        AND_OR = String(f'{tree.children[1]} ')
        exp = left + [Break(), AND_OR] + right
        self.stack.append(exp)

    # "(" boolean_expression ")" -> parentheses_expression

    def parentheses_expression(self, tree):
        exp = self.stack.pop()
        exp = block([String('('), *exp, String(')')])
        self.stack.append(exp)

    # field_path: IDENTIFIER ("/" IDENTIFIER)*

    def field_path(self, tree):
        path = "/".join([str(child) for child in tree.children])
        self.stack.append([Break(blankSpace=0), String(path)])

    # lambda_expression: IDENTIFIER ":" boolean_expression

    def lambda_expression(self, tree):
        right = self.stack.pop()
        identifier = String(tree.children[0] + ': ')
        exp = block([identifier] + right)
        self.stack.append(exp)

    # collection_filter_expression: field_path ANY_OR_ALL lambda_expression? ")"

    def collection_filter_expression(self, tree):
        right = self.stack.pop() if len(tree.children) == 3 else []
        left = self.stack.pop()
        ANY_OR_ALL = String(tree.children[1])

        exp = block(left + [ANY_OR_ALL] + right + [String(')')])
        self.stack.append(exp)

    def print(self, tree):
        self.visit(tree)
        result = [Begin(breakType=BreakType.consistent), *self.stack.pop(), End(), Eof()]
        return pprint(result)


def pretty_print(filter):
    parse_tree = odata_parse.parse(filter)
    printer = PrettyPrint()
    result = printer.print(parse_tree)
    return result
