import logging
# from tokenize import COMMENT
import random
from lancer.utils import fix_wrapper, setup_logging, window
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
        for win in window(tokens, 3):
            a, b, c = win

            print(a.type)

        return tokens


if __name__ == '__main__':

    fixer = VariableFixer()

    fixer.fix("test.py")
