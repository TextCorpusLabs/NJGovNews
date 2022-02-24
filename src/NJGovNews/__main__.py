
import pathlib
import sys
from .__init__ import __version__
from .site import treasury
from argparse import ArgumentParser
from typeguard import typechecked

@typechecked
def main() -> None:
    parser = ArgumentParser(prog = 'NJGovNews', description = "Scrape the news feed from the New Jersey government")
    subparsers = parser.add_subparsers(required = True, help = 'sub-commands')
    treasury_parser(subparsers.add_parser('treasury', help = 'Department of the Treasury'))
    args = parser.parse_args()
    print(f'NJGovNews v{__version__}')
    args.function(args.file_out)

@typechecked
def treasury_parser(parser: ArgumentParser) -> None:
    parser.add_argument('-out', dest = 'file_out', type = pathlib.Path, required = True, help = 'File to store the results')
    parser.set_defaults(function = treasury)

if __name__ == "__main__":
    sys.exit(main())
