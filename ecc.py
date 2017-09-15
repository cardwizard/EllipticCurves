#   Primary Author: Aadesh M Bagmar <aadesh@soroco.com>
#
#   Purpose: Elliptic Curve Cryptography main class

from math_helpers import *
from typing import List, Tuple, Dict

import matplotlib.pyplot as plt
import math

class EllipticCurve:
    def __init__(self, a: int, b: int, field_size: int)->None:
        """
        An Elliptic curve can be defined as y^2 = x^3 + ax + b

        Args:
            a (int): Coefficient for x^1
            b (int): Coefficient for x^0
            field_size (int): Finite field size
        """
        self.a = a
        self.b = b
        self.field = field_size

        discriminant = modulo_multiply(-16, (modulo_multiply(4, modulo_pow(a, 3, self.field), self.field) +
                                             modulo_multiply(27, modulo_pow(b, 2, self.field), self.field)), self.field)

        self.discriminant = discriminant % self.field

        if not self.is_group():
            raise Exception("The curve does not satisfy condition for a group")

        self.order = len(self.find_coordinates()) + 1

    def is_group(self)->bool:
        """
        An Elliptic curve satisfies the condition to be a group only if the discriminant is non-zero

        Returns:
            Boolean whether it is a group or not.
        """
        return self.discriminant != 0

    def find_coordinates(self)->List[Tuple]:
        coordinate_list = []
        for index in range(0, self.field):
            rhs = self.evaluate_rhs(index)
            y = math.sqrt(rhs)

            if y.is_integer():
                y = int(y)

                coordinate_list.append((index % self.field, y % self.field))
                coordinate_list.append((index % self.field, -y % self.field))

        return coordinate_list

    def plot_curve(self)->plt:
        coordinates = self.find_coordinates()
        x = [x[0] for x in coordinates]
        y = [x[1] for x in coordinates]

        plt.scatter(x, y)
        plt.grid()
        plt.title("Curve -> {}".format(self))
        return plt

    def plot_points(self, annotated_points: [])->None:
        coordinates = self.find_coordinates()
        x = [x[0] for x in coordinates]
        y = [x[1] for x in coordinates]

        fig, ax = plt.subplots()
        ax.scatter(x, y)
        plt.grid()

        for point in annotated_points:
            ax.annotate("{} ({}, {})".format(point.name, point.x, point.y),
                        (point.x, point.y), xytext=(point.x + 1.5, point.y + 0.5),
                        arrowprops=dict(facecolor='black', shrink=0.05))
        plt.show()


    def __str__(self)->str:
        """
        Print the curve
        """
        return "y^2 = x^3 + {}x + {} on finite field F({}).".format(self.a, self.b, self.field)

    def __eq__(self, other)->bool:
        """
        Check if two curves are equal

        Returns:
            Boolean value suggesting equality of the curves
        """
        return (self.a, self.b) == (other.a, other.b)

    def evaluate_lhs(self, y: int)->int:
        return modulo_pow(y, 2, self.field)

    def evaluate_rhs(self, x: int)->int:
        return (modulo_pow(x, 3, self.field) +
                modulo_multiply(x, self.a, self.field) +
                self.b) % self.field

class Point:
    def __init__(self, curve: EllipticCurve, x: int, y: int, name: str="")->None:
        self.curve = curve
        self.x = x % self.curve.field
        self.y = y % self.curve.field
        self.name = name

        if not self.test_point():
            raise Exception("The given point ({}, {}) is not on the curve {}.".format(self.x, self.y, curve))

    def test_point(self)->bool:
        return self.curve.evaluate_lhs(self.y) == self.curve.evaluate_rhs(self.x)

    def plot_point(self)->None:
        self.curve.plot_points({self.name: (self.x, self.y)})

    def __neg__(self):
        return Point(self.curve, self.x, -self.y, "{}'".format(self.name))

    def __str__(self)->str:
        return "Point {} = ({}, {})".format(self.name, self.x, self.y)

    def __eq__(self, other):
        return (self.curve, self.x, self.y) == (other.curve, other.x, other.y)

    def __add__(self, Q):
        """
        Args:
            Q: Adding a point to self

        Returns:
            Point object after adding a point
        """

        if isinstance(Q, Ideal):
            return self

        x_1, y_1, x_2, y_2 = self.x, self.y, Q.x, Q.y

        if (x_1, y_1) == (x_2, y_2):
            if y_1 == 0:
                return Ideal(self.curve)

            numerator = (modulo_multiply(3, modulo_pow(x_1, 2, self.curve.field),
                                         self.curve.field) + self.curve.a) % self.curve.field
            denominator = modulo_multiply(2, y_1, self.curve.field) % self.curve.field

            slope = modulo_div(numerator, denominator, self.curve.field)
        else:
            if x_1 == x_2:
                return Ideal(self.curve)

            numerator = (y_2 - y_1) % self.curve.field
            denominator = (x_2 - x_1) % self.curve.field
            slope = modulo_div(numerator, denominator, self.curve.field)

        x_3 = (modulo_pow(slope, 2, self.curve.field) - x_2 - x_1) % self.curve.field
        y_3 = (modulo_multiply(slope, (x_3 - x_1) % self.curve.field, self.curve.field) + y_1) % self.curve.field

        return Point(self.curve, x_3, -y_3)

    def __mul__(self, n: int):
        """
        Multiplying a scalar to a point in a field.

        Args:
            n (int): Scalar to multiple

        Returns:
            Point object
        """
        if n < 0:
            return -self * -n
        if n == 0:
            return Ideal(self.curve)
        else:
            Q = self
            R = self if n & 1 == 1 else Ideal(self.curve)
            i = 2
            while i <= n:
                Q = Q + Q

                if n & i == i:
                    R = Q + R
                i = i << 1
        return R


    def __rmul__(self, n: int):
        return self * n

class Ideal(Point):
    def __init__(self, curve):
        self.curve = curve
        self.x = 0
        self.y = 0

    def __str__(self)->str:
        return "Ideal"

    def __neg__(self):
        return self

    def __add__(self, Q):
        return Q

def main()->None:
    e = EllipticCurve(7, 3, 37)
    # # e.plot_curve().show()
    print(e)
    p = Point(e, 2, 5, "P")
    q = 4 * p

    q.name = "2P"
    e.plot_points([p, q])
    print(modulo_multiply(26, 19, 37))

if __name__ == '__main__':
    main()