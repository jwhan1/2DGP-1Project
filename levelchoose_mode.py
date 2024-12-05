from pico2d import *
import framework
import Game_world
import play_mode
from button import button
from Background import Background
from UI import UI
from Furniture import Furniture, Cookware, FoodBox
from Wall import Wall
from Charater import Charater





def load_saved_world():
    play_mode.charater, play_mode.background = None, None
    play_mode.counter,play_mode.cookwares,play_mode.foodboxs,play_mode.button,play_mode.Ui,play_mode.walls=[],[],[],[],[]
    
    Game_world.load()
    for o in Game_world.all_objects():
        if isinstance(o, Background):
            play_mode.background = o
        elif isinstance(o, Charater):
            play_mode.charater = o
        elif isinstance(0,Furniture):
            play_mode.counter = o
        elif isinstance(0,Cookware):
            play_mode.cookwares = o
        elif isinstance(0,FoodBox):
            play_mode.foodboxs.append(o)
        elif isinstance(0,button):
            play_mode.button.append(o)
        elif isinstance(0,UI):
            play_mode.Ui = o
        elif isinstance(0,Wall):
            play_mode.walls.append(o)
        





def handle_events():
    global charater
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT or event.key == SDLK_ESCAPE:
            framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN :
            for button in buttons:
                button.handle_event(event)
           

def init():
    global image, imageui, buttons
    image = load_image('image/title.png')
    buttons = [button('level_1',get_canvas_width() / 2,get_canvas_height() / 3+100)]
    buttons.append(button('level_2',get_canvas_width() / 2,get_canvas_height() / 3))
    buttons.append(button('level_3',get_canvas_width() / 2,get_canvas_height() / 3-100))
    Game_world.add_objects(buttons,1)

def finish():
    Game_world.clear()

def update():
    Game_world.update()

def draw():
    clear_canvas()
    image.clip_draw(0, 0, image.w, image.h, get_canvas_width()/2, get_canvas_height()/2,get_canvas_width(), get_canvas_height())

    Game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass