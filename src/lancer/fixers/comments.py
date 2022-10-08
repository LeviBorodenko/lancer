import logging
from tokenize import COMMENT, NAME, NEWLINE, OP
from typing import List, Sequence, Tuple
from random import randint
from lancer.utils import fix_wrapper, isemptytype, window
import pkg_resources

__author__ = "Levi Borodenko"
__copyright__ = "Levi Borodenko"
__license__ = "mit"


# Tuple of (<token type>, (<token value>)
# These tokens are returned by the fixer, and are suitable for being passed to
# untokenize() to convert back to source code.
LancerTokenType = Tuple[int, str]


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

        # Path to lyric file resources
        self.LYRIC_FILE = pkg_resources.resource_filename(
            __name__, "../resources/lyrics.txt")

        self.SFW_LYRIC_FILE = pkg_resources.resource_filename(
            __name__, "../resources/sfw_lyrics.txt")

        # Generate safe for work content (False by default)
        self.sfw = False

        # Number of lyrics
        self.NUM_LYRICS = sum(1 for line in open(self.LYRIC_FILE))

        # setting name
        self.__name__ = "CommentFixer"

    def _get_lyric(self) -> str:
        """Returns a random song lyric.

        By default, gives one of many insightful Pitbull quotes.
        If self.sfw is True, return lyrics that are safe for work.
        """
        lyric_file = self.SFW_LYRIC_FILE if self.sfw else self.LYRIC_FILE
        # Open lyrics file and grab a random line
        with open(lyric_file) as f:

            random_index = randint(0, self.NUM_LYRICS - 1)

            lyrics = f.readlines()

            # .rstrip to remove trailing whitespace
            return "# " + lyrics[random_index].rstrip()

    def _substitute_comments_for_lyrics(
        self, tokens: Sequence[LancerTokenType]
    ) -> List[LancerTokenType]:
        """
        Substitute any comment tokens in the sequence tokens with random
        lyrics.
    
        Arguments:
            tokens  -- the list of tokens to substitute comments from.
        
        Return:
            out_tokens  -- the new list of tokens after substitution.
        """
        out_tokens: List[LancerTokenType] = []

        for token_type, token_val in tokens:
            if token_type == COMMENT:
                out_tokens.append((COMMENT, self._get_lyric()))
            else:
                out_tokens.append((token_type, token_val))

        return out_tokens

    def _add_pointless_variable_init_comments(
        self, tokens: Sequence[LancerTokenType]
    ) -> List[LancerTokenType]:
        """
        Add totally useless comments describing when variables are initialized.
        E.g.    my_val = 3
            ->
                # Setting value of my_val
                my_val = 3
    
        Arguments:
            tokens  -- the current list of tokens for the source code.
        
        Return:
            out_tokens  -- the new list of tokens after adding pointless
                           comments.
        """
        # Identify initialized variables by looking for the following
        # pattern:
        #     first      NEWLINE        '\n'
        #     middle     NAME           'my_var'
        #     last       OP             '='
        #
        # Obviously this doesn't catch all initialized variables, but it will
        # catch a decent number while keeping things simple.
        out_tokens: List[LancerTokenType] = []

        # Loop over token windows of size 3, inserting a pointless comment
        # if the above pattern is spotted, and adding the middle token to the
        # output list. Note that this means the first & last tokens are added
        # seperately.
        out_tokens.append(tokens[0])

        token_iter = iter(tokens)
        for first, middle, last in window(token_iter, 3):
            if (
                isemptytype(first[0]) and
                middle[0] == NAME and
                last[0] == OP
                and last[1] == "="
            ):
                out_tokens.append(
                    (COMMENT, "# Setting value of {}".format(middle[1]))
                )
                out_tokens.append((NEWLINE, "\n"))

            out_tokens.append(middle)

        out_tokens.append(tokens[-1])

        return out_tokens

    @fix_wrapper
    def fix(self, tokens):
        """After decoration, it will take the file that you want to fix and
        create a fixed .lanced file.

        BEFORE DECORATION: takes a list of tokens and returns
        a list of the fixed tokens.

        Arguments:
            tokens -- the list of tokens from the file

        Returns:
            fixed_tokens - list of tokens, but now with fixed comments
        """

        # Strip off the unneeded token elements.
        stripped_tokens = [(token[0], token[1]) for token in tokens]

        fixed_tokens = self._substitute_comments_for_lyrics(stripped_tokens)

        fixed_tokens = self._add_pointless_variable_init_comments(fixed_tokens)

        return fixed_tokens
