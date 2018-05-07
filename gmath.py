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
    color = [0, 0, 0]
    for i in range(len(color)):
        color[i] = a[i] + d[i] + s[i]
    return limit_color(color)

def calculate_ambient(alight, areflect):
    acolor = [0, 0, 0]
    for i in range(len(acolor)):
        acolor[i] = alight[i] * areflect[i]
    return limit_color(acolor)

def calculate_diffuse(light, dreflect, normal):
    dcolor = [0, 0, 0]
    lvector = normalize(light[LOCATION])
    lcolor = light[COLOR]
    for i in range(len(dcolor)):
        dcolor[i] = lcolor[i] * dreflect[i] * dot_product(lvector, normalize(normal))
    return limit_color(dcolor)

def calculate_specular(light, sreflect, view, normal):
    scolor = [0, 0, 0]
    temp = [0, 0, 0]
    lvector = light[LOCATION]
    lcolor = light[COLOR]
    k = 2 * dot_product(lvector, normal)
    for i in range(len(temp)):
        temp[i] = k * normal[i] - lvector[i]
    k = (dot_product(temp,view)) ** 16
    for i in range(len(scolor)):
        scolor[i] = lcolor[i] * sreflect[i] * k
    return limit_color(scolor)

def limit_color(color):
    for i in range(len(color)):
        color[i] = int(color[i])
        if color[i] < 0:
            color[i] = 0
        elif color[i] > 255:
            color[i] = 255
    return color

#vector functions
def normalize(vector):
    mag = (vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2) ** 0.5
    return [vector[0]/mag, vector[1]/mag, vector[2]/mag]

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
