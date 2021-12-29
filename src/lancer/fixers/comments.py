import logging
from tokenize import COMMENT
from random import randint
from lancer.utils import fix_wrapper
import pkg_resources

__author__ = "Levi Borodenko"
__copyright__ = "Levi Borodenko"
__license__ = "mit"

# setting up logger instance
_logger = logging.getLogger(__name__)


class CommentFixer(object):
    """[summary]
    Turns all comments in a file into Pitbull song lyrics.

    [description]
    Iterates over all tokens, substituting the "COMMENT"
    ones with its own.

    Methods:
        fix(file) - takes file and returns the fixed "file.lanced"
    """

    def __init__(self):
        super(CommentFixer, self).__init__()

        # Path to lyric file resource
        self.LYRIC_FILE = pkg_resources.resource_filename(
            __name__, "../resources/lyrics.txt")

        # Load lyrics which replace original comments here
        self.LYRICS = None
        with open(self.LYRIC_FILE, 'r') as f:
            self.LYRICS = f.readlines()

        # Number of lyrics
        self.NUM_LYRICS = len(self.LYRICS)

        # setting name
        self.__name__ = "CommentFixer"

    def _get_lyric(self) -> str:
        """Returns a random song lyric.

        Gives one of many insightful Pitbull quotes.
        """

        # Grab a random line from our lyrics
        random_index = randint(0, self.NUM_LYRICS - 1)

        # .rstrip to remove trailing whitespace
        return "# " + self.LYRICS[random_index].rstrip()

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
