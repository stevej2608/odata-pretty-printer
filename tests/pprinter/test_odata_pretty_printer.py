from  odata_pretty_printer.odata_tools import pretty_print


def make_result(text):
    """Template for the "result = (...)" value generator

    Arguments:
        text {str} -- The output from the pretty printer

    Returns:
        str -- Formatted result ready to be pasted into the test

    Example:

        print(make_result(output))

    prints:

    result = (
        "ShowOnSite eq true\n"
        "  and PublicationDate le 2020-04-29T08:49:33Z\n"
        "  and PublicationDate ge 2019-04-29T08:49:33Z\n"
        "  and ChannelId eq 23\n"
        "  and (ExpiryDate eq null or ExpiryDate ge 2020-04-29T08:49:33Z)\n"
        "  and IsAdvisor eq true\n"
        "  and (FundCodeList/any(fundcode: fundcode eq 'ITSMT')\n"
        "        or SectorCodeList/any(sectorcode: sectorcode eq 'T:IG')\n"
        "        or GroupCodeList/any(groupcode: groupcode eq 'BAIL'))"
    )

    """
    lines = text.split('\n')
    lines = '\\n"\n        "'.join(lines)
    lines = f'    result = (\n        "{lines}"\n    )\n'
    return lines

# Throw OData expressions at pretty_print and confirm reverse parsed result
# that maches the input is returned.

def test_simple():
    filter = "ShowOnSite eq true and (ExpiryDate eq null or ExpiryDate ge 2020-04-29T08:49:33Z)"
    output = pretty_print(filter)

    make_result(output)
    assert output == 'ShowOnSite eq true\n  and (ExpiryDate eq null or ExpiryDate ge 2020-04-29T08:49:33Z)'


def test_collection_filter_expression():
    filter = "SectorCodeList/any(sectorcode: sectorcode eq 'T:IG')"
    output = pretty_print(filter)
    assert output == filter


def test_example1():
    filter = (
        "ShowOnSite eq true "
        "and PublicationDate le 2020-04-29T08:49:33Z "
        "and PublicationDate ge 2019-04-29T08:49:33Z "
        "and ChannelId eq 23 "
        "and (ExpiryDate eq null "
        "or ExpiryDate ge 2020-04-29T08:49:33Z"
        ") "
        "and IsAdvisor eq true "
        "and (FundCodeList/any(fundcode: fundcode eq 'ITSMT') "
        "or SectorCodeList/any(sectorcode: sectorcode eq 'T:IG') "
        "or GroupCodeList/any(groupcode: groupcode eq 'BAIL')"
        ")"
    )

    result = (
        "ShowOnSite eq true\n"
        "  and PublicationDate le 2020-04-29T08:49:33Z\n"
        "  and PublicationDate ge 2019-04-29T08:49:33Z\n"
        "  and ChannelId eq 23\n"
        "  and (ExpiryDate eq null or ExpiryDate ge 2020-04-29T08:49:33Z)\n"
        "  and IsAdvisor eq true\n"
        "  and (FundCodeList/any(fundcode: fundcode eq 'ITSMT')\n"
        "        or SectorCodeList/any(sectorcode: sectorcode eq 'T:IG')\n"
        "        or GroupCodeList/any(groupcode: groupcode eq 'BAIL'))"
    )

    output = pretty_print(filter)
    assert output == result


def test_example2():
    filter = """
            (IsTrustnetUnit eq true and IsTrustnetFund eq true)
                and Category ne 'AIP'
                and Category ne 'NIP'
                and Category ne 'RIP'
                and Category ne 'COP'
                and Currency ne 'CPS'
                and UniverseCodeList/any(u: u eq 'T')
    """

    result = (
        "(IsTrustnetUnit eq true and IsTrustnetFund eq true)\n"
        "  and Category ne 'AIP'\n"
        "  and Category ne 'NIP'\n"
        "  and Category ne 'RIP'\n"
        "  and Category ne 'COP'\n"
        "  and Currency ne 'CPS'\n"
        "  and UniverseCodeList/any(u: u eq 'T')"       
    )

    output = pretty_print(filter)
    assert output == result


def test_example3():
    filter = """
        (IsTrustnetUnit eq true and IsTrustnetFund eq true)
        and Category ne 'AIP'
        and Category ne 'NIP'
        or (Category ne 'RIP' and Category ne 'COP' and Currency ne 'CPS')
        and UniverseCodeList/any(u: u eq 'T')
    """

    result = (
        "(IsTrustnetUnit eq true and IsTrustnetFund eq true)\n"
        "  and Category ne 'AIP'\n"
        "  and Category ne 'NIP'\n"
        "  or (Category ne 'RIP' and Category ne 'COP' and Currency ne 'CPS')\n"
        "  and UniverseCodeList/any(u: u eq 'T')"
    )

    output = pretty_print(filter)
    assert output == result
