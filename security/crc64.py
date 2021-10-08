# -*- coding: utf-8 -*-

try:
    from crcmod.crcmod import *
    import crcmod.predefined
except ImportError:
    # Make this backward compatible
    from crcmod import *
__doc__ = crcmod.__doc__

from .crc64_combine import mkCombineFun


class Crc64(object):

    _POLY = 0x142F0E1EBA9EA3693
    _XOROUT = 0XFFFFFFFFFFFFFFFF

    def __init__(self, init_crc=0):
        """
        Compose the polynomials.

        Args:
            self: write your description
            init_crc: write your description
        """
        self.crc64 = crcmod.Crc(self._POLY, initCrc=init_crc, rev=True, xorOut=self._XOROUT)
        self.crc64_combineFun = mkCombineFun(self._POLY, initCrc=init_crc, rev=True, xorOut=self._XOROUT)

    def __call__(self, data):
        """
        Update the cache with the given data.

        Args:
            self: write your description
            data: write your description
        """
        self.update(data)

    def update(self, data):
        """
        Update the CRC64 with the given data.

        Args:
            self: write your description
            data: write your description
        """
        self.crc64.update(data)

    def combine(self, crc1, crc2, len2):
        """
        Combines two CRC64s and returns the result.

        Args:
            self: write your description
            crc1: write your description
            crc2: write your description
            len2: write your description
        """
        return self.crc64_combineFun(crc1, crc2, len2)

    @property
    def crc(self):
        """
        CRC of the file.

        Args:
            self: write your description
        """
        return self.crc64.crcValue
