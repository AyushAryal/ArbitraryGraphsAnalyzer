"""
Module that handles SVG files.
"""
from enum import Enum


class CommandType(Enum):
    """
    An enumeration to implement SVG commands
    """
    MoveAbsolute = 'M'
    LineAbsolute = 'L'
    VerticalAbsolute = "V"
    HorizontalAbsolute = "H"
    CubicAbsolute = 'C'
    ClosePointAbsolute = 'Z'



class Command:
    """
    A class that represents a single SVG command
    """
    def __init__(self, type):
        self.type = type
        self.points = []

    def __repr__(self):
        s = f"[ {self.type.name}: "
        for x, y in self.points:
            s += f"({x},{y}), "
        s += ']'
        return s

    def __str__(self):
        return self.__repr__()



class SVG:
    """
    A class that only has static methods.
    Parses SVG commands.
    """

    @staticmethod
    def spline_to_points(splines, current_point, points_per_curve=4):
        """
        Converts the unique curve splines to a form that is usable for DFT
        """
        splines = [current_point, ] + splines
        assert (len(splines) - 1) % (points_per_curve -
                                     1) == 0, "Points must be of certain format"

        points = []
        for index in range(0, len(splines)-1, points_per_curve-1):
            points.append(
                list(map(lambda x: complex(*x),  splines[index: index + points_per_curve])))
        return points

    @staticmethod
    def parse(file_path: str) -> [Command]:
        with open(file_path) as f:
            scale, offset, data = f.readlines()
            scale = tuple(map(float, scale.split()))
            offset = tuple(map(float, offset.split()))
            svg = data.split()
        current_command = None
        command_list: [Command] = []
        for item in svg:
            if item.isalpha():
                if current_command:
                    command_list.append(current_command)
                current_command = Command(CommandType(item))
            else:
                if current_command:
                    if current_command.type == CommandType.HorizontalAbsolute:
                        ...
                        # Not necessary to implement.
                        # current_command.points.append((float(item),0))
                        # current_command.type = CommandType.LineAbsolute
                    elif current_command.type == CommandType.VerticalAbsolute:
                        ...
                        # Not necessary to implement.
                        # current_command.points.append((0,-float(item)))
                        # current_command.type = CommandType.LineAbsolute
                    else:
                        current_command.points.append((scale[0] * float(item.split(",")[0]) + offset[0],
                                                       - scale[1] * float(item.split(",")[1]) + offset[1]))

        if current_command:
            command_list.append(current_command)
        return command_list
