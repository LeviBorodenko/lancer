# -*- coding: utf-8 -*-

import pytest
from lancer.fixers.comments import CommentFixer
from pathlib import Path

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
    fixer = CommentFixer()

    def test_init(self):

        assert self.fixer.__name__ == "CommentFixer"

    def test_fix(self, tmp_path):
        """Testing basic attributes.
        """
        # create temporary folder and script file
        path = tmp_path / "folder"
        path.mkdir()

        file = path / "comments.py"
        file.write_text(self.TEST_FILE_CONTENT)

        self.fixer.fix(file)

        assert self.fixer.__output__ == path / "comments.lanced"

        assert isinstance(self.fixer.FILE_PATH, Path)
        assert self.fixer.FILE_PATH.name == "comments.py"

        with pytest.raises(ValueError):
            self.fixer.fix("Not_a_python_file.txt")

        with pytest.raises(FileNotFoundError):
            self.fixer.fix("No_such_file.py")

    def test_get_lyric(self):
        """Test random lyric generation.
        """

        lyric = self.fixer._get_lyric()

        assert isinstance(lyric, str)
        assert len(lyric) > 2

        another_lyric = self.fixer._get_lyric()

        assert lyric != another_lyric

        # make sure comment starts with "# "
        assert lyric[:2] == "# "

        assert self.fixer.NUM_LYRICS > 100
