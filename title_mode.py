from pico2d import *
import framework
import Game_world
import levelchoose_mode

def handle_events():
    global charater
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT or event.key == SDLK_ESCAPE:
            framework.quit()
        elif event.type == SDL_KEYDOWN :
            framework.change_mode(levelchoose_mode)
           

def init():
    global image
    image = load_image('image/title.png')


def finish():
    pass

def update():
    pass
def draw():
    clear_canvas()
    image.clip_draw(0, 0, image.w, image.h, 400, 300, 800, 600)
    update_canvas()

def pause():
    pass

def resume():
    pass

class button:
    def __init__(self,x,y):
        self.x=x
        self.y=y