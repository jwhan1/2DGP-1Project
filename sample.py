from pico2d import *

Ingredient = list({'fish', 'fruit', 'sashimi', 'spare', 'steak', 'sushi'})

class Background:
    def __init__(self, what):
        if what == 'background':
            self.x = 400
            self.y = 300
            self.image = load_image(f'image/{what}.png')
            self.w = self.image.w
            self.h = self.image.h
            self.imgW = self.image.w
            self.imgH = self.image.h
        elif what == 'floor':
            self.x = 400
            self.y = 50
            self.w = 800
            self.h = 100
            self.image = load_image(f'image/{what}.png')
            self.imgW = self.image.w
            self.imgH = self.image.h

    def update(self):
        pass
    def draw(self):
        self.image.clip_draw(0, 0, self.imgW, self.imgH, self.x, self.y, self.w, self.h)
    def handle_event(self, event):
        pass


class Furniture:
    def __init__(self, what, x, y):
        self.x = x
        self.y = 100 + y/2
        self.w = 100
        self.h = y
        self.image = load_image(f'image/furniture/{what}.png')
        self.imgW = self.image.w
        self.imgH = self.image.h
    def update(self):
        pass
    def draw(self):
        self.image.clip_draw(0, 0, self.imgW, self.imgH, self.x, self.y, self.w, self.h)
    def handle_event(self, event):
        pass

class Foods:
    def __init__(self, what, x, y):
        self.x = x
        self.y = 100 + y
        self.w = 50
        self.h = 50

        self.image = load_image(f'image/food/{what}.png')
        self.imgW = self.image.w
        self.imgH = self.image.h
    def update(self):
        pass
    def draw(self):
        self.image.clip_draw(0, 0, self.imgW, self.imgH, self.x, self.y, self.w, self.h)
    def handle_event(self, event):
        pass

class Charater:
    def __init__(self, what):
        self.x = 50
        self.y = 550
        self.w = 100
        self.h = 100
        self.image = load_image(f'image/food/{what}.png')
        self.imgW = self.image.w
        self.imgH = self.image.h
    def update(self):
        pass
    def draw(self):
        self.image.clip_draw(0, 0, self.imgW, self.imgH, self.x, self.y, self.w, self.h)
    def handle_event(self, event):
        pass




def update_world():
    for o in world:
        o.update()

def rander_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

def reset_world():
    global running, world, food, background, floor, countertop, counter
    running = True
    world=[]

    background = Background('background')
    world.append(background)

    floor = Background('floor')
    world.append(floor)

    food = [Foods(Ingredient[i],i * 100 + 50, 50) for i in range(len(Ingredient))]#음식들
    world += food
    
    countertop = Furniture('table', 750, 100)#테이블
    world.append(countertop)

    counter = Furniture('counter', 650, 200)#음식 투입구
    world.append(counter)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

open_canvas()

reset_world()
while running:
    handle_events()
    update_world()
    rander_world()
    delay(0.01)

close_canvas()
