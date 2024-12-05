from pico2d import *
import framework
import Game_world

def handle_events():
    global charater
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN :
            framework.pop_mode()
           

def init():
    global image
    image = load_image('image/title.png')


def finish():
    pass

def update():
    pass
def draw():
    clear_canvas()
    image.clip_draw(0, 0, image.w, image.h, get_canvas_width()/2, get_canvas_width()/2, get_canvas_width(), get_canvas_width())
    update_canvas()

def pause():
    pass

def resume():
    pass