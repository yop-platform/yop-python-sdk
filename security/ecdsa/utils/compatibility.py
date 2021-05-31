# -*- coding: utf-8 -*-

from sys import version_info as pyVersion
from binascii import hexlify, unhexlify

BLOCK_SIZE = 32  # Bytes, AES256


def pad(data_to_pad, block_size=BLOCK_SIZE):
    '''
    参考 from Crypto.Util.Padding import pad
    '''
    padding_len = block_size - len(data_to_pad) % block_size
    padding = bytes([padding_len]) * padding_len
    return data_to_pad.encode() + padding


if pyVersion.major == 3:
    # py3 constants and conversion functions

    xrange = range
    intTypes = (int, float)

    def toString(string):
        return string.decode("latin-1")

    def toBytes(string):
        return string.encode("latin-1")

    def safeBinaryFromHex(hexString):
        return unhexlify(hexString)

    def safeHexFromBinary(byteString):
        return hexlify(byteString)

    def unpad(padded_data, block_size=BLOCK_SIZE):
        '''
        参考 from Crypto.Util.Padding import unpad
        '''
        pdata_len = len(padded_data)
        if pdata_len == 0:
            raise ValueError("Zero-length input cannot be unpadded")
        if pdata_len % block_size:
            raise ValueError("Input data is not padded")
        padding_len = padded_data[-1]
        if padding_len < 1 or padding_len > min(block_size, pdata_len):
            raise ValueError("Padding is incorrect.")
        if padded_data[-padding_len:] != bytes([padding_len]) * padding_len:
            raise ValueError("PKCS#7 padding is incorrect.")
        return padded_data[:-padding_len].decode()
else:
    # py2 constants and conversion functions

    xrange = range
    intTypes = (int, float, long)  # noqa

    def toString(string):
        return string

    def toBytes(string):
        return string

    def safeBinaryFromHex(hexString):
        return unhexlify(hexString)

    def safeHexFromBinary(byteString):
        return hexlify(byteString)

    def unpad(padded_data, block_size=BLOCK_SIZE):
        '''
        参考 from Crypto.Util.Padding import unpad
        '''
        return padded_data[:-ord(padded_data[-1])]
