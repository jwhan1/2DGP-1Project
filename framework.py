import time

def change_mode(mode):
    global stack# 모드 관리
    if (len(stack) > 0):
        stack[-1].finish()# 현재 모드를 종료
        stack.pop()# 현재 모드를 제거
    stack.append(mode)
    mode.init()


def push_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()#현재 모드를 일시정지
    stack.append(mode)
    mode.init()


def pop_mode():
    global stack
    if (len(stack) > 0):
        stack[-1].finish()#현재 모드를 제거
        stack.pop()
    if (len(stack) > 0):
        stack[-1].resume()#이전 모드를 실행


def quit():
    global running
    running = False


def run(start_mode):
    global running, stack
    running = True
    stack = [start_mode]
    start_mode.init()
    global frame_time
    frame_time=0.0
    current_time=time.time()
    while running:#현재 모드를 실행
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        frame_time = time.time() - current_time
        frame_rate = 1.0 / frame_time
        current_time += frame_time

    while (len(stack) > 0):
        stack[-1].finish()
        stack.pop()