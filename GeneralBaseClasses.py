from OpenGL.GL import *
from OpenGL.GLUT import *
from math import sqrt, pow, acos, degrees, pi, sin, cos


class Color:
    """
    x
    """

    def __init__(self, r=0, g=0, b=0, a=1):
        self.r = r/255
        self.g = g/255
        self.b = b/255
        self.a = a

    def alter_color(self, col, measure):
        """

        :param col:
        :param measure:
        :return:
        """
        if col == "r":
            self.r += measure/255
        elif col == "g":
            self.r += measure/255
        elif col == "b":
            self.r += measure / 255
        else:
            print("WRONG COLOR AS AN ARGUMENT, ONLY r, g or b IS ACCEPTABLE!!!")


def color_factory(colors):
    """
    Create Color from a list, e.g: colors = [100, 20, 50]
    :param colors:
    :return: Color
    """
    if len(colors) == 4:
        return Color(colors[0], colors[1], colors[2], colors[3])
    return Color(colors[0], colors[1], colors[2], 1)


class Vector:
    """
    x
    """
    def __init__(self, x0=0.0, y0=0.0, z0=0.0):
        self.x = x0
        self.y = y0
        self.z = z0

    def __str__(self):
        return "({0},{1},{2})".format(self.x, self.y, self.z)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vector(x, y, z)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vector(x, y, z)

    def __mul__(self, other):
        # dot product
        # if isinstance(other, self.__class__):
            x = self.x * other.x
            y = self.y * other.y
            z = self.z * other.z
            return x+y+z
        # else:
        #     self.x = self.x * other
        #     self.y = self.y * other
        #     self.z = self.z * other
            # return x+y+z

    def scalar_multi(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def __mod__(self, other):
        # cross product
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vector(x, y, z)

    def length(self):
        return sqrt(pow(self.x, 2)+pow(self.y, 2)+pow(self.z, 2))

    def div(self, num):
        return Vector(self.x/num, self.y/num, self.z/num)

    def normalize(self):
        le = self.length()
        x = self.x / le
        y = self.y / le
        z = self.z / le
        return Vector(x, y, z)


def vector_factory(coord):
    vectors = []
    for c in coord:
        vectors.append(Vector(c[0], c[1], c[2] if len(c) > 2 else 0.0))
    return vectors


def vector_from_list(coord):
    if len(coord) > 2:
        return Vector(coord[0], coord[1], coord[2])
    else:
        return Vector(coord[0], coord[1], 0.0)


def create_vectors_for_triangleset(coord):
    vectors = []
    for c in coord:
        vectors.append(vector_factory(c))
    return vectors


def is_convex(a, b, c):
    # only convex if traversing anti-clockwise!
    crossp = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)
    if crossp >= 0:
        return True
    return False


def in_triangle(a, b, c, p):
    L = [0, 0, 0]
    eps = 0.0000001
    # calculate barycentric coefficients for point p
    # eps is needed as error correction since for very small distances denom->0
    L[0] = ((b.y - c.y) * (p.x - c.x) + (c.x - b.x) * (p.y - c.y)) \
           / (((b.y - c.y) * (a.x - c.x) + (c.x - b.x) * (a.y - c.y)) + eps)
    L[1] = ((c.y - a.y) * (p.x - c.x) + (a.x - c.x) * (p.y - c.y)) \
           / (((b.y - c.y) * (a.x - c.x) + (c.x - b.x) * (a.y - c.y)) + eps)
    L[2] = 1 - L[0] - L[1]
    # check if p lies in triangle (a, b, c)
    for x in L:
        if x > 1 or x < 0:
            return False
    return True


def is_clockwise(poly):
    # initialize sum with last element
    sum = (poly[0].x - poly[len(poly) - 1].x) * (poly[0].y + poly[len(poly) - 1].y)
    # iterate over all other elements (0 to n-1)
    for i in range(len(poly) - 1):
        sum += (poly[i + 1].x - poly[i].x) * (poly[i + 1].y + poly[i].y)
    if sum > 0:
        return True
    return False


def get_ear(poly):
    size = len(poly)
    if size < 3:
        return []
    if size == 3:
        tri = (poly[0], poly[1], poly[2])
        del poly[:]
        return list(tri)
    for i in range(size):
        tritest = False
        p1 = poly[(i - 1) % size]
        p2 = poly[i % size]
        p3 = poly[(i + 1) % size]
        if is_convex(p1, p2, p3):
            for x in poly:
                if not (x in (p1, p2, p3)) and in_triangle(p1, p2, p3, x):
                    tritest = True
            if not tritest:
                del poly[i % size]
                return [p1, p2, p3]
    return []


class Drawable:
    def from_dict(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)

    def set_color(self, new_r, new_g, new_b, new_a=1):
        self.color.r = new_r / 255
        self.color.g = new_g / 255
        self.color.b = new_b / 255
        self.color.a = new_a


class Rectangle(Drawable):
    """
    Cube class can be drawn as a filled rectangle or unfilled rectangle
    """
    def __init__(self, element_id=None, coordinates=Vector(0.0, 0.0, 0.0), a=0.0, b=0.0,
                 color=Color(r=100, g=100, b=100), filled=False):
        self.id = element_id
        self.color = color
        self.coordinates = coordinates
        self.a = a
        self.b = b
        self.filled = filled

    def convert(self):
        """
        Convert x,y,a,b to Vectors
        :return:
        """
        return [Vector(self.coordinates.x - self.a / 2, self.coordinates.y - self.b / 2, 0),
                Vector(self.coordinates.x + self.a / 2, self.coordinates.y - self.b / 2, 0),
                Vector(self.coordinates.x + self.a / 2, self.coordinates.y + self.b / 2, 0),
                Vector(self.coordinates.x - self.a / 2, self.coordinates.y + self.b / 2, 0)]

    def draw(self):
        """
        :return:
        """
        glColor4f(self.color.r, self.color.g, self.color.b, self.color.a)
        if self.filled:
            glBegin(GL_POLYGON)
        else:
            glBegin(GL_LINE_LOOP)
        for c in self.convert():
            glVertex3f(c.x, c.y, c.z)
        glEnd()


class Cube(Drawable):
    """
    Cube class can be drawn as a filled rectangle or unfilled rectangle
    """
    def __init__(self, element_id=None, coordinates=Vector(0, 0, 0), side=[0, 0, 0], rotate=[0, 0, 0, 0],
                 color=Color(r=100, g=100, b=100), filled=True):
        self.id = element_id
        self.color = color
        self.coordinates = coordinates
        self.side = side
        self.rotate = rotate
        self.filled = filled

    def convert(self):
        """
        :return:
        """
        return [Vector(self.coordinates.x - self.side[0] / 2, self.coordinates.y - self.side[0] / 2, 0),
                Vector(self.coordinates.x + self.side[0] / 2, self.coordinates.y - self.side[0] / 2, 0),
                Vector(self.coordinates.x + self.side[0] / 2, self.coordinates.y + self.side[0] / 2, 0),
                Vector(self.coordinates.x - self.side[0] / 2, self.coordinates.y + self.side[0] / 2, 0)]

    def alter_color(self, measure):
        """
        :param measure:
        :return:
        """
        self.color.alter_color("g", measure)

    def draw(self):
        """

        :return:
        """
        glColor4f(self.color.r, self.color.g, self.color.b, self.color.a)
        if self.filled:
            glBegin(GL_POLYGON)
        else:
            glBegin(GL_LINE_LOOP)
        for c in self.convert():
            glVertex3f(c.x, c.y, c.z)
        glEnd()

    def draw3d(self):
        """

        :return:
        """
        glColor4f(self.color.r, self.color.g, self.color.b, self.color.a)
        glPushMatrix()
        glTranslatef(self.coordinates.x, self.coordinates.y, self.coordinates.z)
        glRotatef(self.rotate[0], self.rotate[1], self.rotate[2], self.rotate[3])
        glScalef(self.side[0], self.side[1], self.side[2])
        glutSolidCube(1.0)
        glPopMatrix()


class Polyline(Drawable):
    """
    """
    def __init__(self, element_id=None, coordinates=Vector(), width=1, filled=False,
                 color=Color(r=100, g=80, b=80, a=1)):
        self. id = element_id
        self.coordinates = coordinates
        self.width = width
        self.filled = filled
        self.color = color

    def draw(self):
        """

        :return:
        """

        glColor4f(self.color.r, self.color.g, self.color.b, self.color.a)
        glNormal3f(0, 0, 1)
        glLineWidth(self.width)
        if self.filled:
            glBegin(GL_TRIANGLES)
            coord = self.coordinates[::-1] if is_clockwise(self.coordinates) else self.coordinates[:]
            while len(coord) >= 3:
                vertex = get_ear(coord)
                if len(vertex) == 0:
                    break
                glColor4f(self.color.r, self.color.g, self.color.b, self.color.a)
                for v in vertex:
                    glVertex3f(v.x, v.y, v.z)
            glEnd()
        else:
            glBegin(GL_LINE_STRIP)
            for c in self.coordinates:
                glVertex3f(c.x, c.y, c.z)
            glEnd()
        glLineWidth(1.0)


class Grid(Drawable):
    """
    Measurement class
    If type is grid, it generates a grid
    If type is axis, it generates x and y axis
    """

    def __init__(self, element_id=None, coordinates=Vector(0, 0, 0), scale=1, color=Color(r=40, g=40, b=40),
                 width=600, height=600, m_type="grid", zoom = 1):
        self.id = element_id
        self.coordinates = coordinates
        self.scale = scale
        self.color = color
        self.width = width
        self.height = height
        self.type = m_type
        self.zoom = zoom

    def draw(self):
        """

        :return:
        """
        if self.type == "grid" or self.type == "axis":
            glPushMatrix()
            glTranslatef(self.coordinates.x, self.coordinates.y, self.coordinates.z)
            glColor4f(self.color.r, self.color.g, self.color.b, self.color.a)
            glNormal3f(0, 0, 1)
            glBegin(GL_LINES)
            glVertex3f(-self.width/2, 0, 0)
            glVertex3f(self.width / 2, 0, 0)
            glVertex3f(0, -self.height/2, 0)
            glVertex3f(0, self.height / 2, 0)
            if self.type == "grid":
                width = self.width
                height = self.height
            else:
                width = self.width*self.zoom/200
                height = self.height*self.zoom/200

            final_y = int(round((self.height/2)/self.scale))
            for h in range(0, final_y):
                glVertex3f(-width / 2, h * self.scale, 0)
                glVertex3f(width / 2, h * self.scale, 0)
                glVertex3f(-width / 2, -h * self.scale, 0)
                glVertex3f(width / 2, -h * self.scale, 0)

            final_x = int(round((self.width/2)/self.scale))
            for w in range(0, final_x):
                glVertex3f(w * self.scale, -height / 2, 0)
                glVertex3f(w * self.scale, height / 2, 0)
                glVertex3f(-w * self.scale, -height / 2, 0)
                glVertex3f(-w * self.scale, height / 2, 0)
            glEnd()
            glPopMatrix()


class MatrixObject:
    def __init__(self, matrix=[], color=Color(r=255, g=0, b=0), type="solid"):
        self.matrix = matrix
        self.color = color
        self.type = type

    def draw_dots(self):
        glDisable(GL_LIGHTING)
        glBegin(GL_POINTS)
        for row in self.matrix:
            for element in row:
                glVertex3f(element.x, element.y, element.z)
        glEnd()
        glEnable(GL_LIGHTING)

    def draw_lines(self):
        glDisable(GL_LIGHTING)
        row = len(self.matrix)
        column = len(self.matrix[0])

        for c in range(0, column):
            glBegin(GL_LINE_STRIP)
            for r in range(0, row):
                glVertex3f(self.matrix[r][c].x, self.matrix[r][c].y, self.matrix[r][c].z)
            glEnd()

        for r in range(0, row):
            glBegin(GL_LINE_STRIP)
            for c in range(0, column):
                glVertex3f(self.matrix[r][c].x, self.matrix[r][c].y, self.matrix[r][c].z)
            glEnd()
        glEnable(GL_LIGHTING)

    def draw_solid(self):
        row = len(self.matrix)
        column = len(self.matrix[0])

        for r in range(0, row-1):
            glBegin(GL_TRIANGLES)
            for c in range(0, column-1):
                normal = ((self.matrix[r][c + 1] - self.matrix[r][c]) %
                          (self.matrix[r + 1][c] - self.matrix[r][c])).normalize()
                glNormal3f(normal.x, normal.y, normal.z)
                glVertex3f(self.matrix[r][c].x, self.matrix[r][c].y, self.matrix[r][c].z)
                glVertex3f(self.matrix[r][c + 1].x, self.matrix[r][c + 1].y, self.matrix[r][c + 1].z)
                glVertex3f(self.matrix[r + 1][c].x, self.matrix[r + 1][c].y, self.matrix[r + 1][c].z)

                normal = ((self.matrix[r + 1][c + 1] - self.matrix[r][c + 1]) %
                          (self.matrix[r + 1][c] - self.matrix[r][c + 1])).normalize()
                glNormal3f(normal.x, normal.y, normal.z)
                glVertex3f(self.matrix[r][c + 1].x, self.matrix[r][c + 1].y, self.matrix[r][c + 1].z)
                glVertex3f(self.matrix[r + 1][c + 1].x, self.matrix[r + 1][c + 1].y, self.matrix[r + 1][c + 1].z)
                glVertex3f(self.matrix[r + 1][c].x, self.matrix[r + 1][c].y, self.matrix[r + 1][c].z)

            glEnd()

    def draw3d(self):
        glColor4f(self.color.r, self.color.g, self.color.b, self.color.a)
        if self.type is "dot":
            self.draw_dots()
        elif self.type is "line":
            self.draw_lines()
        elif self.type is "solid":
            self.draw_solid()

        else:
            raise TypeError("Bad matrix type")


class Sphere(Drawable):
    def __init__(self, element_id=None, coordinates=Vector(0.0, 0.0, 0.0), radius=0.0, color=Color(r=100, g=100, b=100),
                 filled=True):
        self.id = element_id
        self.color = color
        self.coordinates = coordinates
        self.radius = radius
        self.filled = filled

    def draw(self):
        glColor4f(self.color.r, self.color.g, self.color.b, self.color.a)
        triangle_amount = 100
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(self.coordinates.x, self.coordinates.y, self.coordinates.z)
        for i in range(0, triangle_amount+1):
            glVertex2f(self.coordinates.x + (self.radius * cos(i * 2 * pi / triangle_amount)),
                       self.coordinates.y + (self.radius * sin(i * 2 * pi / triangle_amount)))
        glEnd()

    def draw3d(self):
        """

        :return:
        """
        glColor4f(self.color.r, self.color.g, self.color.b, self.color.a)
        glPushMatrix()
        glTranslatef(self.coordinates.x, self.coordinates.y, self.coordinates.z)
        # glScalef(self.a, self.b, self.c)
        glutSolidSphere(self.radius, 100, 100)
        glPopMatrix()


class Cylinder(Drawable):
    def __init__(self, p1=Vector(20, 0, 0), p2=Vector(20, 0, 0), radius=3, color=Color(r=255, g=255, b=0),
                 type="solid"):
        self.p1 = p1
        self.p2 = p2
        self.radius = radius
        self.color = color
        self.type = type

    def height(self):
        return sqrt(pow(self.p2.x-self.p1.x, 2)+pow(self.p2.y-self.p1.y, 2)+pow(self.p2.z-self.p1.z, 2))

    def angle(self, p=Vector(), q=Vector()):
        return degrees(acos((p*q)/(p.length()*q.length())))

    def draw3d(self):
        """

        :return:
        """
        glColor4f(self.color.r, self.color.g, self.color.b, self.color.a)
        glPushMatrix()
        glTranslatef(self.p1.x, self.p1.y, self.p1.z)
        axis = Vector(0, 0, 1) % (self.p2 - self.p1)
        glRotatef(self.angle(self.p2-self.p1, Vector(0, 0, 1)), axis.x, axis.y, axis.z)
        glutSolidCylinder(self.radius, self.height(), 100, 100)
        glPopMatrix()



class LineSet(Drawable):
    def __init__(self, vector_list=[], radius=0):
        self.vectors = vector_list
        self.radius = radius

    def draw3d(self):
        # [[p1, p2], [p2, p3]]
        if self.radius > 0:
            for element in self.vectors:
                Sphere(element[0], self.radius).draw3d()
                Cylinder(element[0], element[1], self.radius).draw3d()
        else:
            glBegin(GL_LINES)
            for element in self.vectors:
                glVertex3f(element[0].x, element[0].y, element[0].z)
                glVertex3f(element[1].x, element[1].y, element[1].z)
            glEnd()


class TriangleSet(Drawable):
    def __init__(self, element_id=None, coordinates=Vector(), filled=True, color=Color(r=100, g=80, b=80, a=1)):
        self. id = element_id
        self.coordinates = coordinates
        self.filled = filled
        self.color = color

    def draw3d(self):
        for element in self.coordinates:
            normal = ((element[1] - element[0]).normalize() % (element[2] - element[0]).normalize()).normalize()

            glColor4f(self.color.r, self.color.g, self.color.b, self.color.a)
            if self.filled:
                glBegin(GL_TRIANGLES)
            else:
                glBegin(GL_LINE_LOOP)
            glNormal3f(normal.x, normal.y, normal.z)
            glVertex3f(element[0].x, element[0].y, element[0].z)
            glVertex3f(element[1].x, element[1].y, element[1].z)
            glVertex3f(element[2].x, element[2].y, element[2].z)
            glEnd()


class Route(Drawable):
    def __init__(self, src, dst, width, color):
        self.src = src
        self.dst = dst
        self.width = width
        self.color = color

    def _get_coords(self):
        norm = Vector(self.dst.y-self.src.y, -(self.dst.x-self.src.x)).normalize()
        return [self.src+norm.scalar_multi(self.width/2), self.src-norm.scalar_multi(self.width/2),
                self.dst-norm.scalar_multi(self.width/2), self.dst+norm.scalar_multi(self.width/2)]

    def draw(self):
        glColor4f(self.color.r, self.color.g, self.color.b, self.color.a)
        glBegin(GL_POLYGON)
        for coord in self._get_coords():
            glVertex3f(coord.x, coord.y, coord.z)
        glEnd()
