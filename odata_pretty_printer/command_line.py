import logging
import argparse
import asyncio

from .odata_tools import pretty_print


logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(asctime)s.%(msecs)03d %(module)10s/%(lineno)-5d %(message)s'
)

logger = logging.getLogger()

def command_line():
    """Provides a command line interface for pretty printer
    """
    parser = argparse.ArgumentParser(description='OData filter pretty printer')
    group_ex = parser.add_mutually_exclusive_group()

    group_ex.add_argument("filter", nargs='?', help='odata filter')
    group_ex.add_argument("--file", "-f", type=argparse.FileType('r', encoding='UTF-8'), help='filter file')

    args = parser.parse_args()

    try:

        if args.file:
            filter = args.file.read()
            result = pretty_print(filter)
            print(result)

        elif args.filter:
            result = pretty_print(args.filter)
            print(result)


    except KeyboardInterrupt:
        pass
    except Exception as ex:
        print(ex)
