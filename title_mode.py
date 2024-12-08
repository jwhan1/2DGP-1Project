from pico2d import *
import framework
import Game_world
from button import button
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
    global image, buttons
    image = load_image('image/title.png')
    buttons = [button('start',get_canvas_width() / 2, get_canvas_height() / 3)]
    buttons.append(button('quit',get_canvas_width() / 2, get_canvas_height() / 3-100))
    Game_world.add_objects(buttons,1)

def finish():
    Game_world.clear()

def update():
    Game_world.update()
    
def draw():
    clear_canvas()
    image.clip_draw(0, 0, image.w, image.h, get_canvas_width() / 2, get_canvas_height() / 2, get_canvas_width(), get_canvas_height())
    Game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

