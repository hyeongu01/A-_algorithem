import pygame
import math
import random
import argparse
# import checkbox

# parser 선언부
parser = argparse.ArgumentParser()

parser.add_argument('-size', '--screen_size', nargs=2, type=int, default=[600, 600], metavar=("X", "Y"))
parser.add_argument('-obs_ratio', '--inc_obstacle_ratio', type=float, default=0.2, metavar="obs_ratio")

args = parser.parse_args()

# 화면 크기 및 큐브 크기 설정
screen_x = args.screen_size[0]
screen_y = args.screen_size[1]

# 큐브 격자 크기 설정
cube_size = (30, 30)
cube_size_x = screen_x // cube_size[0]
cube_size_y = screen_y // cube_size[1]

# obstacle_ratio 설정
random_rate = args.inc_obstacle_ratio

# 색깔 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
EMERALD = (97, 223, 182)
YELLOW = (255, 255, 0)
SKYBLUE = (135, 206, 235)
WHITEGRAY = (207, 207, 207)

# 큐브 상태 정의
CUBE_STATES = {
    0: WHITE,
    1: GRAY,
    2: GREEN,
    3: RED,
    4: EMERALD,
    5: SKYBLUE
}

def draw_cube(screen, cubes, cube_index):
    pygame.draw.rect(screen, CUBE_STATES[cubes[cube_index[0]][cube_index[1]]], (cube_index[0] * cube_size_x, cube_index[1] * cube_size_y, cube_size_x, cube_size_y))

def draw_cubes(screen, cubes):
    for x in range(len(cubes)):
        for y in range(len(cubes[0])):
            draw_cube(screen, cubes, (x, y))
def draw_grid(screen):
    for x in range(0, screen_x, cube_size_x):
        pygame.draw.line(screen, BLACK, (x, 0), (x, screen_y))
    for y in range(0, screen_y, cube_size_y):
        pygame.draw.line(screen, BLACK, (0, y), (screen_y, y))
        
        
def get_manhattan_distance(start, goal):   # start에서 goal의 맨허튼 거리 (가로거리 + 세로거리)
    delta_x = abs(start[0] - goal[0])
    delta_y = abs(start[1] - goal[1])
    return delta_x + delta_y

def get_euclidean_distance(start, goal):    # # start에서 goal의 유클리드 거리 (피타고라스)
    delta_x = start[0] - goal[0]
    delta_y = start[1] - goal[1]
    return math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2))

def draw_button(screen, point, size, title):
    button_font = pygame.font.SysFont(None, 25)
    my_text = button_font.render(title, True, BLACK)
    pygame.draw.rect(screen, GRAY, (point[0], point[1], size[0], size[1]), 0, 5)
    screen.blit(my_text, (point[0]+5, point[1] + 5))

def draw_button_all(screen):
    padding = 10
    button_size_x = 110
    button_size_y = 25
    position = (screen_x - button_size_x - padding, screen_y - button_size_y * 3 - 10 - padding) 
    draw_button(screen, (position[0], position[1]), (button_size_x, button_size_y), "A* Start")
    draw_button(screen, (position[0], position[1] + 30), (button_size_x, button_size_y), "Clear obs")
    draw_button(screen, (position[0], position[1] + 60), (button_size_x, button_size_y), "Random obs")
    start_button = [position, (button_size_x, button_size_y)]
    clear_button = [(position[0], position[1] + 30), (button_size_x, button_size_y)]
    random_button = [(position[0], position[1] + 60), (button_size_x, button_size_y)]
    return start_button, clear_button, random_button

def is_on_button(pointer, button):
    button_position = button[0]
    button_size = button[1]
    if (pointer[0] >= button_position[0]) and (pointer[1] >= button_position[1]):
        if (pointer[0] <= button_position[0] + button_size[0]) and (pointer[1] <= button_position[1] + button_size[1]):
            return True
    else:
        return False
    
def clear_obs(cubes):
    for x in range(cube_size[0]):
        for y in range(cube_size[1]):
            if cubes[x][y] in (1, 4, 5):
                cubes[x][y] = 0
                
                
def random_obs(cubes, random_rate):
    total_node_num = cube_size[0] * cube_size[1]
    obs_num = total_node_num * random_rate
    
    clear_obs(cubes)
    i = 0
    while i < obs_num:
        x = random.randint(0, cube_size[0] - 1)
        y = random.randint(0, cube_size[1] - 1)
        if cubes[x][y] in (1, 2, 3):
            continue
        else:
            cubes[x][y] = 1
            i += 1
    i = 0
    for j in cubes:
        for k in j:
            if k == 1:
                i+= 1
    
    
MANHATTAN = 0
EUCLIDEAN = 1

def possible_path(nodes, node):
    result = []
    if (node[1] + 1 < cube_size[1]) and (nodes[node[0]][node[1] + 1] != 1): # up
        result.append((node[0], node[1] + 1))
    if (nodes[node[0]][node[1] - 1] != 1) and (node[1] - 1 >= 0): # down
        result.append((node[0], node[1] -1))
    if (node[0] + 1 < cube_size[0]) and (nodes[node[0] + 1][node[1]] != 1): # right
        result.append((node[0] + 1, node[1]))
    if (nodes[node[0] - 1][node[1]] != 1) and (node[0] - 1 >= 0): # left
        result.append((node[0] - 1, node[1]))
    return result

NODE_ID = 0
F_SCORE = 1
G_SCORE = 2
H_SCORE = 3
PARENT = 4

def get_start_info(nodes, start_node, goal_node, manhattan):
    open_list = []
    close_list = [[start_node, 0, 0, 0, None]]
    # print("compare: ", start_node)
    for i in possible_path(nodes, start_node):
        node_id = i
        g = 1
        if manhattan:
            h = get_manhattan_distance(i, goal_node)
        else:
            h = get_euclidean_distance(i, goal_node)
        f = g + h
        parent_node = start_node
        open_list.append([node_id, f, g, h, parent_node])
        # print("append ", [node_id, f, g, h, parent_node])
    return open_list, close_list

def update_open_info(nodes, parent_node_info, goal_node, manhattan):
    open_list = []
    for i in possible_path(nodes, parent_node_info[0]):
        node_id = i
        g = parent_node_info[2] + 1
        if manhattan:
            h = get_manhattan_distance(i, goal_node)
        else:
            h = get_euclidean_distance(i, goal_node)
        f = g + h
        parent_node = parent_node_info[0]
        open_list.append([node_id, f, g, h, parent_node])
    return open_list

def clear_nodes(nodes):
    for x in range(cube_size[0]):
        for y in range(cube_size[1]):
            if nodes[x][y] in (4, 5):
                nodes[x][y] = 0
        

def color_open_list(nodes, open_list):
    for node_info in open_list:
        node = node_info[0]
        if nodes[node[0]][node[1]] == 0:
            nodes[node[0]][node[1]] = 4

def connect_node(screen, nodes, node1, node2):
    node1_mid = [node1[0]*cube_size_x + cube_size_x//2, node1[1]*cube_size_y + cube_size_y//2]
    node2_mid = [node2[0]*cube_size_x + cube_size_x//2, node2[1]*cube_size_y + cube_size_y//2]
    pygame.draw.line(screen, YELLOW, node1_mid, node2_mid, width=2)
    if nodes[node1[0]][node1[1]] != 5:
        draw_cube(screen, nodes, node1)
    if nodes[node2[0]][node2[1]] != 5:
        draw_cube(screen, nodes, node2)

def get_result_path(close_list):
    goal_node_info = close_list.pop()
    reverse_path = [goal_node_info[NODE_ID]]
    
    target = goal_node_info[PARENT]
    while target != None:
        for node in close_list:
            if node[0] == target:
                reverse_path.append(node[0])
                target = node[PARENT]
    return reverse_path

    


def A_star(nodes, start_node, goal_node, screen, manhattan=True):
    clear_nodes(nodes)
    open_list = None
    close_list = None
    close_nodes = []

    while True:
        if open_list is None:
            open_list, close_list = get_start_info(nodes, start_node, goal_node, manhattan)
            close_nodes.append(start_node)
        else:
            open_list = sorted(open_list, key=lambda x: x[1], reverse=True)
            if len(open_list) == 0:
                close_list = sorted(close_list, key=lambda x: x[1], reverse=True)
                print(len(close_list))
                print("path not founded!")
                return get_result_path(close_list)
            compare_node_info = open_list.pop()
            close_list.append(compare_node_info)
            close_node = compare_node_info[0]
            close_nodes.append(close_node)
            if goal_node in close_nodes:
                break
            nodes[close_node[0]][close_node[1]] = 5
            
            open_list_nodes = update_open_info(nodes, compare_node_info, goal_node, manhattan)
            # print("compare: ", compare_node_info)
            for o in open_list_nodes:
                o_open_list_node = None
                col = None
                # print(o)
                for n, o_open_list in enumerate(open_list):
                    if o[NODE_ID] == o_open_list[NODE_ID]:
                        o_open_list_node = o
                        col = n
                if o_open_list_node != None:
                    if o[G_SCORE] < o_open_list_node[G_SCORE]:
                        open_list[col] = o
                elif o[NODE_ID] in close_nodes:
                    continue
                else:
                    open_list.append(o)
        
        color_open_list(nodes, open_list)
        draw_cubes(screen, nodes)
        draw_grid(screen)
        pygame.display.flip()
        # time.sleep(1)
        # print("----")
    h = None
    if manhattan:
        h = "Manhattan"
    else:
        h = "Euclidean"
        
    print("number of explored nodes: ", len(close_list) - 1, " in ", h)
    # color_open_list(nodes, open_list)
    result = get_result_path(close_list)
    return result
        
# Checkbox class
class Checkbox:
    def __init__(self, x, y, text, status=False):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.checked = status
        self.text = text

    def draw(self, screen):
        font = pygame.font.SysFont(None, 20)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        if self.checked:
            button_font = pygame.font.SysFont(None, 30)
            checked = button_font.render("*", True, BLACK)
            padding = 3
            screen.blit(checked, (self.rect.x + padding, self.rect.y + padding))
        text_surface = font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.rect.right + 5, self.rect.centery - text_surface.get_height() // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.checked:
                    return False
                else:
                    self.checked = True
                    return True
    
    def _toggle(self):
        self.checked = not self.checked
    
    def is_checked(self):
        return self.checked
                
def draw_checkbox_background(screen, position, size):
    background = pygame.Rect(position[0], position[1], size[0], size[1])
    pygame.draw.rect(screen, WHITEGRAY, background, 0, 5)

def draw_checkbox(screen, checkbox_list, position, title):
    size = (110, 70)
    font = pygame.font.SysFont(None, 30)
    title_text = font.render(title, True, BLACK)
    draw_checkbox_background(screen, position, size)
    screen.blit(title_text, (position[0] + 5, position[1] + 5))
    for checkbox in checkbox_list:
        checkbox.draw(screen)
    
def checkbox_event(checkbox_list, event):
    for n, checkbox in enumerate(checkbox_list):
        if checkbox.handle_event(event):
            checkbox_list[n-1].checked = not checkbox_list[n-1].checked
        
    

def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption("A* Algorithem")
    
    checkbox_position = (screen_x - 120, screen_y - 95 - 80)
    manhattan = Checkbox(checkbox_position[0] + 5, checkbox_position[1] + 30, "Manhattan", True)
    euclidean = Checkbox(checkbox_position[0] + 5, checkbox_position[1] + 30 + 15 + 5, "Euclidean")
    checkbox_list = [manhattan, euclidean]

    cubes = [[0 for _ in range(cube_size[1])] for _ in range(cube_size[0])]
    
    # 시작지점, 목표지점 설정
    start_cube = ((len(cubes) // 3), (len(cubes[0]) // 2))
    goal_cube = ((len(cubes) * 2 // 3), (len(cubes[0]) // 2))
    cubes[start_cube[0]][start_cube[1]] = 2
    cubes[goal_cube[0]][goal_cube[1]] = 3
    
    selected_cube = None
    selected_offset = None

    clock = pygame.time.Clock()
    running = True

    result = None
    while running:
        for event in pygame.event.get():
            checkbox_event(checkbox_list, event)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 누를 때
                x, y = pygame.mouse.get_pos()
                cube_x = x // cube_size_x
                cube_y = y // cube_size_y
                # print(x, y)
                
                if is_on_button((x, y), start_button):
                    result = A_star(cubes, start_cube, goal_cube, screen, manhattan.is_checked())
                    # print(result)
                elif is_on_button((x, y), clear_button):
                    clear_obs(cubes)
                elif is_on_button((x, y), random_button):
                    random_obs(cubes, random_rate)
                    
                elif cubes[cube_x][cube_y] not in (2, 3):
                    selected_cube = cubes[cube_x][cube_y]
                    selected_offset = (cube_x, cube_y)
                    if cubes[cube_x][cube_y] in (4, 5):
                        cubes[cube_x][cube_y] = 1
                    else:
                        cubes[cube_x][cube_y] = (cubes[cube_x][cube_y] + 1) % 2
                        
                        
                elif cubes[cube_x][cube_y] in (2, 3):
                    selected_cube = cubes[cube_x][cube_y]
                    selected_offset = (cube_x, cube_y)
                    cubes[cube_x][cube_y] = 0
                    
            elif event.type == pygame.MOUSEBUTTONUP:    # 마우스 클릭 뗄 때
                if selected_cube in (2, 3):
                    x, y = pygame.mouse.get_pos()
                    cube_x = x // cube_size_x
                    cube_y = y // cube_size_y
                    if cubes[cube_x][cube_y] in (0, 4, 5):
                        cubes[cube_x][cube_y] = selected_cube
                        if selected_cube == 2:
                            start_cube = (cube_x, cube_y)
                        else:
                            goal_cube = (cube_x, cube_y)
                    else:
                        cubes[selected_offset[0]][selected_offset[1]] = selected_cube
                        if selected_cube == 2:
                            start_cube = (cube_x, cube_y)
                        else:
                            goal_cube = (cube_x, cube_y)
                    # print("")
                    # print(f"start: ({start_cube[0]}, {start_cube[1]})")
                    # print(f"goal: ({goal_cube[0]}, {goal_cube[1]})")
                    # print(f"mangattan distance: {get_manhattan_distance(start_cube, goal_cube)}")
                    # print(f"Euclidean distance: {get_euclidean_distance(start_cube, goal_cube)}")
                selected_cube = None
                selected_offset = None
                
            elif event.type == pygame.MOUSEMOTION:  # 마우스 드래그할 때
                if selected_cube in (0, 1, 4, 5):
                    x, y = pygame.mouse.get_pos()
                    cube_x = x // cube_size_x
                    cube_y = y // cube_size_y
                    if selected_offset != (cube_x, cube_y):
                        if cubes[cube_x][cube_y] in (0, 1, 4, 5):
                            if cubes[cube_x][cube_y] in (0, 1):
                                selected_cube = cubes[cube_x][cube_y]
                                selected_offset = (cube_x, cube_y)
                                cubes[cube_x][cube_y] = (cubes[cube_x][cube_y] + 1) % 2
                            else:
                                selected_cube = cubes[cube_x][cube_y]
                                selected_offset = (cube_x, cube_y)
                                cubes[cube_x][cube_y] = 1
                        # else:
                        #     selected_cube = cubes[cube_x][cube_y]
                        #     selected_offset = (cube_x, cube_y)
                        #     cubes[cube_x][cube_y] = 1
                            
                elif selected_cube in (2, 3):
                    x, y = pygame.mouse.get_pos()
                    cube_x = x // cube_size_x
                    cube_y = y // cube_size_y
                    if cubes[cube_x][cube_y] in (0, 4, 5):
                        cubes[selected_offset[0]][selected_offset[1]] = 0
                        selected_offset = (cube_x, cube_y)
                        cubes[selected_offset[0]][selected_offset[1]] = selected_cube
            
        
        screen.fill(WHITE)
        draw_cubes(screen, cubes)
        if result != None:
            prev = None
            for node in result:
                if prev == None:
                    prev = node
                    continue
                else:
                    connect_node(screen, cubes, node, prev)
                    prev = node
        draw_grid(screen)
        start_button, clear_button, random_button = draw_button_all(screen)
        draw_checkbox(screen, checkbox_list, checkbox_position, "Heuristic")
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()