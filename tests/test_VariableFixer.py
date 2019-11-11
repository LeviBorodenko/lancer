# -*- coding: utf-8 -*-

from lancer.fixers.variables import VariableFixer

__author__ = "Levi Borodenko"
__copyright__ = "Levi Borodenko"
__license__ = "mit"


class TestCommentFixer(object):
    """Testing the CommentFixer class."""

    # test file content
    TEST_FILE_CONTENT = """
        from pathlib import Path


        def some_function(some_arg: Path= "lol"):

            a = "b"

            # comment 1
            return a

        # comment 2


        if __name__ == '__main__':

        # comment 3
        some_function()
    """

    # test instance
    fixer = VariableFixer()

    def test_init(self):

        assert self.fixer.__name__ == "VariableFixer"

    def test_name_gen(self):

        name = self.fixer._get_new_name("TEST")

        assert isinstance(name, str)

        # check that we have saved the old name and the translation
        assert self.fixer.dict["TEST"] == name

        # check if same name generates same output
        assert name == self.fixer._get_new_name("TEST")

    def test_fix(self, tmp_path):
        """Testing it can fix without breaking.
        """
        # create temporary folder and script file
        path = tmp_path / "folder"
        path.mkdir()

        file = path / "variables.py"
        file.write_text(self.TEST_FILE_CONTENT)

        self.fixer.fix(file)
