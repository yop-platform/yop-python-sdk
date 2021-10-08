# -*- coding: utf-8 -*-

from .utils.integer import RandomInteger
from .utils.compatibility import toBytes
from .utils.binary import BinaryAscii
from .utils.der import fromPem, removeSequence, removeInteger, removeObject, removeOctetString, removeConstructed, toPem, encodeSequence, encodeInteger, encodeBitString, encodeOid, encodeOctetString, encodeConstructed
from .publicKey import PublicKey
from .curve import sm2p256v1, curvesByOid, supportedCurves
from .math import Math

hexAt = "\x00"


class PrivateKey:

    def __init__(self, curve=sm2p256v1, secret=None):
        """
        Curve construction.

        Args:
            self: write your description
            curve: write your description
            sm2p256v1: write your description
            secret: write your description
        """
        self.curve = curve
        self.secret = secret or RandomInteger.between(1, curve.N - 1)

    def publicKey(self):
        """
        Return public key as PublicKey object.

        Args:
            self: write your description
        """
        curve = self.curve
        publicPoint = Math.multiply(
            p=curve.G,
            n=self.secret,
            N=curve.N,
            A=curve.A,
            P=curve.P,
        )
        return PublicKey(point=publicPoint, curve=curve)

    def toString(self):
        """
        Return the secret key as a string.

        Args:
            self: write your description
        """
        return BinaryAscii.stringFromNumber(number=self.secret, length=self.curve.length())

    def toDer(self):
        """
        Return a DER - encoded representation of this EllipticCurve.

        Args:
            self: write your description
        """
        encodedPublicKey = self.publicKey().toString(encoded=True)

        return encodeSequence(
            encodeInteger(1),
            encodeOctetString(self.toString()),
            encodeConstructed(0, encodeOid(*self.curve.oid)),
            encodeConstructed(1, encodeBitString(encodedPublicKey)),
        )

    def toPem(self):
        """
        Return this Signer as a DER - encoded PEM.

        Args:
            self: write your description
        """
        return toPem(der=toBytes(self.toDer()), name="EC PRIVATE KEY")

    @classmethod
    def fromPem(cls, string):
        """
        Create a PrivateKey from a DER encoded private key.

        Args:
            cls: write your description
            string: write your description
        """
        # privateKeyPem = string[string.index("-----BEGIN EC PRIVATE KEY-----"):]
        return cls.fromDer(fromPem(string))

    @classmethod
    def fromDer(cls, string):
        """
        Create a PrivateKey from a DER encoded string.

        Args:
            cls: write your description
            string: write your description
        """
        t, empty = removeSequence(string)
        if len(empty) != 0:
            raise Exception(
                "trailing junk after DER private key: " +
                BinaryAscii.hexFromBinary(empty)
            )

        one, t = removeInteger(t)
        if one != 1:
            # Java编码的私钥此处为0
            # raise Exception(
            #     "expected '1' at start of DER private key, got %d" % one
            # )
            privateKeyStr = string[35:35 + 32]
            oidCurve = (1, 2, 156, 10197, 1, 301)
            curve = curvesByOid[oidCurve]
            return cls.fromString(privateKeyStr, curve)

        privateKeyStr, t = removeOctetString(t)
        tag, curveOidStr, t = removeConstructed(t)
        if tag != 0:
            raise Exception("expected tag 0 in DER private key, got %d" % tag)

        oidCurve, empty = removeObject(curveOidStr)

        if len(empty) != 0:
            raise Exception(
                "trailing junk after DER private key curve_oid: %s" %
                BinaryAscii.hexFromBinary(empty)
            )

        if oidCurve not in curvesByOid:
            raise Exception(
                "unknown curve with oid %s; The following are registered: %s" % (
                    oidCurve,
                    ", ".join([curve.name for curve in supportedCurves])
                )
            )

        curve = curvesByOid[oidCurve]

        if len(privateKeyStr) < curve.length():
            privateKeyStr = hexAt * (curve.lenght() - len(privateKeyStr)) + privateKeyStr

        return cls.fromString(privateKeyStr, curve)

    @classmethod
    def fromString(cls, string, curve=sm2p256v1):
        """
        Create a PrivateKey instance from a string.

        Args:
            cls: write your description
            string: write your description
            curve: write your description
            sm2p256v1: write your description
        """
        return PrivateKey(secret=BinaryAscii.numberFromString(string), curve=curve)
