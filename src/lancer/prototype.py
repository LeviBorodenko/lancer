from lancer.skeleton import setup_logging
import logging
from pathlib import Path
from tokenize import tokenize, untokenize, COMMENT
from random import randint

__author__ = "Levi Borodenko"
__copyright__ = "Levi Borodenko"
__license__ = "mit"

# setting up logger instance
_logger = logging.getLogger(__name__)

# setting up logger format and default log level
setup_logging(logging.DEBUG)


class ProtoCommentFixer(object):
    """docstring for ProtoCommentFixer"""

    def __init__(self, file: Path = Path("./")):
        super(ProtoCommentFixer, self).__init__()

        # File to be fixed
        self.FILE_PATH = Path(file)

        # Path to lyric file
        self.LYRIC_FILE = Path("./data/lyrics.txt")

        # Number of lyrics
        self.NUM_LYRICS = sum(1 for line in open(self.LYRIC_FILE))

        # check if file is a python file
        if self.FILE_PATH.suffix != ".py":
            raise ValueError("File needs to be .py")

    def get_lyric(self) -> str:
        """Returns a random song lyric.

        [description]
        """

        # Open lyrics file and grab a random line
        with open(self.LYRIC_FILE) as f:

            random_index = randint(0, self.NUM_LYRICS)

            lyrics = f.readlines()

            # .rstrip to remove trailing whitespace
            return lyrics[random_index].rstrip()


if __name__ == '__main__':
    a = ProtoCommentFixer("test.py")
    print(a.get_lyric())
