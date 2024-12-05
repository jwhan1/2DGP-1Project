from pico2d import *
import framework
import Game_world
import play_mode
from button import button
import Charater
import Background





def load_saved_world():
    play_mode.Charater, play_mode.background = None, None
    Game_world.load()
    for o in Game_world.all_objects():
        if isinstance(o, Charater):
            play_mode.Charater = o
        elif isinstance(o, Background):
            play_mode.background = o
    if play_mode.Charater and play_mode.background:
        pass





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