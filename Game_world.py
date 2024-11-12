world = [[] for _ in range(4)]
collision_pairs = {} # 충돌 검사를 수행할 빈 딕셔너리

# 생성

def add_collision_pair(group,a,b):
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]
    if a: collision_pairs[group][0].append(a)
    if b: collision_pairs[group][1].append(b)

def add_object( e, depth):#추가할 객체,레이어        
    world[depth].append(e)

def add_objects(ol, depth = 0):#객체들 추가
    world[depth] += ol
#진행

def update():
    for layer in world:
        for o in layer:
            o.update()

def  render():
    for layer in world:
        for o in layer:
            o.draw()
#제거

def remove_object(o):# o 제거
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o#메모리에서 객체를 삭제
            return
    print(f'CRITICAL : 존재하지 않는 객체{o}를 지우려고 합니다.')


def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def clear():
    for layer in world:
        layer.clear()

#충돌 판정
def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def handle_collision(): #실제 검사를 진행 (어떤 객체의 충돌도 사용 가능)
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:#a리스트에서 하나
            for b in pairs[1]:#b리스트에서 하나
                if collide(a,b):#충돌 검사
                    print(f"{group} collide")
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)


