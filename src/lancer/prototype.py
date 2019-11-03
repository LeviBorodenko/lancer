from lancer.skeleton import setup_logging
import logging
from pathlib import Path
from tokenize import tokenize, untokenize, COMMENT
from random import randint
from io import BytesIO

__author__ = "Levi Borodenko"
__copyright__ = "Levi Borodenko"
__license__ = "mit"

# setting up logger instance
_logger = logging.getLogger(__name__)

# setting up logger format and default log level
setup_logging(logging.DEBUG)


class ProtoCommentFixer(object):
    """docstring for ProtoCommentFixer"""

    def __init__(self):
        super(ProtoCommentFixer, self).__init__()

        # Path to lyric file
        self.LYRIC_FILE = Path("./data/lyrics.txt")

        # Number of lyrics
        self.NUM_LYRICS = sum(1 for line in open(self.LYRIC_FILE))

    def _get_lyric(self) -> str:
        """Returns a random song lyric.

        [description]
        """

        # Open lyrics file and grab a random line
        with open(self.LYRIC_FILE) as f:

            random_index = randint(0, self.NUM_LYRICS)

            lyrics = f.readlines()

            # .rstrip to remove trailing whitespace
            return "# " + lyrics[random_index].rstrip()

    def _fix_file(self, file):
        """Takes a file from the script and substitutes comments

        We make use of the tokenize module to substitute comments.

        Arguments:
            file {str} -- line from python script.
        """

        result = []

        # get file content as string
        file_str = file.read()

        # convert to callable object for tokenize
        file_bytes = BytesIO(file_str.encode('utf-8')).readline

        # first we tokenize the string
        tokens = tokenize(file_bytes)

        # iterating over tokens
        for token_type, token_val, _, _, _, in tokens:

            if token_type == COMMENT:
                result.append(
                    (COMMENT, self._get_lyric())
                )

            else:
                result.append((token_type, token_val))

        # converting back to string
        result = untokenize(result).decode("utf-8")

        return result

    def fix(self, in_file: Path):
        """Changes all comments in given in_file to random lyrics

        We make use of the tokenize module to substitute comments.

        Arguments:
            in_file {Path} -- Path to python script that should be fixed


        Raises:
            ValueError -- if input file is not a .py or .lanced file
        """

        # File to be fixed
        path = Path(in_file)
        self.FILE_PATH = Path(in_file)

        # Getting file name
        self.FILE_NAME = Path(in_file).stem

        # check if input file is a python file or a lanced python file
        if self.FILE_PATH.suffix not in [".py", ".lanced"]:
            raise ValueError("File needs to be .py or .lanced")

        # (temporary) output file
        out_file = (path.parent / path.name).with_suffix(".lanced")

        # creating it if it does not exist
        out_file.touch()

        with open(self.FILE_PATH, "r") as in_f, open(out_file, "w") as out_f:

            # iterating over file and substituting all comments with lyrics
            result = self._fix_file(in_f)
            print(result, file=out_f, end="")


if __name__ == '__main__':
    a = ProtoCommentFixer()
    a.fix("./test.py")
