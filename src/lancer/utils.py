from io import BytesIO
from functools import wraps
from pathlib import Path
from tokenize import tokenize, untokenize
import sys
import logging
from collections import deque


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
setup_logging(logging.DEBUG)


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

        _logger.info(f"Applyig {self.__name__} to {path}")

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
        result = untokenize(result_tokens)

        # print resulting script to out_file
        with open(out_file, "w+") as file:
            print(result, file=file, end="")

        _logger.debug(f"In: {path} ~ Fix: {self.__name__} ~ Out: {out_file}")

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
