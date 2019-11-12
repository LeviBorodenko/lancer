# -*- coding: utf-8 -*-
"""
Then run `python setup.py install` which will install the command `lance`
inside your current environment.
"""

import argparse
import sys
import logging
from pathlib import Path
from lancer.utils import copy_and_delete

from lancer.fixers.comments import CommentFixer
from lancer.fixers.variables import VariableFixer

from lancer import __version__

__author__ = "Levi Borodenko"
__copyright__ = "Levi Borodenko"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Ever heard of Black? This is the opposite.")
    parser.add_argument(
        "--version",
        action="version",
        version="lancer {ver}".format(ver=__version__))
    parser.add_argument(
        "-f",
        "--file",
        dest="file",
        help="Python file to be lance'd.",
        type=Path,
        action="store",
        required=True,
        metavar="./FILE_PATH.py")
    parser.add_argument(
        "-y",
        "--yolo",
        dest="yolo",
        help="Overwrite original file, lol.",
        action="store_true")
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def lance(file : Path = "./file.py", yolo : bool = False):
    """[summary]
    Takes a file and lances it.

    [description]
    Turns our code into the most horrendous mess imaginable.
    Seriously.

    Keyword Arguments:
        file {Path} -- File to be lanced (default: {"./file.py"})
        yolo {bool} -- Overwrites original if true (default: {False})
    """
    # turn file into path if not already
    file = Path(file)

    # initiate "fixers"
    variabel_fixer = VariableFixer()
    comment_fixer = CommentFixer()

    # first fix comments
    comment_fixer.fix(file)

    # get the output file
    fixed_file = comment_fixer.__output__

    # applying variable fixer
    variabel_fixer.fix(fixed_file)

    # if yolo mode is true, substitute original
    if yolo:
        copy_and_delete(fixed_file, file)


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)

    lance(file=args.file, yolo=args.yolo)


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
