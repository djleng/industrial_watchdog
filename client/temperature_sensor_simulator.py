import numpy as np
import random as ran
#from argparse import ArgumentParser


def get_temperature_data():
    dx = 1.0
    x = np.arange(1.0, 3601.0, dx)
    y = np.log(x)
    for i in np.nditer(y, op_flags=['readwrite']):
        i[...] = i + ran.uniform(0.0, 50.0)
    return y
