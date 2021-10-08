
# -*- coding: utf-8 -*-

from base64 import b64encode, b64decode


class Base64:

    @classmethod
    def decode(cls, string):
        """
        Base64 decode string.

        Args:
            cls: write your description
            string: write your description
        """
        return b64decode(string)

    @classmethod
    def encode(cls, string):
        """
        Base64 encode the string.

        Args:
            cls: write your description
            string: write your description
        """
        return b64encode(string)
