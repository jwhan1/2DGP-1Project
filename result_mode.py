from pico2d import *
import framework
import Game_world
from Result import Result
from button import button
def handle_events():
    global charater
    events = get_events()
    for event in events:
        #aif event.type == SDL_QUIT:
            framework.quit()
           

def init():
    global image, result,buttons
    image = load_image('image/title.png')
    #결과창
    result = Result()
    buttons = [button('quit',get_canvas_width()-100, 60)]
    buttons.append(button('title',get_canvas_width()-300, 60))

    Game_world.add_object(result,0)


def finish():
    Game_world.clear()

def update():
    Game_world.update()
def draw():
    clear_canvas()
    Game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass