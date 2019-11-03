# -*- coding: utf-8 -*-

import pytest
from lancer.prototype import ProtoCommentFixer as CommentFixer
from pathlib import Path

__author__ = "Levi Borodenko"
__copyright__ = "Levi Borodenko"
__license__ = "mit"


class TestCommentFixer(object):
    """docstring for TestCommentFixer"""

    # test file
    COMMENTS_FILE = "./test_scripts/comments.py"

    # test instance
    fixer = CommentFixer(COMMENTS_FILE)

    def test_init(self):
        """Testing basic attributes.
        """
        assert isinstance(self.fixer.FILE_PATH, Path)
        assert self.fixer.FILE_PATH.name == "comments.py"

        with pytest.raises(ValueError):
            CommentFixer("Not_a_python_file.txt")

        with pytest.raises(FileNotFoundError):
            CommentFixer("./nosuchfile.py")

    def test_get_lyric(self):
        """Test random lyric generation.
        """

        lyric = self.fixer.get_lyric()

        assert isinstance(lyric, str)
        assert len(lyric) > 2

        another_lyric = self.fixer.get_lyric()

        assert lyric != another_lyric

        assert self.fixer.NUM_LYRICS > 100
