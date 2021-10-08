# -*- coding: utf-8 -*-

from .utils.compatibility import toBytes
from .utils.der import fromPem, removeSequence, removeObject, removeBitString, toPem, encodeSequence, encodeOid, encodeBitString
from .utils.binary import BinaryAscii
from .point import Point
from .curve import curvesByOid, supportedCurves, sm2p256v1


class PublicKey:

    def __init__(self, point, curve):
        """
        Initialize the point and curve.

        Args:
            self: write your description
            point: write your description
            curve: write your description
        """
        self.point = point
        self.curve = curve

    def toString(self, encoded=False):
        """
        Return a string representation of the curve.

        Args:
            self: write your description
            encoded: write your description
        """
        xString = BinaryAscii.stringFromNumber(
            number=self.point.x,
            length=self.curve.length(),
        )
        yString = BinaryAscii.stringFromNumber(
            number=self.point.y,
            length=self.curve.length(),
        )
        return "\x00\x04" + xString + yString if encoded else xString + yString

    def toStr(self):
        """
        Returns a string representation of the point.

        Args:
            self: write your description
        """
        return str(hex(self.point.x))[2:-1] + str(hex(self.point.y))[2:-1]

    def toDer(self):
        """
        Return a DER - encoded representation of this EllipticCurve.

        Args:
            self: write your description
        """
        oidEcPublicKey = (1, 2, 840, 10045, 2, 1)
        encodeEcAndOid = encodeSequence(
            encodeOid(*oidEcPublicKey),
            encodeOid(*self.curve.oid),
        )

        return encodeSequence(encodeEcAndOid, encodeBitString(self.toString(encoded=True)))

    def toPem(self):
        """
        Return this Signer as a DER - encoded PEM.

        Args:
            self: write your description
        """
        return toPem(der=toBytes(self.toDer()), name="PUBLIC KEY")

    @classmethod
    def fromPem(cls, string):
        """
        Create a PrivateKey from a PEM encoded string.

        Args:
            cls: write your description
            string: write your description
        """
        return cls.fromDer(fromPem(string))

    @classmethod
    def fromDer(cls, string):
        """
        Create a curve from a DER encoded string.

        Args:
            cls: write your description
            string: write your description
        """
        s1, empty = removeSequence(string)
        if len(empty) != 0:
            raise Exception("trailing junk after DER public key: {}".format(
                BinaryAscii.hexFromBinary(empty)
            ))

        s2, pointBitString = removeSequence(s1)

        oidPk, rest = removeObject(s2)

        oidCurve, empty = removeObject(rest)
        if len(empty) != 0:
            raise Exception("trailing junk after DER public key objects: {}".format(
                BinaryAscii.hexFromBinary(empty)
            ))

        if oidCurve not in curvesByOid:
            raise Exception(
                "Unknown curve with oid %s. Only the following are available: %s" % (
                    oidCurve,
                    ", ".join([curve.name for curve in supportedCurves])
                )
            )

        curve = curvesByOid[oidCurve]

        pointStr, empty = removeBitString(pointBitString)
        if len(empty) != 0:
            raise Exception(
                "trailing junk after public key point-string: " +
                BinaryAscii.hexFromBinary(empty)
            )

        return cls.fromString(pointStr[2:], curve)

    @classmethod
    def fromString(cls, string, curve=sm2p256v1, validatePoint=True):
        """
        Create a PublicKey instance from a string.

        Args:
            cls: write your description
            string: write your description
            curve: write your description
            sm2p256v1: write your description
            validatePoint: write your description
        """
        baseLen = curve.length()

        xs = string[:baseLen]
        ys = string[baseLen:]

        p = Point(
            x=BinaryAscii.numberFromString(xs),
            y=BinaryAscii.numberFromString(ys),
        )

        if validatePoint and not curve.contains(p):
            raise Exception(
                "point ({x},{y}) is not valid for curve {name}".format(
                    x=p.x, y=p.y, name=curve.name
                )
            )

        return PublicKey(point=p, curve=curve)
