from pico2d import *
from Result import Result
import framework
import Game_world

def handle_events():
    global charater
    events = get_events()
    for event in events:
        pass
           

def init():
    global image
    image = load_image('image/title.png')
    #결과창
    result=Result()

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