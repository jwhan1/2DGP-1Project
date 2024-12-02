from pico2d import *
import framework
import Game_world
import play_mode

def handle_events():
    global charater
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT or event.key == SDLK_ESCAPE:
            framework.quit()
        elif event.type == SDL_KEYDOWN :
            framework.change_mode(play_mode)
           

def init():
    global image,imageui,button
    image = load_image('image/title.png')
    imageui = load_image('image\selectlevelUI.png')
    

def finish():
    pass

def update():
    pass
def draw():
    clear_canvas()
    image.clip_draw(0, 0, image.w, image.h, get_canvas_width()/2, get_canvas_height()/2,get_canvas_width(), get_canvas_height())
    imageui.clip_draw(0, 0, image.w, image.h, get_canvas_width()/2, get_canvas_height()/2, 400, 300)
    update_canvas()

def pause():
    pass

def resume():
    pass