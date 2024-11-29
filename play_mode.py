from pico2d import *
import framework
import Game_world

from Background import Background
from UI import UI
from Furniture import Furniture, Cookware, FoodBox
from Wall import Wall
from Charater import Charater
import pause_mode


Ingredient = ['fish', 'fruit', 'sashimi', 'spare', 'steak', 'sushi',
              'apple_green','apple_red','apple_yellow','avocado_whole',
            'banana','beet','blueberries',
            'cantaloupe_whole','carrot','cheese','cherries',
            'strawberry',
            'tomato',
            'watermelon_whole']#음식의 종류
Cookwares = ['chopping_board','cooking_pot','frying_pan' ]

def handle_events():
    global charater
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_0:
            print(pause)
            framework.push_mode(pause_mode)
        else:
            charater.handle_event(event)

def init():
    global Ui, charater, foods, counter, cookwares, wall#충돌하는 물체만

    background = Background()
    Game_world.add_object(background,0)
    Ui = UI()
    Game_world.add_object(Ui,2)

    counter = Furniture('counter', 650, 200,100,200)#음식 투입구
    Game_world.add_object(counter,0)
    Game_world.add_collision_pair('charater:counter',None,counter)

    wall=Wall(0,800,100,0)
    Game_world.add_object(counter,0)
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
    foodboxs=[FoodBox(Ingredient[i], i * 60 , 200, 60,60) for i in range(len(Ingredient))]
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
    pausetime = framework.frame_time
    pass

def resume():
    #멈춘 시간만큼 UI시간 수정
    Ui.timer = Ui.timer + framework.frame_time - pausetime
    pass
