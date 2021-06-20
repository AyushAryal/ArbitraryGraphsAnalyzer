"""
Module that handles sampler tasks
"""
import math
from svg import CommandType, SVG
from abc import ABC, abstractmethod, abstractstaticmethod

"""
Creating a abstract class for the sampler.
"""
class Sampler(ABC):
    @abstractmethod
    def __call__(self, t):
        ...

    @abstractmethod
    def length(self):
        ...

"""
A simple line sampler
"""
class LineSampler(Sampler):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __call__(self, t):
        return self.start + (self.end - self.start) * t

    """
    Calculates length of the curve
    """
    def length(self):
        return abs(self.end-self.start)

    def __repr__(self):
        return "{L: " + f"{self.start} {self.end}" + "}"

    def __str__(self):
        return self.__repr__()


class CircleSampler(Sampler):
    def __init__(self, radius):
        self.radius = radius

    def __call__(self, t):
        return self.radius * complex(math.cos(2*math.pi*t), math.sin(2*math.pi*t))

    """
    Calculates length of the curve
    """
    def length(self):
        return 2*math.pi*self.radius

class ArcSampler(Sampler):
    def __init__(self, radius, start, end):
        self.radius = radius
        self.start = start
        self.end = end

    def __call__(self, t):
        return self.radius * complex(math.cos(self.start + (self.end-self.start)*t), math.sin(self.start + (self.end-self.start)*t))

    """
    Calculates length of the curve
    """
    def length(self):
        return (self.end-self.start) * self.radius

class CubicBezierSampler(Sampler):
    def __init__(self, points):
        self.points = points
        self.curve_length = 0
        self.calculate_length()

    def __call__(self, t):
        return ((1-t)**3) * self.points[0] + (3*(1-t)**2)*t*self.points[1] + \
            3*(1-t)*(t**2)*self.points[2] + self.points[3] * (t**3)

    def differentiate(self, t):
        return 3 * ((1-t)**2) * (self.points[1]-self.points[0]) + \
            6 * (1-t) * t * (self.points[2] - self.points[1]) + \
            3 * (t**2) * (self.points[3] - self.points[2])

    """
    Calculates length of the curve
    Using numerical integration since the integral is not easy to compute. 
    Requires elliptic curve integration.
    """
    def calculate_length(self, delta = 0.001):
        t = 0
        integral = 0
        while t < 1:
            derivative = self.differentiate(t + delta/2)
            integral += abs(derivative) * delta
            t+=delta
        self.curve_length = integral

    def length(self):
        return self.curve_length
        

class CombinedSampler(Sampler):
    """
    A sampler capable of combining multiple samplers. 
    The time is distributed according the the length of the individual sampler.
    """

    def __init__(self, samplers):
        self.samplers = samplers
        self.calculate_length()
        self.sampler_frac = [x.length()/self.length() for x in self.samplers]

    def __call__(self, t):
        """
        The time is distributed according the the length of the individual sampler.
        """
        cumulative = 0
        for i, time in enumerate(self.sampler_frac):
            cumulative += time
            if t < cumulative:
                return self.samplers[i]((t-cumulative+time)/(time))

        return self.samplers[-1](t)

    def calculate_length(self):
        self.curve_length = sum(x.length() for x in self.samplers)

    def length(self):
        return self.curve_length

    def __repr__(self):
        return "{ C: [" + ", ".join(str(x) for x in self.samplers) + "] }"

    def __str__(self):
        return self.__repr__()


"""
Creates and combines the samplers obtained from parsing the SVG commands.
"""
def create_dft_samplers(file_path):
    command_list = SVG.parse(file_path)

    samplers = []
    sampler = None
    current_point = None 
    initial_point = None
    for command in command_list:
        if command.type == CommandType.MoveAbsolute:
            current_point = command.points[0]
            initial_point = current_point
            if sampler:
                samplers.append(sampler)
                sampler = None
        if command.type == CommandType.CubicAbsolute:
            points = SVG.spline_to_points(command.points, current_point)
            sampler_new = CombinedSampler([CubicBezierSampler(x) for x in points])
            if sampler:
                sampler = CombinedSampler([sampler, sampler_new])
            else:
                sampler = sampler_new
            current_point = command.points[-1]
        if command.type == CommandType.LineAbsolute:
            points = SVG.spline_to_points(command.points, current_point, points_per_curve=2)
            sampler_new = CombinedSampler([LineSampler(*x) for x in points])
            if sampler:
                if len(points) == 1:
                    sampler = CombinedSampler([sampler, LineSampler(*points[0])])
                else:
                    sampler = CombinedSampler([sampler, sampler_new])
            else:
                if len(points) == 1:
                    sampler = LineSampler(*points[0])
                else:
                    sampler = sampler_new
            current_point = command.points[-1]
        if command.type == CommandType.ClosePointAbsolute:
            if initial_point and current_point and initial_point != current_point:
                if sampler:
                    sampler = CombinedSampler([sampler, LineSampler(complex(*current_point), complex(*initial_point))])
                else:
                    sampler = LineSampler(complex(*current_point), complex(*initial_point))
    if sampler:
        samplers.append(sampler)
            
    return samplers
