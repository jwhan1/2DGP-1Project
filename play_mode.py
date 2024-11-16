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
    background = Background()
    Game_world.add_object(background,0)
    

    counter = Furniture('counter', 650, 200,100,200)#음식 투입구
    Game_world.add_object(counter,0)
    Game_world.add_collision_pair('charater:counter',None,counter)

    chopping_board = Furniture('chopping_board', 350, 200,60,60)#도마
    Game_world.add_object(chopping_board,0)
    Game_world.add_collision_pair('charater:cookware',None,chopping_board)  

    cooking_pot = Furniture('cooking_pot', 250, 200,60,60)#냄비
    Game_world.add_object(cooking_pot,0)
    Game_world.add_collision_pair('charater:cookware',None,cooking_pot)  

    frying_pan = Furniture('frying_pan', 150, 200,60,60)#프라이팬
    Game_world.add_object(frying_pan,0)
    Game_world.add_collision_pair('charater:cookware',None,frying_pan)  

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

