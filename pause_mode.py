from pico2d import *
import framework
import Game_world
import title_mode
def handle_events():
    global charater
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_r:#돌아가기
            framework.pop_mode()
        if event.type == SDL_KEYDOWN and event.key == SDLK_q:#타이틀로
            Game_world.clear()
            framework.change_mode(title_mode)
        if event.type == SDL_KEYDOWN and event.key == SDLK_s:#세이브
            Game_world.save()
            framework.pop_mode()
        if event.type == SDL_KEYDOWN and event.key == SDLK_l:#로드
            Game_world.load()
            framework.pop_mode()
           

def init():
    global image
    image = load_image('image\pause.png')


def finish():
    pass

def update():
    pass
def draw():
    clear_canvas()
    Game_world.update()
    image.clip_draw(0, 0, image.w, image.h, get_canvas_width()/2, get_canvas_width()/2, get_canvas_width(), get_canvas_width())
    update_canvas()

def pause():
    pass

def resume():
    pass