import math
import turtle

from sampler import *
from dft import DFT
import argparse


def draw_dft(f):
    """
    Draw a DFT represented using turtle
    """
    time = 0.001
    turtle.penup()
    turtle.goto(f(0).real, f(0).imag)
    turtle.speed(0)
    turtle.pensize(1)
    turtle.pendown()

    while time < 1:
        point = f(time)
        turtle.goto(point.real, point.imag)
        time += 0.01


def main():

    parser = argparse.ArgumentParser(description='Display DFT curves')
    parser.add_argument('image', help='The image to draw', choices=("hunter", "scenery", "fairy"))
    args = parser.parse_args()
    

    choice_map = {
        "hunter": "resources/hunter.dat",
        "scenery": "resources/scene.dat",
        "fairy": "resources/fairy.dat",
    }

    samplers = create_dft_samplers(choice_map[args.image])
    for sampler in samplers:
        dft = DFT(sampler, size = 50)
        draw_dft(dft)

    turtle.getscreen().mainloop()

if __name__ == '__main__':
    main()
