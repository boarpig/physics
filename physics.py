#!/usr/bin/python2 -d
# coding: utf8

# Created by Lauri Hakko
# This code is public domain

import pyglet
from pyglet.window import key
import sys, math, time

window = pyglet.window.Window(width=800, height=480)

kappale_lista = []
drag_begin = (0.0, 0.0)
paused = True

class kappale:
    
    def __init__(self, paikka, massa, speed=[0.0, 0.0], mobility=True):
        self.mobile = mobility
        self.nopeus = speed
        self.circ = pyglet.resource.image('pallo.png')
        self.mass = float(str(massa))
        self.position = [float(str(paikka[0])), float(str(paikka[1]))]
        self.circ.blit(paikka[0], paikka[1])

    def __str__(self):
        return str([self.mass, self.position])

    def move(self):
        print "lol"


def getDistance(obj1, obj2):
    'calculate distance between first and second object'
    x = obj2.position[0] - obj1.position[0]
    y = obj2.position[1] - obj1.position[1]
    return [float(x),float(y)]

def getForce(obj1, obj2):
    'Calculates the gravitational force between two objects'
    g = float("6.67259e-11")
    distTuple = getDistance(obj1, obj2)
    distance = float(str(math.sqrt(distTuple[0]**2 + distTuple[1]**2)))
    if distance < 16:
        return [0,0]
    else:
        N = g * (obj1.mass * obj2.mass / distance**2)
        xAccel = N * (distTuple[0] / (abs(distTuple[1])+abs(distTuple[0]))) / 2 / obj1.mass
        yAccel = N * (distTuple[1] / (abs(distTuple[1])+abs(distTuple[0]))) / 2 / obj1.mass
        return [xAccel, yAccel]

@window.event
def on_mouse_press(x, y, button, modifiers):
    global drag_begin
    if button == pyglet.window.mouse.LEFT:
        drag_begin = (x, y)

@window.event
def on_mouse_release(x, y, button, modifiers):
    global drag_begin
    if button == pyglet.window.mouse.LEFT:
        if drag_begin:
            nopeus = [(x-drag_begin[0])/10, (y-drag_begin[1])/10]
            if modifiers & key.MOD_CTRL:
                kappale_lista.append(kappale([drag_begin[0],drag_begin[1]], 6e13, nopeus, False))
            else:
                kappale_lista.append(kappale([drag_begin[0],drag_begin[1]], 6e13, nopeus))
            drag_begin = None

@window.event
def on_key_release(symbol, modifiers):
    global paused
    global kappale_lista
    if symbol == key.F5:
        paused = False
    elif symbol == key.F9:
        paused = True
    elif symbol == key.DELETE:
        kappale_lista = []
        paused = True

@window.event
def on_draw():
    window.clear()
    for i,kappale1 in enumerate(kappale_lista):
        if not paused and kappale1.mobile:
            if kappale1.position[0] > 2000 or kappale1.position[1] > 2000 or \
               kappale1.position[0] < -2000 or kappale1.position[1] < -2000:
                del kappale_lista[i]
            else:
                kappale1.position[0] += kappale1.nopeus[0]
                kappale1.position[1] += kappale1.nopeus[1]
        kappale1.circ.blit(int(kappale1.position[0]), int(kappale1.position[1]))

def calc(args):
    global kappale_lista
    if len(kappale_lista) > 0:
        if not paused:
            for i,eka in enumerate(kappale_lista):
                for j, toka in enumerate(kappale_lista):
                    if i != j:
                        force = getForce(eka, toka)
                        eka.nopeus[0] += force[0]
                        eka.nopeus[1] += force[1]
        

pyglet.clock.schedule_interval(calc, 0.01)

pyglet.app.run()
