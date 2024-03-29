# -*- coding: utf-8 -*-

from random import choice
from builtins import bytes

xor = lambda a, b: list(map(lambda x, y: x ^ y, a, b))

rotl = lambda x, n: ((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)

get_uint32_be = lambda key_data: ((key_data[0] << 24) | (key_data[1] << 16) | (key_data[2] << 8) | (key_data[3]))

put_uint32_be = lambda n: [((n >> 24) & 0xff), ((n >> 16) & 0xff), ((n >> 8) & 0xff), ((n) & 0xff)]

padding = lambda data, block=16: data + [(16 - len(data) % block)for _ in range(16 - len(data) % block)]

unpadding = lambda data: data[:-data[-1]]


def bytes_to_int(bytes):
    """
    Convert bytes to a signed integer.

    Args:
        bytes: write your description
    """
    result = 0
    for b in bytes:
        result = result * 256 + ord(b)
    return result


def int_to_bytes(value, length):
    """
    Convert a value to a list of bytes.

    Args:
        value: write your description
        length: write your description
    """
    result = []
    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)
    result.reverse()
    return result


list_to_bytes = lambda data: b''.join([bytes((i,)) for i in data])

bytes_to_list = lambda data: [bytes_to_int(i) for i in data]

random_hex = lambda x: ''.join([choice('0123456789abcdef') for _ in range(x)])
