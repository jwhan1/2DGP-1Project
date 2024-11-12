from pico2d import open_canvas, delay, close_canvas
from framework import run

import play_mode as start_mode


open_canvas(800,600)
run(start_mode)
close_canvas()
