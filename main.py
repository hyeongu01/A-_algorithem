import pygame
import math

# 화면 크기 및 큐브 크기 설정
screen_x = 600
screen_y = 600

# 큐브 격자 크기 설정
cube_size = [20, 20]
cube_size_x = screen_x // cube_size[0]
cube_size_y = screen_y // cube_size[1]

# 색깔 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
EMERALD = (97, 223, 182)

# 큐브 상태 정의
CUBE_STATES = {
    0: WHITE,
    1: GRAY,
    2: GREEN,
    3: RED,
    4: EMERALD
}


def draw_cubes(screen, cubes):
    for x in range(len(cubes)):
        for y in range(len(cubes[0])):
            pygame.draw.rect(screen, CUBE_STATES[cubes[x][y]], (x * cube_size_x, y * cube_size_y, cube_size_x, cube_size_y))

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


MANHATTAN = 0
EUCLIDEAN = 1

def possible_path(nodes, node):
    result = []
    if nodes[node[0]][node[1] + 1] != 1: # up
        result.append((node[0], node[1] + 1))
    if nodes[node[0]][node[1] - 1] != 1: # down
        result.append((node[0], node[1] -1))
    if nodes[node[0] + 1][node[1]] != 1: # right
        result.append((node[0] + 1, node[1]))
    if nodes[node[0] - 1][node[1]] != 1: # left
        result.append((node[0] - 1, node[1]))
    return result

# NODE_ID = 0
# F_SCORE = 1
# G_SCORE = 2
# H_SCORE = 3
# PARENT = 4

def get_start_info(nodes, start_node, goal_node, manhattan):
    open_list = []
    close_list = [[start_node, 0, 0, 0, None]]
    for i in possible_path(nodes, start_node):
        node_id = i
        g = 1
        if manhattan:
            h = get_euclidean_distance(i, goal_node)
        else:
            h = get_manhattan_distance(i, goal_node)
        f = g + h
        parent_node = start_node
        open_list.append([node_id, f, g, h, parent_node])
    return open_list, close_list

def update_open_info(nodes, parent_node_info, goal_node, manhattan):
    open_list = []
    for i in possible_path(nodes, parent_node_info[0]):
        node_id = i
        g = parent_node_info[2] + 1
        if manhattan:
            h = get_euclidean_distance(i, goal_node)
        else:
            h = get_manhattan_distance(i, goal_node)
        f = g + h
        parent_node = parent_node_info[0]
        open_list.append([node_id, f, g, h, parent_node])
    return open_list

def A_star(nodes, start_node, goal_node, manhattan=MANHATTAN):
    open_list, close_list = get_start_info(nodes, start_node, goal_node, manhattan)
    for f in open_list:
        print(f[1])
    

    print(open_list)
    print(close_list)


def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption("A* Algorithem")

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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 누를 때
                x, y = pygame.mouse.get_pos()
                cube_x = x // cube_size_x
                cube_y = y // cube_size_y
                print(cube_x, cube_y)
                if cubes[cube_x][cube_y] in (0, 1):
                    selected_cube = cubes[cube_x][cube_y]
                    selected_offset = (cube_x, cube_y)
                    cubes[cube_x][cube_y] = (cubes[cube_x][cube_y] + 1) % 2
                    
                    if (cube_x, cube_y) == (cube_size[0] - 1, cube_size[1] - 1):          # 임시 A* 시작버튼
                        A_star(cubes, start_cube, goal_cube)
                    
                elif cubes[cube_x][cube_y] in (2, 3):
                    selected_cube = cubes[cube_x][cube_y]
                    selected_offset = (cube_x, cube_y)
                    cubes[cube_x][cube_y] = 0
                    
            elif event.type == pygame.MOUSEBUTTONUP:    # 마우스 클릭 뗄 때
                if selected_cube in (0, 1):
                    selected_cube = None
                    selected_offset = None
                    
                elif selected_cube in (2, 3):
                    x, y = pygame.mouse.get_pos()
                    cube_x = x // cube_size_x
                    cube_y = y // cube_size_y
                    if cubes[cube_x][cube_y] == 0:
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
                    print("")
                    print(f"start: ({start_cube[0]}, {start_cube[1]})")
                    print(f"goal: ({goal_cube[0]}, {goal_cube[1]})")
                    print(f"mangattan distance: {get_manhattan_distance(start_cube, goal_cube)}")
                    print(f"Euclidean distance: {get_euclidean_distance(start_cube, goal_cube)}")
                    selected_cube = None
                    selected_offset = None
                
            elif event.type == pygame.MOUSEMOTION:  # 마우스 드래그할 때
                if selected_cube in (0, 1):
                    x, y = pygame.mouse.get_pos()
                    cube_x = x // cube_size_x
                    cube_y = y // cube_size_y
                    if selected_offset != (cube_x, cube_y):
                        if cubes[cube_x][cube_y] in (0, 1):
                            selected_cube = cubes[cube_x][cube_y]
                            selected_offset = (cube_x, cube_y)
                            cubes[cube_x][cube_y] = (cubes[cube_x][cube_y] + 1) % 2
                            
                elif selected_cube in (2, 3):
                    x, y = pygame.mouse.get_pos()
                    cube_x = x // cube_size_x
                    cube_y = y // cube_size_y
                    if cubes[cube_x][cube_y] == 0:
                        cubes[selected_offset[0]][selected_offset[1]] = 0
                        selected_offset = (cube_x, cube_y)
                        cubes[selected_offset[0]][selected_offset[1]] = selected_cube
        
        
        screen.fill(WHITE)
        draw_cubes(screen, cubes)
        draw_grid(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()