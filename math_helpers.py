#   Primary Author: Aadesh M Bagmar <aadeshbagmar@gmail.com>
#
#   Purpose: Mathematical Helper functions

from typing import Tuple

def modulo_multiply(a: int, b: int, mod: int) -> int:
    """
    Evaluates a * b % mod
    """
    if mod == 0:
        raise Exception("Divide by zero error")


    return ((a % mod) * (b % mod)) % mod

def modulo_pow(a: int, b: int, mod: int) -> int:
    """
    Evaluates a^b % mod.

    Args:
        a (int): Base
        b (int): Power
        mod (int): Modulo

    Returns:
        a ^ b % mod
    """
    result = 1
    while b:
        result = modulo_multiply(result, a, mod)
        b -= 1
    return result % mod

def egcd(a: int, b: int)->Tuple[int, int, int]:
    """
    Extended Euclidean algorithm to compute the gcd
    Taken from https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm

    Returns:
        A tuple (g, x, y) where a*x + b*y = gcd(x, y)
    """
    if a == 0:
        return (b, 0, 1)

    g, x, y = egcd(b % a, a)
    return (g, y - (b // a) * x, x)


def modulo_div(a: int, b: int, mod: int) -> int:
    """
    Evaluates (a / b) % mod
    """
    return modulo_multiply(a, mulinv(b, mod), mod)

def mulinv(b: int, n: int) -> int:
    """
    Multiplicative inverse of b modulo n
    """

    g, x, _ = egcd(b, n)

    if g == 1:
        return x % n

    raise Exception("Modular Inverse does not exist")