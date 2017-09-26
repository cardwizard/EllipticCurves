#   Primary Author: Aadesh M Bagmar <aadeshbagmar@gmail.com>
#
#   Purpose: Diffie Hellman Using ECC

from ecc import *


def generate_keys(p: int, a: int, b: int, G: Tuple, n: int)->Point:
    """
    Generates keys according to the Diffie Hellman Algorithm

    Args:
        p (int): Prime field size
        a (int): Coefficient of x^1 in the Elliptic Curve
        b (int): Coefficient of x^0 in the Elliptic Curve
        G (Point): Generator Point on the curve
        n (int): Private Key

    Returns:
        Generated key.
    """
    elliptic_curve = EllipticCurve(a, b, p)
    generator = Point(elliptic_curve, G[0], G[1], "Generator")
    generated_point = generator * n
    return generated_point

    # print(elliptic_curve, generated_point)
    # generated_point.name = "{} X Generator".format(n)
    # elliptic_curve.plot_points([generator])
    # return 0

if __name__ == '__main__':
    alice_private_key = 4
    bob_private_key = 7

    ecc = EllipticCurve(7, 3, 37)
    Generator = Point(ecc, 2, 5, "Generator")

    alice_pub = alice_private_key * Generator
    alice_pub.name = "Alice Public Key"

    bob_pub = bob_private_key * Generator
    bob_pub.name = "Bob Public Key"

    shared_secret_bob = alice_pub * bob_private_key
    shared_secret_alice = bob_pub * alice_private_key

    assert(shared_secret_alice == shared_secret_bob)
    shared_secret_alice.name = "Shared Secret"

    ecc.plot_points([Generator, alice_pub, bob_pub, shared_secret_alice])


