## odata-pretty-printer

Pretty printer for OData filter expressions. 

This is an example of using [oppen-pretty-print] to create a pretty-printer for 
OData filter expressions.

This is not a robust program, just a bench tool that's used occasionally to pretty-print
complex OData filters that would otherwise be unreadable. The input filter is expected to be 
grammatically correct, just untidy. Pretty error reporting is non-existent!

### Usage

	pip install odata-pretty-printer

    odata-printer  "ShowOnSite eq true and PublicationDate le 2020-04-29T08:49:33Z \
                    and PublicationDate ge 2019-04-29T08:49:33Z and ChannelId eq 23 \
                    and (ExpiryDate eq null or ExpiryDate ge 2020-04-29T08:49:33Z) and \
                    IsAdvisor eq true and (FundCodeList/any(fundcode: fundcode eq 'ITSMT') \
                    or SectorCodeList/any(sectorcode: sectorcode eq 'T:IG') \
                    or GroupCodeList/any(groupcode: groupcode eq 'BAIL'))"

    odata-printer -f tmp/filter_example.txt  

Output:
```
ShowOnSite eq true
  and PublicationDate le 2020-04-29T08:49:33Z
  and PublicationDate ge 2019-04-29T08:49:33Z
  and ChannelId eq 23
  and (ExpiryDate eq null or ExpiryDate ge 2020-04-29T08:49:33Z)
  and IsAdvisor eq true
  and (FundCodeList/any(fundcode: fundcode eq 'ITSMT')
        or SectorCodeList/any(sectorcode: sectorcode eq 'T:IG')
        or GroupCodeList/any(groupcode: groupcode eq 'BAIL'))
```

### overview

The printer uses the ODATA grammar from Microsoft's [Search Query OData Syntax Reference] to 
create a [Lark] based OData parser. 

Filter input is pretty-printed as follows: 

* The Lark parser creates an AST from the user input.

* The AST is traversed by a tree-visitor that emits [oppen-pretty-print] tokens. 

* The tokens are pretty-printed using the [oppen-pretty-print] printer algorithm.

Providing you have the EBNF grammar I found this to be a quick way to implement a 
pretty-printer. The OData filter pretty-printer presented here is just 56 lines
of code.

### Development

    pip install -r requirements.txt
    pytest

publish:

    invoke publish 0.1.1

**Links**

* [Search Query OData Syntax Reference]
* [Lark]
* [oppen-pretty-print]


[Search Query OData Syntax Reference]:https://docs.microsoft.com/en-us/azure/search/search-query-odata-syntax-reference
[Lark]: https://github.com/lark-parser/lark
[oppen-pretty-print]: https://github.com/stevej2608/oppen-pretty-printer/blob/master/README.md 
