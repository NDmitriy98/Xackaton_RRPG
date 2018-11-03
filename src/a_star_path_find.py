import src.tile_list
import src.Tile
from src.tile_list import *
from src.Point.Point import *


class Cell(object):
    def __init__(self, x, y, reachable, g = 0, h = 0, f = 0):
        """Initialize new cell.

        @param reachable is cell reachable? not a wall?
        @param x cell x coordinate
        @param y cell y coordinate
        @param g cost to move from the starting cell to this cell.
        @param h estimation of the cost to move from this cell
                 to the ending cell.
        @param f f = g + h
        """
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = g
        self.h = h
        self.f = f

    def __lt__(self, other):
        return self.f < other.f

class PathFinder:

    def __init__(self, body):
        # open list
        self.opened = []
        # visited cells list
        self.closed = set()
        # grid cells
        self.cells = []
        self.body = body
        self.neighbors = []
        self.path = []

        self.neighbor_coef = [(0, -1), (-1, 0), (1, 0), (0, 1)]
        self.extend_neighbor_coef = [(-1, -1), (0, -1), (1, -1),
                                     (-1, 0), (1, 0),
                                     (-1, 1), (0, 1), (1, 1)]

    def lengh_between(self, p1 : Point, p2 : Point):
        xDiff = 0
        yDiff = 0
        if p1.x >= p2.x:
            xDiff = p1.x - p2.x
        else:
            xDiff = p2.x - p1.x

        if p1.y >= p2.y:
            yDiff = p1.y - p2.y
        else:
            yDiff = p2.y - p1.y

        return xDiff + yDiff

    def check_coord(self, x, y):
        if x < 0 or x >= len(self.body[0]):
            return False
        elif y < 0 or y >= len(self.body):
            return False
        else:
            return True

    def min_f(self):
        if len(self.opened) == 0:
            return -1
        minF = self.opened[0].f
        index = 0
        for i, o in enumerate(self.opened):
            if o.f <= minF:
                minF = o.f
                index = i
        #print('min f: ' + str(minF))
        #print('at ({0},{1})'.format(self.opened[index].x, self.opened[index].y))
        return index

    def find_index(self, vec, cell : Cell):

        for i, v in enumerate(vec):
            if v.x == cell.x and v.y == cell.y:
                return i

    def in_vector(self, vec, cell : Cell):
        for v in vec:
            if v.x == cell.x and v.y == cell.y:
                return True
        return False

    def find_neighbors(self, x, y):
        self.neighbors.clear()
        if not self.check_coord(x, y):
            return

        for n_coef in self.neighbor_coef:
            n_x = n_coef[0] + x
            n_y = n_coef[1] + y

            if not self.check_coord(n_x, n_y):
                continue
            else:
                neighbor = Cell(n_x, n_y, True)
                self.neighbors.append(neighbor)

    def find_more_neighbors(self, x, y):
        n_points = []
        self.neighbors.clear()
        if not self.check_coord(x, y):
            return

        for n_coef in self.extend_neighbor_coef:
            n_x = n_coef[0] + x
            n_y = n_coef[1] + y

            if not self.check_coord(n_x, n_y):
                continue
            else:
                neighbor = Cell(n_x, n_y, True)
                self.neighbors.append(neighbor)
                neighborPoint = Point(n_x, n_y)
                n_points.append(neighborPoint)
        return n_points

    def reconstruct_path(self, start : Cell, finish : Cell):
        self.path.clear()
        curr_cell = finish
        while curr_cell != None:
            self.path.append((curr_cell.x, curr_cell.y))
            curr_cell = curr_cell.parent

    def print_body(self, _body):
        for x, row in enumerate(_body):
            print('{:>2}'.format(x), end='')
            for t in row:
                t.draw()
            print()

    def draw_path(self):
        temp_body = self.body
        for p in self.path:
            temp_body[p[0]][p[1]].symbol = ROAD_TILE
        self.print_body(temp_body)

    def print_path(self):
        temp_body = self.body
        for p in self.opened:
            temp_body[p.y][p.x].symbol = 'O'
        for p in self.closed:
            temp_body[p.y][p.x].symbol = 'C'
        self.print_body(temp_body)

    def find_path(self, start : Point, finish : Point):
        start_cell = Cell(start.x, start.y, True)
        start_cell.g = 0
        start_cell.h = self.lengh_between(start, finish)
        start_cell.f = start_cell.g + start_cell.h

        finish_cell = Cell(finish.x, finish.y, True)
        finish_cell.g = 0
        finish_cell.h = 0
        finish_cell.f = 0

        self.closed.clear()
        self.opened.clear()
        self.opened.append(start_cell)

        while len(self.opened) != 0:
            x = self.opened[self.min_f()]
            if x.x == finish.x and x.y == finish.y:
                self.reconstruct_path(start_cell, x)
                return self.path
            self.opened.remove(x)
            self.closed.add(x)

            self.neighbors.clear()
            self.find_neighbors(x.x, x.y)

            for neighbor in self.neighbors:
                if neighbor in self.closed:
                    continue
                if self.body[neighbor.y][neighbor.x].symbol == WALL_TILE:
                    self.closed.add(neighbor)
                    continue

                tentative_g_score = x.g + self.lengh_between(Point(x.x, x.y), Point(neighbor.x, neighbor.y))
                tentative_is_better = True

                if not self.in_vector(self.opened, neighbor):
                    tentative_is_better = True
                else:
                    tentative_is_better = tentative_g_score <= neighbor.g

                if tentative_is_better:
                    neighbor.parent = x
                    neighbor.g = tentative_g_score
                    neighbor.h = self.lengh_between(Point(neighbor.x, neighbor.y), finish)
                    neighbor.f = neighbor.h + neighbor.g
                    self.opened.append(neighbor)


            #self.print_path()
        return None



        


