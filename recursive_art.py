""" TODO: Put your header comment here """

import random
import math
from PIL import Image


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)

        The base functions that are used are:
                * "x" - take the x position
                * "y" - take the y position
                * "prod" - take the product of two things
                * "avg" - take the average of two things
                * "cos_pi" - take the cosine of a thing times pi
                * "sin_pi" - take the sine of a thing times pi
                * "sqr" - square a thing
                * "abs" - take the aboslute value of a thing
    """
    if min_depth>max_depth:
        max_depth = min_depth
    if min_depth ==0: #Checks if we've recursed enough
        if max_depth == 0 or random.randint(0,1) == 0:
            """ Checks if it's hit the bottom of the recursion
                If we haven't, there's a 50/50 chance that it stops.
            """
            func = random.randint(0,1)
        else:
            func = random.randint(2,7)
            min_depth = 1
    else:
        func = random.randint(2,7)


    if func == 0: #x
        random_function = ["x"]
    elif func == 1: # Y
        random_function = ["y"]
    elif func == 2: # Product
        random_function = ["prod",build_random_function(min_depth-1, max_depth-1),build_random_function(min_depth-1, max_depth-1)]
    elif func ==3: # Average
        random_function = ["avg", build_random_function(min_depth-1, max_depth-1),build_random_function(min_depth-1, max_depth-1)]
    elif func ==4: # Cosin Pi
        random_function = ["cos_pi", build_random_function(min_depth-1, max_depth-1)]
    elif func ==5:  # sine pi
        random_function = ["sin_pi", build_random_function(min_depth-1, max_depth-1)]
    elif func == 6: #cube
        random_function = ["cube", build_random_function(min_depth-1, max_depth-1)]
    elif func ==7: # Arctan
        random_function = ["atan", build_random_function(min_depth-1, max_depth-1)]
    # print(random_function)
    return random_function


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    func=f[0]
    if func == "x":
        return x;
    elif func == "y":
        return y
    elif func == "prod":
        a=evaluate_random_function(f[1],x,y)
        b=evaluate_random_function(f[2],x,y)
        return a*b
    elif func == "avg":
        a=evaluate_random_function(f[1],x,y)
        b=evaluate_random_function(f[2],x,y)
        return 0.5*(a+b)
    elif func == "cos_pi":
        a=evaluate_random_function(f[1],x,y)
        return math.cos(3.14159 * a)
    elif func == "sin_pi":
        a=evaluate_random_function(f[1],x,y)
        return math.sin(3.14159 * a)
    elif func == "cube":
        a=evaluate_random_function(f[1],x,y)
        return a*a*a
    elif func == "atan":
        a=evaluate_random_function(f[1],x,y)
        return math.atan(a)
    else:
        return 0
    pass


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    scaling = (val - input_interval_start)/(input_interval_end-input_interval_start)
    remapped_val = scaling * (output_interval_end - output_interval_start) + output_interval_start
    return remapped_val


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))  #Create a new image of a certain size
    pixels = im.load()  #Give us access to the pixels
    for i in range(x_size):  #Loops through columns
        for j in range(y_size):  # Loops through pixels in the given column
            x = remap_interval(i, 0, x_size, -1, 1)  #Transforms the pixel grid to a graph from -1 to +1
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel  #Picks a random number
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7,15)
    green_function = build_random_function(7,15)
    blue_function = build_random_function(7,15)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)
    print("red function = ", red_function)
    print("blue function = ", blue_function)
    print("green function = ", green_function)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart.png")

    # Test that PIL is installed correctly
    # DONE: Comment or remove this function call after testing PIL install
    # test_image("noise.png")
