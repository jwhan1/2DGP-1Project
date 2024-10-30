from pico2d import *

from Background import Background
from Foods import Foods
from Furniture import Furniture

Ingredient = list({'fish', 'fruit', 'sashimi', 'spare', 'steak', 'sushi'})

def update_world():
    for o in world:
        o.update()

def rander_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

def reset_world():
    global running, world, food, background, floor, countertop, counter
    running = True
    world=[]

    background = Background('background')
    world.append(background)

    floor = Background('floor')
    world.append(floor)

    food = [Foods(Ingredient[i],i * 100 + 50, 50) for i in range(len(Ingredient))]#음식들
    world += food
    
    countertop = Furniture('table', 750, 100)#테이블
    world.append(countertop)

    counter = Furniture('counter', 650, 200)#음식 투입구
    world.append(counter)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

open_canvas()

reset_world()
while running:
    handle_events()
    update_world()
    rander_world()
    delay(0.01)

close_canvas()
