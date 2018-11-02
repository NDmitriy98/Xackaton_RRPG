from src.Point.Point import *
from src.Tile import *
import random

MIN_MAP_SIZE = 50
MAX_MAP_SIZE = 80

MIN_ROOM_SIZE = 5
MAX_ROOM_SIZE = 12

MAX_ROOMS = 12

class Room:

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def intersect(self, room):
        return self.x1 <= room.x2 and \
               self.x2 >= room.x1 and \
               self.y1 <= room.y2 and \
               self.y2 >= room.y1
    


    @property
    def center(self):
        c: Point
        c.x = (self.x1 + self.x2) / 2
        c.x = (self.y2 + self.y2) / 2
        return c


class Map:


    def __init__(self):
        self.width = random.randint(MIN_MAP_SIZE, MAX_MAP_SIZE - MIN_MAP_SIZE)
        self.height = random.randint(MIN_MAP_SIZE, MAX_MAP_SIZE - MIN_MAP_SIZE)
        self.body = [[Tile(BACK_TILE, False)
                      for y in range(self.height) ]
                        for x in range(self.width)]
        self.roomCount = 0
        self.rooms = []

    def roomGen(self):
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





