import math
from display import *

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    a = calculate_ambient(ambient, areflect)
    d = calculate_diffuse(light, dreflect, normal)
    s = calculate_specular(light, sreflect, view, normal)
    color = [x + y + z for x, y, z in zip(a, d, s)]
    return limit_color(color)

def calculate_ambient(alight, areflect):
    acolor = [int(x * y) for x, y in zip(alight, areflect)]
    return limit_color(acolor)

def calculate_diffuse(light, dreflect, normal):
    dot = dot_product(normalize(normal), normalize(light[LOCATION]))
    dcolor = [int(x * y * dot) for x, y in zip(light[COLOR],dreflect)]
    return limit_color(dcolor)

def calculate_specular(light, sreflect, view, normal):
    scolor = [x * y for x, y in zip(light[COLOR], sreflect)]
    l = normalize(light[LOCATION])
    v = normalize(view)
    n = normalize(normal)
    a = [x * 2 * dot_product(n, l) for x in n]
    b = [x - y for x,y in zip(a,l)]
    c = [int(x * (dot_product(b, v) ** 16)) for x in scolor]
    if dot_product(n, l) <= 0:
        return [0, 0, 0]
    return limit_color(c)

def limit_color(color):
    for i in range(len(color)):
        if color[i] < 0:
            color[i] = 0
        elif color[i] > 255:
            color[i] = 255
    return color

#vector functions
def normalize(vector):
    mag = (vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2) ** 0.5
    return [x / mag for x in vector]

def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
