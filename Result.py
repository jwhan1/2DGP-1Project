from Game_data import Game_point, what_input, best_point
from pico2d import load_image, load_font, get_canvas_height, get_canvas_width
from time import time
import framework
import title_mode
class Result:
    font = None
    def __init__(self):
        self.time = time()
        self.best = best_point
        self.point = Game_point[-1]
        self.list = []
        print(what_input)
        self.list = [load_image(f'image/food/{what_input[i]}.png') for i in range(len(what_input))]
        self.back = load_image('image/result_background.png')
        if Result.font == None:
            Result.font = load_font('CookieRun Regular.ttf', 20)
    def update(self):
        if time() > self.time + 10:
            framework.change_mode(title_mode)
        pass
    def draw(self):
        self.back.clip_draw(0, 0, self.back.w, self.back.h, get_canvas_width()/2, get_canvas_height()/2, get_canvas_width(), get_canvas_height())
        Result.font.draw(20, get_canvas_height()-200, f'total point:{self.point}', (0, 0, 255))
        #get_canvas_width()/2+50~get_canvas_width()+200
        for i in range(len(self.list)):
            self.list[i].clip_draw(0, 0, self.list[i].w, self.list[i].h, 100+(25*(i%10)), get_canvas_height()/2-(50*(i//10)), 50, 50)
        Result.font.draw(get_canvas_width()-200, 100,f"{int(10 + self.time-time())}초 뒤에 타이틀로")
