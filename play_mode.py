from pico2d import *
import framework
import Game_world

from Background import Background
from Foods import Foods
from Furniture import Furniture
from Charater import Charater



Ingredient = list({'fish', 'fruit', 'sashimi', 'spare', 'steak', 'sushi'})#음식의 종류

def handle_events():
    global charater
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            framework.quit()
        else:
            charater.handle_event(event)

def init():
    global charater, foods, counter#충돌하는 물체만
    background = Background('background')
    Game_world.add_object(background,0)

    floor = Background('floor')
    Game_world.add_object(floor,0)
    
    countertop = Furniture('table', 750, 100)#테이블
    Game_world.add_object(countertop,0)

    counter = Furniture('counter', 650, 200)#음식 투입구
    Game_world.add_object(counter,0)
    Game_world.add_collision_pair('charater:counter',None,counter)


    foods = [Foods(Ingredient[i], i * 100 + 50, 100) for i in range(len(Ingredient))]#음식들
    Game_world.add_objects(foods,1)
    for food in foods:
        Game_world.add_collision_pair('charater:food',None,food)

    charater = Charater()# 플레이어 캐릭터
    Game_world.add_object(charater,1)
    Game_world.add_collision_pair('charater:counter',charater,None)
    Game_world.add_collision_pair('charater:food',charater,None)




def finish():
    Game_world.clear()
    pass


def update():
    Game_world.update()
    Game_world.handle_collision()


def draw():
    clear_canvas()
    Game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

