"""
Module that handles DFT related tasks
"""
import math


class DFT:
    """
    Class that handles discrete fourier transform calculations
    """

    def __init__(self, sampler, size=50):
        """
        Constructor:
        sampler: The function to sample points from.
        size: The accuracy of the transform. An infinite value gives perfect precision.
        """
        self.size = size
        self.constants = self.calculate_constants(sampler)

    def __call__(self, time):
        """
        Overloading the call operator to make the calls friendly.
        Calculating the value of the equation.
        """
        sum = 0
        for index, c in enumerate(self.constants):
            n = index - self.size
            sum += c * (math.e ** (2 * math.pi * complex(0, 1) * time * n))
        return sum

    def integrate(self, n, sampler, start=0, end=1, delta=0.001):
        """
        Numerical integration to calculate the value of the one of the constant
        in the DFT equation.
        """
        sum = 0
        while start < end:
            sum += (math.e ** (-2*math.pi*complex(0, 1)*n *
                               (start+delta/2))) * sampler(start+delta/2) * delta
            start += delta
        return sum

    def calculate_constants(self, sampler):
        """
        A helper function that integrates all values from -size to size.
        """
        constants = []
        for n in range(-self.size, self.size+1):
            constants.append(self.integrate(n, sampler))
        return constants
