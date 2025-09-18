import pygame as pg
from Vec import *


class Inputs:
    def __init__(self):
        self.keysPressed = set()
        self.keysReleased = set()
        self.keysHolding = set()
        self.isResized = False
        self.quit = False
        self.k2pg = {}
        self.compute_pg2keys()
        self.mouse_pos = Vec(0, 0)
        self.mouse_pressed = False
        self.new_screen_size = Vec(0, 0)

        self.game_events = {}

    def compute_pg2keys(self):
        self.k2pg = {}
        for pg_k in pg.__dict__:
            if pg_k[:2] == "K_":
                self.k2pg[pg_k[2:]] = pg.__dict__[pg_k]

    def update(self):
        self.keysPressed = set()
        self.keysReleased = set()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True
            elif event.type == pg.KEYDOWN:
                self.keysPressed.add(event.key)
                self.keysHolding.add(event.key)
            elif event.type == pg.KEYUP:
                self.keysReleased.add(event.key)
                self.keysHolding.remove(event.key)
            elif event.type == pg.VIDEORESIZE:
                self.isResized = True
                self.new_screen_size = Vec(*event.dict['size'])
        self.mouse_pressed = pg.mouse.get_pressed()[0]
        self.mouse_pos = Vec(*pg.mouse.get_pos())

    def get_pressed(self, key):
        return self.k2pg[key] in self.keysPressed

    def get_released(self, key):
        return self.k2pg[key] in self.keysReleased

    def get_holding(self, key):
        return self.k2pg[key] in self.keysHolding

    def get_resized(self):
        if self.isResized:
            self.isResized = False
            return True
        return False

    def add_event(self, event, parameters):
        self.game_events[event] = parameters

    def exist_event(self, event):
        return event in self.game_events
