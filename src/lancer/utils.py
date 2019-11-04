from io import BytesIO
from functools import wraps
from pathlib import Path
from tokenize import tokenize, untokenize


def fix_wrapper(fix_method):
    """Wraps a method that fixes the tokens, so that we can pass a
    file to it and it will fix the tokens and create a fixed file.

    [description]

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

        # check if input file is a python file or a lanced python file
        if self.FILE_PATH.suffix not in [".py", ".lanced"]:
            raise ValueError("File needs to be .py or .lanced")

        # (temporary) output file
        out_file = (path.parent / path.name).with_suffix(".lanced")

        # creating it if it does not exist
        out_file.touch()

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
        result = untokenize(result_tokens).decode("utf-8")

        # print resulting script to out_file
        with open(out_file, "w") as out_file:
            print(result, file=out_file, end="")

    return wrapper
