from pico2d import *
import framework
import Game_world
import time
import pickle
from Background import Background
from UI import UI
from Furniture import Furniture, Cookware, FoodBox
from Wall import Wall
from Charater import Charater
import pause_mode
from Game_data import Raw_food, Cookwares


def handle_events():
    global charater
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_0:
            framework.push_mode(pause_mode)
        else:
            charater.handle_event(event)

def init():
    global Ui, charater, foods, counter, cookwares, orders, walls#충돌하는 물체만

    
    background = Background()
    Game_world.add_object(background,0)
    Ui = UI()
    Game_world.add_object(Ui,2)

    counter = Furniture('counter', get_canvas_width()*4/5, get_canvas_height()/3, get_canvas_width()*15/16, get_canvas_height()*2/3)#음식 투입구
    Game_world.add_object(counter,0)
    Game_world.add_collision_pair('charater:counter',None,counter)



    walls = [Wall(0,0,get_canvas_width(),100)]
    walls.append(Wall(get_canvas_width()*4/5,100, (get_canvas_width()*7)/8,get_canvas_height()/3))
    walls.append(Wall(get_canvas_width()*13/15,get_canvas_height()/4, get_canvas_width()*15/16,get_canvas_height()*3/4))
    walls.append(Wall(get_canvas_width()*4/5,get_canvas_height()*2/3, get_canvas_width()*7/8,get_canvas_height()))
    Game_world.add_objects(walls,0)
    for wall in walls:
        Game_world.add_collision_pair('charater:wall',None,wall)

    #       캐릭터,조리도구,음식
    # 플레이어 캐릭터  
    charater = Charater()
    Game_world.add_object(charater,1)
    Game_world.add_collision_pair('charater:cookware',charater,None)
    Game_world.add_collision_pair('charater:counter',charater,None)
    Game_world.add_collision_pair('charater:food',charater,None)
    Game_world.add_collision_pair('charater:wall',charater,None)
    # 조리도구
    cookwares = [Cookware(Cookwares[i],30, i * 60 + 300, 60,60) for i in range(len(Cookwares))]
    Game_world.add_objects(cookwares,0)
    for cookware in cookwares:
        Game_world.add_collision_pair('charater:cookware',None,cookware)  
    
    #음식
    foodboxs=[FoodBox(Raw_food[i], 30+i * 60 , get_canvas_height()-180, 60,60) for i in range(len(Raw_food))]
    Game_world.add_objects(foodboxs,0)


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
    #UI시간 멈추기
    global pausetime
    pausetime = time.time()
    pass

def resume():
    #멈춘 시간만큼 UI시간 수정
    pause = time.time() - pausetime
    Ui.timer = Ui.timer + pause
    
