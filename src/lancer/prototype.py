from lancer.skeleton import setup_logging
import logging
from pathlib import Path
from tokenize import COMMENT
from random import randint
from lancer.utils import fix_wrapper

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
        self.LYRIC_FILE = Path("./resources/lyrics.txt").absolute()

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

    @fix_wrapper
    def fix(self, tokens):
        """After decoration, it will take the file that you want to fix and
        create a fixed .lanced file.

        BEFORE DECORATION: takes a list of tokens and returns
        a list of the fixed tokens.

        Arguments:
            tokens -- the list of tokens from the file

        Returns:
            result - list of tokens, but now with fixed comments
        """

        result = []

        # iterating over tokens
        for token_type, token_val, _, _, _, in tokens:

            # if token is a comment, substitute with a random lyric comment.
            if token_type == COMMENT:
                result.append(
                    (COMMENT, self._get_lyric())
                )

            else:
                result.append((token_type, token_val))
        return result


if __name__ == '__main__':
    a = ProtoCommentFixer()
    a.fix("./test.lanced")
