from src.Point.Point import *
from src.Tile import *
from src.tile_list import *
import src.a_star_path_find as aStar
from src.Settings import *
import random

MIN_MAP_SIZE = 50
MAX_MAP_SIZE = 80

MIN_ROOM_SIZE = 7
MAX_ROOM_SIZE = 12

MAX_ROOMS = 12


class Room:

    def __init__(self, x1, y1, w, h):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1 + w
        self.y2 = y1 + h

    def intersect(self, room):
        return self.x1 <= room.x2 and \
               self.x2 >= room.x1 and \
               self.y1 <= room.y2 and \
               self.y2 >= room.y1

    def center(self):
        _x = (self.x1 + self.x2) // 2
        _y = (self.y1 + self.y2) // 2


        #print('center: {0}, {1}'.format(_x, _y))
        return _x, _y


class Map:

    def __init__(self):
        self.width = random.randint(MIN_MAP_SIZE, MIN_MAP_SIZE + MAX_MAP_SIZE - MIN_MAP_SIZE)
        self.height = random.randint(MIN_MAP_SIZE, MIN_MAP_SIZE + MAX_MAP_SIZE - MIN_MAP_SIZE)
        self.body = [[Tile(BACK_TILE, False)
                      for y in range(self.width)]
                     for x in range(self.height)]
        self.roomCount = 0
        self.rooms = []

    def get_cell(self, x, y):
        return self.body[y][x]

    def get_walls(self):
        walls = []
        for y in range(self.height):
            for x in range(self.width):
                if self.body[y][x].symbol == WALL_TILE:
                    walls.append((x, y))

        return walls

    def draw_path(self, path, symb):
        for (x, y) in path:
            self.body[y][x].symbol = symb

    def room_gen(self):
        for i in range(MAX_ROOMS):
            for j in range(1000):
                room_w = MIN_ROOM_SIZE + random.randint(0, MAX_ROOM_SIZE - MIN_ROOM_SIZE)
                room_h = MIN_ROOM_SIZE + random.randint(0, MAX_ROOM_SIZE - MIN_ROOM_SIZE)
                room_x = random.randint(3, self.width - room_w - 4)
                room_y = random.randint(3, self.height - room_h - 4)

                room = Room(room_x, room_y, room_w, room_h)
                if self.roomCount == 0:
                    for y in range(room.y1, room.y2 + 1):
                        for x in range(room.x1, room.x2 + 1):
                            self.body[y][x] = Tile(FLOOR_TILE, False)
                    self.rooms.append(room)
                    self.roomCount += 1
                else:
                    ok = True
                    for c in range(self.roomCount):
                        if room.intersect(self.rooms[c]):
                            ok = False
                            break
                    if ok:
                        for y in range(room.y1, room.y2 + 1):
                            for x in range(room.x1, room.x2 + 1):
                                self.body[y][x] = Tile(FLOOR_TILE, False)
                        self.rooms.append(room)
                        self.roomCount += 1
                        break

    def set_edges(self):
        for room in self.rooms:
            self.body[room.y1][room.x1] = Tile(WALL_TILE, False)
            self.body[room.y1][room.x2] = Tile(WALL_TILE, False)
            self.body[room.y2][room.x1] = Tile(WALL_TILE, False)
            self.body[room.y2][room.x2] = Tile(WALL_TILE, False)

    def connect_two_rooms(self, room1, room2):
        finder = aStar.PathFinder(self.body)
        r1_x, r1_y = room1.center()
        r2_x, r2_y = room2.center()
        path = finder.find_path(Point(r1_x, r1_y), Point(r2_x, r2_y))
        if path:
            self.draw_path(path, ROAD_TILE)


    def connect_rooms(self):
        for i in range(0, self.roomCount - 1):
            self.connect_two_rooms(self.rooms[i], self.rooms[i + 1])

    def set_walls(self):
        for room in self.rooms:
            for i in range(room.x1, room.x2):
                if self.body[room.y1][i].symbol == ROAD_TILE:
                    continue
                self.body[room.y1][i].symbol = WALL_TILE

            for i in range(room.x1, room.x2):
                if self.body[room.y2][i].symbol == ROAD_TILE:
                    continue
                self.body[room.y2][i].symbol = WALL_TILE

            for i in range(room.y1, room.y2):
                if self.body[i][room.x1].symbol == ROAD_TILE:
                    continue
                self.body[i][room.x1].symbol = WALL_TILE

            for i in range(room.y1, room.y2):
                if self.body[i][room.x2].symbol == ROAD_TILE:
                    continue
                self.body[i][room.x2].symbol = WALL_TILE




    def set_doors(self):
        for room in self.rooms:
            for i in range(room.x1+1, room.x2):
                if (self.body[room.y1][i].symbol == ROAD_TILE) and \
                        (self.body[room.y1][i+1].symbol == WALL_TILE) and \
                        self.body[room.y1][i-1].symbol == WALL_TILE:
                    self.body[room.y1][i].symbol = DOOR_TILE

            for i in range(room.x1+1, room.x2):
                if (self.body[room.y2][i].symbol == ROAD_TILE) and \
                        (self.body[room.y2][i+1].symbol == WALL_TILE) and \
                        self.body[room.y2][i-1].symbol == WALL_TILE:
                    self.body[room.y2][i].symbol = DOOR_TILE

            for i in range(room.y1+1, room.y2):
                if (self.body[i][room.x1].symbol == ROAD_TILE) and \
                        (self.body[i+1][room.x1].symbol == WALL_TILE) and \
                        self.body[i-1][room.x1].symbol == WALL_TILE:
                    self.body[i][room.x1].symbol = DOOR_TILE

            for i in range(room.y1+1, room.y2):
                if (self.body[i][room.x2].symbol == ROAD_TILE) and \
                        (self.body[i+1][room.x2].symbol == WALL_TILE) and \
                        self.body[i-1][room.x2].symbol == WALL_TILE:
                    self.body[i][room.x2].symbol = DOOR_TILE


    def set_moreWalls(self):
        pathFinder = aStar.PathFinder(self.body)
        for y in range(self.height):
            for x in range(self.width):
                if self.body[y][x].symbol == ROAD_TILE:
                    pathFinder.neighbors.clear()
                    neighbors = pathFinder.find_more_neighbors(x, y)
                    for neighbor in neighbors:
                        if self.body[neighbor.y][neighbor.x].symbol == BACK_TILE:
                            self.body[neighbor.y][neighbor.x].symbol = WALL_TILE

    def delete_roads(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.body[y][x].symbol == ROAD_TILE:
                    self.body[y][x].symbol = FLOOR_TILE


    def generate_map(self):
        self.room_gen()
        self.set_edges()
        self.connect_rooms()
        self.set_walls()
        self.set_doors()
        self.set_moreWalls()
        self.delete_roads()

    def print_map(self, display, camera, images):
        x = y = 0
        for row in self.body:
            for t in row:
                t.draw(x, y, display, camera, images)
                x += BLOCK_WIDTH
            y += BLOCK_HEIGHT
            x = 0

    def debug_print_map(self):
        for row in self.body:
            for t in row:
                t.debug_draw()
            print()




