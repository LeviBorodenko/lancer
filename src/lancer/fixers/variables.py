import logging
from tokenize import NAME, NL, DEDENT, INDENT
from itertools import tee
import random
from lancer.utils import fix_wrapper, window, isbuildin
import pkg_resources

# import pkg_resources

__author__ = "Levi Borodenko"
__copyright__ = "Levi Borodenko"
__license__ = "mit"

# setting up logger instance
_logger = logging.getLogger(__name__)


class VariableFixer(object):
    """[summary]
    Changes all your good variable names into horrible ones.

    [description]
    Iterates over file spotting all variable, function and class names,
    substituting them with its own BAD ones.

    Methods:
        fix(file) - takes file and returns the fixed "file.lanced"

    Todo:
        Fix annotation compatability
    """

    def __init__(self):
        super(VariableFixer, self).__init__()

        # setting name
        self.__name__ = "VariableFixer"

        # dictionary containing the patterns to generate the new names
        self.PATTERNS = {1: {"initial": "O", "chars": ["0", "O", "Ο"]},
                         2: {"initial": "I", "chars": ["I", "l", "Ι", "1"]},
                         3: {"initial": None, "chars": ["α", "a"]}
                         }

        # initializing dict that will translate the actual variable names
        # to our generated onces.
        self.dict = {}

        # length of variable name noise
        self.NUM_NOISE_CHAR = 5

        # Path to lyric file resource
        self.SOUNDS_FILE = pkg_resources.resource_filename(
            __name__, "../resources/sounds.txt")

        # Number of Sounds
        self.NUM_SOUNDS = sum(1 for line in open(self.SOUNDS_FILE))

    def _get_random_noise(self) -> str:
        """[summary]
        Returns a random horrible mess according to self.PATTERNS

        [description]
        Stuff like: IllIlI11Ι1IIIlI1, 000O00OOO, aaαaaααααaaaαaα etc
        """
        # choosing a pattern at random
        idx = random.randint(1, len(self.PATTERNS))

        pattern = self.PATTERNS[idx]

        # creating noise from pattern
        noise = ""

        if pattern["initial"] is not None:
            noise += pattern["initial"]

        # generate noise from list of chars
        noise += "".join(random.choices(pattern["chars"],
                                        k=self.NUM_NOISE_CHAR))

        return noise

    def _get_random_animal_sound(self) -> str:
        """[summary]
        returns a random animal sound like "bark_bark" etc.
        [description]
        We read the animal sounds from /resource/sounds.txt
        """

        # Open sounds file and grab a random line
        with open(self.SOUNDS_FILE) as f:

            random_index = random.randint(0, self.NUM_SOUNDS - 1)

            sounds = f.readlines()

            # get random sound and strip whitespaces
            sound = sounds[random_index].rstrip()

            # repeat sound up to 2 times
            sound_list = [sound for i in range(random.randint(1, 3))]

            # join them to one string
            sound = "_".join(sound_list) + "_"

            return sound

    def _get_new_name(self, input_name: str):

        # first check if we haven't already generated a new name
        try:
            self.dict[input_name]

        except KeyError:

            # Generate new name
            ###

            sounds = self._get_random_animal_sound()
            noise = self._get_random_noise()

            # combine to generate variable name
            name = sounds + noise

            # save to dict
            self.dict[input_name] = name

            return name

        finally:

            return self.dict[input_name]

    def _spot_definitions(self, token_triple: iter) -> None:
        """[summary]
        Looks for function and class names in a token triple

        [description]
        Takes a consecutive token triple and checks if the middle one
        if is:

        def NAME(...):

        class NAME(...):

        Arguments:
            token_triple {iter} -- consecutive token triple
        """
        # get tokens
        first, middle, last = token_triple

        # check if definition
        if first.string in ["def", "class"] and middle.type == NAME:

            # ignore if function name contains "__"
            # like __init__ etc
            if "__" not in middle.string:

                # write into dictionary
                self._get_new_name(middle.string)

    def _spot_isolated_names(self, token_triple: iter) -> None:
        """[summary]
        Looks for isolated variable definitions

        [description]
        Takes a consecutive token triple and checks if the middle one
        if is:

        NAME = ...


        Arguments:
            token_triple {iter} -- consecutive token triple
        """
        # get tokens
        first, middle, last = token_triple

        # check if "first" empty
        if first.type in [NL, INDENT, DEDENT] and middle.type == NAME:

            # check if middle is not a build-in name.
            # For cases like:
            #   return ...all

            # also we want to avoid selecting names of isolated function calls.
            # Things like:
            #   function(...)
            if not isbuildin(middle.string) and last.string != "(":

                # write into dictionary
                self._get_new_name(middle.string)

    def _spot_argument_names(self, token_triple: iter) -> None:
        """[summary]
        Looks for argument names.

        [description]
        Takes a consecutive token triple and checks if the middle one
        if is:

        def function(NAME1, NAME2 = ..., *NAME3, **NAME4):

        Arguments:
            token_triple {iter} -- consecutive token triple
        """

        # get tokens
        first, middle, last = token_triple

        # check if we are defining something and if yes, make sure
        # the middle is followed by either a comma, = or closing bracket
        if "def" in first.line and last.string in ["=", ",", ")", ":"]:

            # also make sure middle is an actual NAME and not "self".
            if middle.type == NAME and middle.string != "self":

                # additinally we need to check that it is not an annotation :)
                # sorry about the chain of if statements. How to avoid them?
                if first.string not in [":", "->"]:

                    # write into dictionary
                    self._get_new_name(middle.string)

    def _substitute(self, tokens):

        result = []

        # iterating over tokens
        for token_type, token_val, _, _, _, in tokens:

            # if token is a Name, substitute from dict.
            if token_type == NAME:

                try:

                    # try to get name
                    new_name = self.dict[token_val]
                    result.append((NAME, new_name))

                except KeyError:

                    # if name not collected
                    # leave it as is.
                    result.append((NAME, token_val))

            # if not a name, append as is.
            else:
                result.append((token_type, token_val))

        return result

    @fix_wrapper
    def fix(self, tokens):

        tokens, tokens_copy = tee(tokens)

        # iterate over consecutive token triples
        for win in window(tokens, 3):

            # collect names in each
            self._spot_definitions(win)
            self._spot_argument_names(win)
            self._spot_isolated_names(win)

        # after spotting all, substitute all names according
        # to our collected dictionary
        result = self._substitute(tokens_copy)

        return result
