# -*- coding: utf-8 -*-

#
# Elliptic Curve Equation
#
# y^2 = x^3 + A*x + B (mod P)
#

from .point import Point


class CurveFp:

    def __init__(self, A, B, P, N, Gx, Gy, name, oid, nistName=None):
        """
        Initialize the object.

        Args:
            self: write your description
            A: write your description
            B: write your description
            P: write your description
            N: write your description
            Gx: write your description
            Gy: write your description
            name: write your description
            oid: write your description
            nistName: write your description
        """
        self.A = A
        self.B = B
        self.P = P
        self.N = N
        self.G = Point(Gx, Gy)
        self.name = name
        self.nistName = nistName
        self.oid = oid

    def contains(self, p):
        """
        Verify if the point `p` is on the curve

        :param p: Point p = Point(x, y)
        :return: boolean
        """
        return (p.y**2 - (p.x**3 + self.A * p.x + self.B)) % self.P == 0

    def length(self):
        """
        Length of the array

        Args:
            self: write your description
        """
        return (1 + len("%x" % self.N)) // 2


sm2p256v1 = CurveFp(
    name="sm2p256v1",
    A=0xfffffffeffffffffffffffffffffffffffffffff00000000fffffffffffffffc,
    B=0x28e9fa9e9d9f5e344d5a9e4bcf6509a7f39789f515ab8f92ddbcbd414d940e93,
    P=0xfffffffeffffffffffffffffffffffffffffffff00000000ffffffffffffffff,
    N=0xfffffffeffffffffffffffffffffffff7203df6b21c6052b53bbf40939d54123,
    Gx=0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7,
    Gy=0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0,
    oid=(1, 2, 156, 10197, 1, 301),
)

secp256k1 = CurveFp(
    name="secp256k1",
    A=0x0000000000000000000000000000000000000000000000000000000000000000,
    B=0x0000000000000000000000000000000000000000000000000000000000000007,
    P=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    N=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
    Gx=0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    Gy=0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8,
    oid=(1, 3, 132, 0, 10),
)

prime256v1 = CurveFp(
    name="prime256v1",
    nistName="P-256",
    A=0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc,
    B=0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b,
    P=0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff,
    N=0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551,
    Gx=0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
    Gy=0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5,
    oid=(1, 2, 840, 10045, 3, 1, 7),
)
p256 = prime256v1

supportedCurves = [
    secp256k1,
    prime256v1,
    sm2p256v1,
]

curvesByOid = {curve.oid: curve for curve in supportedCurves}
