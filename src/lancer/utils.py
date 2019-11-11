from io import BytesIO
from functools import wraps
from pathlib import Path
from tokenize import tokenize, untokenize
import sys
import logging
from collections import deque
from keyword import iskeyword
from shutil import copy2 as copy


__author__ = "Levi Borodenko"
__copyright__ = "Levi Borodenko"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


# setting up logger format and default log level
setup_logging(logging.INFO)


def fix_wrapper(fix_method):
    """Wraps a method that fixes the tokens, so that we can pass a
    file to it and it will fix the tokens and create a fixed file.

    [description]

    TODO:
        - Add attribute to self pointing to output
    Arguments:
        fix_funct {method} -- the method that takes tokens and returns
        fixed tokens.
    """
    @wraps(fix_method)
    def wrapper(self=None, in_file: Path="./file.py"):

        # File to be fixed
        path = Path(in_file)
        self.FILE_PATH = Path(in_file)

        # Saving file name
        self.FILE_NAME = Path(in_file).stem

        # check if input file is a python file or lanced python file
        if self.FILE_PATH.suffix not in [".py", ".lanced"]:
            raise ValueError("File needs to be .py or .lanced")

        # (temporary) output file
        out_file = (path.parent / path.name).with_suffix(".lanced")

        with open(in_file, "r") as file:

            # get file content as string
            in_file_str = file.read()

        # convert to callable object for tokenize
        in_file_bytes = BytesIO(in_file_str.encode('utf-8')).readline

        # Tokenize the script
        tokens = tokenize(in_file_bytes)

        # pass tokens to the method that we wrap
        result_tokens = fix_method(self, tokens)

        # converting back to string
        result = untokenize(result_tokens).decode('utf-8')

        # print resulting script to out_file
        with open(out_file, "w+") as file:
            print(result, file=file, end="")

        # add pointer to outfile to self.
        self.__output__ = out_file

    return wrapper


def window(seq: iter, n: int=2):
    """[summary]

    [description]

    Arguments:
        seq {iter} --  Sequence to iterate over

    Keyword Arguments:
        n {int} -- Size of sliding window (default: {2})

    Yields:
        [type] -- [description]
    """
    it = iter(seq)
    win = deque((next(it, None) for _ in range(n)), maxlen=n)
    yield list(win)
    append = win.append
    for e in it:
        append(e)
        yield list(win)


def isbuildin(name: str) -> bool:
    """[summary]
    Checks if name is a keyword or build-in function
    [description]

    Arguments:
        name {str} -- name to be checked

    Returns:
        bool -- true if it is a build-in
    """

    blacklist = ["abs", "delattr", "hash", "memoryview", "set", "all", "dict",
                 "help", "min", "setattr", "any", "dir", "hex", "next",
                 "slice", "ascii", "divmod", "id", "object", "sorted",
                 "bin", "enumerate", "input", "oct", "staticmethod",
                 "bool", "eval", "int", "open", "str", "breakpoint", "exec",
                 "isinstance", "ord", "sum", "bytearray", "filter",
                 "issubclass", "pow", "super", "bytes", "float", "iter",
                 "print", "tuple", "callable", "format", "len",
                 "property", "type", "chr", "frozenset", "list",
                 "range", "vars", "classmethod", "getattr", "locals",
                 "repr", "zip", "compile", "globals", "map", "reversed",
                 "__import__", "complex", "hasattr", "max", "round", "self"]

    if name in blacklist or iskeyword(name):
        return True
    else:
        return False

def copy_and_delete(in_file:Path, out_file:Path):
    """[summary]
    Copies the contents of in_file into out_file
    then deletes in_file if it is different from out_file.
    
    Arguments:
        in_file {Path} -- File to be copied from and then deleted
        out_file {Path} -- File to create and copy in_file into.
    """

    # turn to Path instances if not already.
    in_file, out_file = Path(in_file), Path(out_file)

    # copy in_file into out_file
    copy(in_file, out_file)

    # delete in_file if it is not the same as outfile
    if in_file != out_file:
        in_file.unlink()
        _logger.debug(f"Overwriting {in_file} with {out_file}. Good luck.")
