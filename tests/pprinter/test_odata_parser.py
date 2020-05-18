import json
from lark import Lark

odata_parse = Lark.open('odata_pretty_printer/odata.lark')

with open('tests/pprinter/filter_example.json') as json_file:
    example_filters = json.load(json_file)

# Throw OData expressions at the parser and confirm an AST is returned. The
# Lark parser throws an exception if it cannot parse the input.

def test_boolean_expression():
    result = odata_parse.parse("fundcode eq 'ITSMT'", start='boolean_expression')
    assert result


def test_lamda():
    result = odata_parse.parse("fundcode: fundcode eq 'ITSMT'", start='lambda_expression')
    assert result


def test_simple_exp_parse():

    result = odata_parse.parse("name", start='variable_or_function')
    assert result

    result = odata_parse.parse("'test'", start='constant')
    assert result

    result = odata_parse.parse("name eq 'test'", start='comparison_expression')
    assert result


def test_expression_snippets():
    result = odata_parse.parse("name eq 'test of strings'", start='boolean_expression')
    assert result

    result = odata_parse.parse("id gt 5", start='boolean_expression')
    assert result

    result = odata_parse.parse("(id lt 5)", start='boolean_expression')
    assert result

    result = odata_parse.parse("name eq 'ultramarine (R)'", start='boolean_expression')
    assert result

    result = odata_parse.parse("name eq 'ultramarine (R)'", start='boolean_expression')
    assert result


def test_collection_filter_expression():
    result = odata_parse.parse("FundCodeList/any(fundcode: fundcode eq 'ITSMT')", start='collection_filter_expression')
    assert result

    result = odata_parse.parse("UniverseCodeList/any(u: u eq 'T')", start='collection_filter_expression')
    assert result

    result = odata_parse.parse("UniverseCodeList/all(u: u eq 'T')", start='collection_filter_expression')
    assert result

    result = odata_parse.parse("UniverseCodeList/any()", start='collection_filter_expression')
    assert result


def test_filter1():
    for filter in example_filters:
        result = odata_parse.parse(filter)
        assert result
