from pico2d import *

from Background import Background
from Foods import Foods
from Furniture import Furniture
from Charater import Charater


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
    global running, world, background, floor, countertop, counter, food, charater
    running = True
    world=[]# 먼저 선언한 것이 뒤로

    background = Background('background')
    world.append(background)

    floor = Background('floor')
    world.append(floor)


    
    countertop = Furniture('table', 750, 100)#테이블
    world.append(countertop)

    counter = Furniture('counter', 650, 200)#음식 투입구
    world.append(counter)
    
    food = [Foods(Ingredient[i],i * 100 + 50, 50) for i in range(len(Ingredient))]#음식들
    world += food

    charater = Charater()# 플레이어 캐릭터
    world.append(charater)


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
    delay(1)

close_canvas()
