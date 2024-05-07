import pygame

# 화면 크기 및 큐브 크기 설정
screen_x = 600
screen_y = 600

# 큐브 격자 크기 설정
cube_size = [30, 30]
cube_size_x = screen_x // cube_size[0]
cube_size_y = screen_y // cube_size[1]

# 색깔 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 큐브 상태 정의
CUBE_STATES = {
    0: WHITE,
    1: GRAY,
    2: GREEN,
    3: RED
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

def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption("Grid Pattern")

    cubes = [[0 for _ in range(cube_size[1])] for _ in range(cube_size[0])]
    cubes[(len(cubes)) // 3][(len(cubes[0])) // 2] = 2
    cubes[(len(cubes)) * 2 // 3][(len(cubes[0])) // 2] = 3
    
    selected_cube = None
    selected_offset = None

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                cube_x = x // cube_size_x
                cube_y = y // cube_size_y
                if cubes[cube_x][cube_y] in (0, 1):
                    cubes[cube_x][cube_y] = (cubes[cube_x][cube_y] + 1) % 2
                elif cubes[cube_x][cube_y] in (2, 3):
                    selected_cube = cubes[cube_x][cube_y]
                    selected_offset = (cube_x, cube_y)
                    cubes[cube_x][cube_y] = 0
            elif event.type == pygame.MOUSEBUTTONUP:
                if selected_cube is not None:
                    x, y = pygame.mouse.get_pos()
                    cube_x = x // cube_size_x
                    cube_y = y // cube_size_y
                    if cubes[cube_x][cube_y] == 0:
                        cubes[cube_x][cube_y] = selected_cube
                    else:
                        cubes[selected_offset[0]][selected_offset[1]] = selected_cube
                selected_cube = None
                selected_offset = None
            elif event.type == pygame.MOUSEMOTION:
                if selected_cube is not None:
                    x, y = pygame.mouse.get_pos()
                    cube_x = x // cube_size_x
                    cube_y = y // cube_size_y
                    selected_offset = (cube_x, cube_y)
        
                    
        screen.fill(WHITE)
        draw_cubes(screen, cubes)
        draw_grid(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()