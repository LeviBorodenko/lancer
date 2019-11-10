import logging
from tokenize import NAME, NL, DEDENT, INDENT
from itertools import tee
import random
from lancer.utils import fix_wrapper, setup_logging, window, isbuildin

# import pkg_resources

__author__ = "Levi Borodenko"
__copyright__ = "Levi Borodenko"
__license__ = "mit"

# setting up logger instance
_logger = logging.getLogger(__name__)

# setting up logger format and default log level
setup_logging(logging.DEBUG)


class VariableFixer(object):
    """docstring for VariableFixer"""

    def __init__(self):
        super(VariableFixer, self).__init__()

        # setting name
        self.__name__ = "VariableFixer"

        # dictionary containing the patterns to generate the new names
        self.PATTERNS = {1: {"initial": "O", "chars": ["0", "O", "Ο"]},
                         2: {"initial": None, "chars": ["I", "l", "Ι"]},
                         3: {"initial": None, "chars": ["α", "a"]}
                         }

        # initilising dict that will translate the actual variable names
        # to our generated onces.
        self.dict = {}

        # length of variable names
        self.NUM_CHAR = 15

    def _get_new_name(self, input_name: str):

        # first check if we haven't already generated a new name
        try:
            self.dict[input_name]

        except KeyError:

            # Generate new name
            ###

            # choosing a pattern at random
            idx = random.randint(1, len(self.PATTERNS))

            pattern = self.PATTERNS[idx]

            # creating name from pattern
            name = ""

            if pattern["initial"] is not None:
                name += pattern["initial"]

            # generate name from list of chars
            name += "".join(random.choices(pattern["chars"], k=self.NUM_CHAR))

            # save to dict
            self.dict[input_name] = name

            return name

        finally:

            return self.dict[input_name]

    @fix_wrapper
    def fix(self, tokens):

        tokens, tokens_copy = tee(tokens)

        def scan(elements):
            """[summary]
            Iterates over tokens, looking for variable names to
            substitute

            [description]
            We slide a 3-element window and try to catch:

            def NAME(...)

            NAME = ...

            class NAME

            Ignore:

            if import in line

            """

            # iterate over 3-windows
            for win in window(elements, 3):

                # get tokens
                first, middle, last = win

                # check if definition
                if first.string in ["def", "class"] and middle.type == NAME:

                    # ignore if function name contains "__"
                    # like __init__ etc
                    if "__" not in middle.string:

                        # write into dictionary
                        self._get_new_name(middle.string)

                # check if isolated variable
                if first.type in [NL, INDENT, DEDENT] and middle.type == NAME:

                    # check if middle is not a build-in and if not isolated
                    # function call
                    if not isbuildin(middle.string) and last.string != "(":

                        # write into dictionary
                        self._get_new_name(middle.string)

        def substitute(elements):
            """[summary]
            Iterate over all NAMEs and substitute from the dictionary

            [description]
            """

            result = []

            # iterating over tokens
            for token_type, token_val, _, _, _, in elements:

                # if token is a Name, substitute from dict.
                if token_type == NAME:

                    try:
                        new_name = self.dict[token_val]

                        result.append(
                            (NAME, new_name)
                        )

                    except KeyError:
                        result.append(
                            (NAME, token_val)
                        )

                else:
                    result.append((token_type, token_val))
            return result

        scan(tokens)
        result = substitute(tokens_copy)
        return result


if __name__ == '__main__':

    fixer = VariableFixer()

    fixer.fix("./test.py")
