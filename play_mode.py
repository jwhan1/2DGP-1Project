from pico2d import *
from pico2d import get_canvas_height, get_canvas_width
from Background import Background
from Charater import Charater
from Furniture import Cookware, FoodBox, Furniture
from Game_data import Cookwares, Raw_food
from Order import Order
from Game_world import all_objects, load
from Wall import Wall
import framework
import Game_world
import time
from UI import UI
import pause_mode


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
    pass
   
    



def finish():
    Game_world.clear()

def update():
    Game_world.update()
    Game_world.handle_collision()

def draw():
    clear_canvas()
    Game_world.render()
    update_canvas()
Pause=False
def pause():
    #UI시간 멈추기
    global pausetime, Pause
    Pause = True
    pausetime = time.time()

def resume():
    global wares
    #멈춘 시간만큼 UI시간 수정
    pause = time.time() - pausetime
   
    if isinstance(Ui,UI) :Ui.timer = Ui.timer + pause
    for i in wares:
        i.timer += pausetime
    pause = False


def create_new_level_1():
    global Ui, charater, counter, wares, foodboxs, walls
    Game_world.clear()
    Ui, charater, counter, wares, foodboxs, walls = None,None,None,None,None,None
    background = Background()
    Game_world.add_object(background,0)

    walls = [Wall(0,0,get_canvas_width(),100)]
    walls.append(Wall(get_canvas_width()*4/5,100, (get_canvas_width()*7)/8,get_canvas_height()/3))
    walls.append(Wall(get_canvas_width()*13/15,get_canvas_height()/3, get_canvas_width()*7/8,get_canvas_height()*2/3))
    walls.append(Wall(get_canvas_width()*4/5,get_canvas_height()*2/3, get_canvas_width()*7/8,get_canvas_height()))
    walls.append(Wall(get_canvas_width()/3,get_canvas_height()/3, get_canvas_width()*2/5,get_canvas_height()*2/3))
    Game_world.add_objects(walls,1)
    for wall in walls:
        Game_world.add_collision_pair('charater:wall',None,wall)

    Ui = UI()
    Game_world.add_object(Ui,2)

    #매대
    counter = Furniture('counter', get_canvas_width()*4/5, get_canvas_height()/3, get_canvas_width()*15/16, get_canvas_height()*2/3)#음식 투입구
    Game_world.add_object(counter,3)
    Game_world.add_collision_pair('charater:counter',None,counter)

    # 조리대
    wares = [Cookware(Cookwares[i],30, i * 60 + 300, 60,60) for i in range(len(Cookwares))]
    Game_world.add_objects(wares,3)
    for cookware in wares:
        Game_world.add_collision_pair('charater:cookware',None,cookware)

    #음식
    foodboxs=[FoodBox(Raw_food[i], 30+i * 60 , get_canvas_height()-180, 60,60) for i in range(len(Raw_food))]
    Game_world.add_objects(foodboxs,3)

    #       캐릭터,조리도구,음식
    # 플레이어 캐릭터  
    charater = Charater()
    Game_world.add_object(charater,5)
    Game_world.add_collision_pair('charater:cookware',charater,None)
    Game_world.add_collision_pair('charater:counter',charater,None)
    Game_world.add_collision_pair('charater:food',charater,None)
    Game_world.add_collision_pair('charater:wall',charater,None)
    
def create_new_level_2():
    global Ui, charater, counter, wares, foodboxs, walls
    Game_world.clear()
    Ui, charater, counter, wares, foodboxs, walls = None,None,None,None,None,None
    background = Background()
    Game_world.add_object(background,0)

    walls = [Wall(0,0,get_canvas_width(),100)]
    walls.append(Wall(get_canvas_width()*4/5,100, (get_canvas_width()*7)/8,get_canvas_height()/3))
    walls.append(Wall(get_canvas_width()*13/15,get_canvas_height()/3, get_canvas_width()*7/8,get_canvas_height()*2/3))
    walls.append(Wall(get_canvas_width()*4/5,get_canvas_height()*2/3, get_canvas_width()*7/8,get_canvas_height()))

    #장애물
    walls.append(Wall(get_canvas_width()/3,get_canvas_height()/3, get_canvas_width()*2/5,get_canvas_height()*2/3))
    Game_world.add_objects(walls,1)
    for wall in walls:
        Game_world.add_collision_pair('charater:wall',None,wall)

    Ui = UI()
    Game_world.add_object(Ui,2)

    #매대
    counter = Furniture('counter', get_canvas_width()*4/5, get_canvas_height()/3, get_canvas_width()*15/16, get_canvas_height()*2/3)#음식 투입구
    Game_world.add_object(counter,3)
    Game_world.add_collision_pair('charater:counter',None,counter)

    # 조리대
    wares = [Cookware(Cookwares[i],30, i * 60 + 300, 60,60) for i in range(len(Cookwares))]
    Game_world.add_objects(wares,3)
    for cookware in wares:
        Game_world.add_collision_pair('charater:cookware',None,cookware)

    #음식
    foodboxs=[FoodBox(Raw_food[i], 30+i * 60 , get_canvas_height()-180, 60,60) for i in range(len(Raw_food))]
    Game_world.add_objects(foodboxs,3)

    #       캐릭터,조리도구,음식
    # 플레이어 캐릭터  
    charater = Charater()
    Game_world.add_object(charater,5)
    Game_world.add_collision_pair('charater:cookware',charater,None)
    Game_world.add_collision_pair('charater:counter',charater,None)
    Game_world.add_collision_pair('charater:food',charater,None)
    Game_world.add_collision_pair('charater:wall',charater,None)

def create_new_level_3():
    global Ui, charater, counter, wares, foodboxs, walls
    Game_world.clear()
    Ui, charater, counter, wares, foodboxs, walls = None,None,None,None,None,None
    background = Background()
    Game_world.add_object(background,0)

    walls = [Wall(0,0,get_canvas_width(),100)]
    walls.append(Wall(get_canvas_width()*4/5,100, (get_canvas_width()*7)/8,get_canvas_height()/3))
    walls.append(Wall(get_canvas_width()*13/15,get_canvas_height()/3, get_canvas_width()*7/8,get_canvas_height()*2/3))
    walls.append(Wall(get_canvas_width()*4/5,get_canvas_height()*2/3, get_canvas_width()*7/8,get_canvas_height()))
    walls.append(Wall(get_canvas_width()/3,get_canvas_height()/3, get_canvas_width()*2/5,get_canvas_height()*2/3))
    Game_world.add_objects(walls,1)
    for wall in walls:
        Game_world.add_collision_pair('charater:wall',None,wall)

    Ui = UI()
    Game_world.add_object(Ui,2)

    #매대
    counter = Furniture('counter', get_canvas_width()*4/5, get_canvas_height()/3, get_canvas_width()*15/16, get_canvas_height()*2/3)#음식 투입구
    Game_world.add_object(counter,3)
    Game_world.add_collision_pair('charater:counter',None,counter)

    # 조리대
    wares = [Cookware(Cookwares[i],30, i * 60 + 300, 60,60) for i in range(len(Cookwares))]
    Game_world.add_objects(wares,3)
    for cookware in wares:
        Game_world.add_collision_pair('charater:cookware',None,cookware)

    #음식
    foodboxs=[FoodBox(Raw_food[i], 30+i * 60 , get_canvas_height()-180, 60,60) for i in range(len(Raw_food))]
    Game_world.add_objects(foodboxs,3)

    #       캐릭터,조리도구,음식
    # 플레이어 캐릭터  
    charater = Charater()
    Game_world.add_object(charater,5)
    Game_world.add_collision_pair('charater:cookware',charater,None)
    Game_world.add_collision_pair('charater:counter',charater,None)
    Game_world.add_collision_pair('charater:food',charater,None)
    Game_world.add_collision_pair('charater:wall',charater,None)

def load_saved_world():
    global Ui, charater, counter, wares, foodboxs, walls
    Game_world.clear()
    Ui, charater, counter, wares, foodboxs, walls = None,None,None,[],[],[]
    Order.list.clear()
    load()
    for o in all_objects():
        if isinstance(o, Charater):
            charater = o
        elif isinstance(o,Furniture):
            counter = o
        elif isinstance(o,Cookware):
            wares.append(o)
        elif isinstance(o,FoodBox):
            foodboxs.append(o)
        elif isinstance(o,UI):
            Ui = o
        elif isinstance(o,Wall):
            walls.append(o)
    print(f"게임 월드 : {Game_world.world[2]}")
    print(f"명령 리스트 : {Order.list}")
    
