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
	
## Documentation

Head over to the [*README*][homepage] for more details.

## Contributing

The source code for *odata-pretty-printer* is available
[on GitHub][repo]. If you find a bug or something is unclear, we encourage
you to raise an issue. We also welcome contributions, to contribute, fork the
repository and open a [pull request][pulls].

[repo]: https://github.com/stevej2608/odata-pretty-printer
[homepage]: https://github.com/stevej2608/odata-pretty-printer/blob/master/README.md
[pulls]: https://github.com/stevej2608/odata-pretty-printer/pulls
[oppen-pretty-print]: https://github.com/stevej2608/oppen-pretty-printer/blob/master/README.md 
