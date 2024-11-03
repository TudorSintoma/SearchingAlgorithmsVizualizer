import pygame, sys
from pygame.locals import *
from collections import deque
import time
import util

pygame.init()

# Set up FPS
FPS = 60
FramePerSec = pygame.time.Clock()


# Colors stuff
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (169, 169, 169)
ORANGE = (255, 165, 0)

MAGENTA = (255, 0, 255)
LIGHT_ORANGE = (255, 185, 130)
LIGHT_GREEN = (60, 179, 113)
TEAL = (0, 128, 128)
LIGHT_RED = (255, 102, 102)

colored_cells = {}
color = GREEN   #first color will be green


#Display stuff
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Maze Runner")


#Grid blocks stuff
startX = 0
startY = 0
endX = 0
endY = 0
blockSize = 20
cost_cells = {}
setting_costs = False


# Algorithm stuff
algorithm_active = False
algorithm_structure = None
algorithm_path = []
end_found = False
algorithm_start_time = 0
NONE = 0
BFS = 1
DFS = 2
UFC = 3
ASTAR = 4
algorithm = NONE


font = pygame.font.Font(None, 25)


def init_costs():
    for i in range (0, SCREEN_WIDTH, blockSize):
        for j in range (0, SCREEN_HEIGHT, blockSize):
            cost_cells[(i,j)] = 0


def set_cost(mouse_x, mouse_y):
    grid_x = (mouse_x // blockSize) * blockSize 
    grid_y = (mouse_y // blockSize) * blockSize 
    if 0 <= grid_x < SCREEN_WIDTH and 0 <= grid_y < SCREEN_HEIGHT:
        if colored_cells.get((grid_x, grid_y)) not in (GREEN, RED, BLUE):
            cost_cells[(grid_x, grid_y)] += 1


def drawGrid():
    col = BLACK
    for i in range (0, SCREEN_WIDTH, blockSize):
        for j in range (0, SCREEN_HEIGHT, blockSize):
            rect = pygame.Rect(i, j, blockSize, blockSize)
            pygame.draw.rect(DISPLAYSURF, BLACK, rect, 1)
            if cost_cells[(i, j)] != 0:
                n = cost_cells[(i, j)]
                if 2 <= n < 4:
                    col = LIGHT_GREEN
                elif 4 <= n < 6:
                    col = TEAL
                elif 6 <= n < 8:
                    col = LIGHT_ORANGE
                elif 8 <= n < 10:
                    col = MAGENTA
                elif n >= 10:
                    col = LIGHT_RED
                else:
                    col = BLACK
                text = font.render(str(cost_cells[(i,j)]), True, col)
                text_rect = text.get_rect(center=(i + blockSize// 2, j + blockSize // 2))
                DISPLAYSURF.blit(text, text_rect)




def colorCell(mouse_x, mouse_y):
    global startX, startY, endX, endY, color
    grid_x = (mouse_x // blockSize) * blockSize 
    grid_y = (mouse_y // blockSize) * blockSize 
    rect = pygame.Rect(grid_x, grid_y, blockSize, blockSize)
    pygame.draw.rect(DISPLAYSURF, color, rect)
    colored_cells[(grid_x, grid_y)] = color

    if color == RED:    #end point is RED
        endX, endY = grid_x, grid_y

    if color == GREEN:  #start point is GREEN
        startX, startY = grid_x, grid_y



def initialize_algorithm(start, end, structure):
    global algorithm_structure, algorithm_path, end_found, algorithm_start_time, algorithm_active
    algorithm_structure = structure
    algorithm_structure.push((start, []))  # Initialize with start position
    algorithm_path = []
    end_found = False
    algorithm_start_time = pygame.time.get_ticks()
    algorithm_active = True


def initialize_algorithm_cost(start, end, structure):
    global algorithm_structure, algorithm_path, end_found, algorithm_start_time, algorithm_active
    algorithm_structure = structure
    algorithm_structure.push((start, [], 0), 0)  # Initialize with start position
    algorithm_path = []
    end_found = False
    algorithm_start_time = pygame.time.get_ticks()
    algorithm_active = True




def ufc_step():
    global algorithm_structure, end_found, algorithm_path, algorithm_active
    if end_found or algorithm_structure.isEmpty():
        algorithm_active = False
        return
    
    (x, y), path, cost = algorithm_structure.pop()
    if (x, y) == (endX, endY):  # Found end
        algorithm_path = path + [(x, y)]
        end_found = True
        return

    neighbors_to_color = []
    for dx, dy in [(-blockSize, 0), (blockSize, 0), (0, -blockSize), (0, blockSize)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < SCREEN_WIDTH and 0 <= ny < SCREEN_HEIGHT:
            if (nx, ny) not in colored_cells or colored_cells.get((nx, ny)) not in (BLUE, GREY):
                neighbors_to_color.append((nx, ny))
                new_cost = cost + cost_cells.get((nx, ny))
                algorithm_structure.push(((nx, ny), path + [(x, y)], new_cost), new_cost)


    for neighbor in neighbors_to_color:
        if colored_cells.get(neighbor) != GREEN and colored_cells.get(neighbor) != RED:
            colored_cells[neighbor] = GREY

        

def as_step():
    global algorithm_structure, end_found, algorithm_path, algorithm_active
    if end_found or algorithm_structure.isEmpty():
        algorithm_active = False
        return
    
    (x, y), path, cost = algorithm_structure.pop()
    if (x, y) == (endX, endY):  # Found end
        algorithm_path = path + [(x, y)]
        end_found = True
        return

    neighbors_to_color = []
    for dx, dy in [(-blockSize, 0), (blockSize, 0), (0, -blockSize), (0, blockSize)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < SCREEN_WIDTH and 0 <= ny < SCREEN_HEIGHT:
            if (nx, ny) not in colored_cells or colored_cells.get((nx, ny)) not in (BLUE, GREY):
                neighbors_to_color.append((nx, ny))
                h_cost = abs(nx - endX) + abs(ny - endY)  #Manhattan distance
                f_cost = cost + h_cost
                algorithm_structure.push(((nx, ny), path + [(x, y)], f_cost), f_cost)

    for neighbor in neighbors_to_color:
        if colored_cells.get(neighbor) != GREEN and colored_cells.get(neighbor) != RED:
            colored_cells[neighbor] = GREY


def fs_step():
    global algorithm_structure, end_found, algorithm_path, algorithm_active
    if end_found or algorithm_structure.isEmpty():
        algorithm_active = False
        return
    
    (x, y), path = algorithm_structure.pop()
    if (x, y) == (endX, endY):  # Found end
        algorithm_path = path + [(x, y)]
        end_found = True
        return

    neighbors_to_color = []
    for dx, dy in [(-blockSize, 0), (blockSize, 0), (0, -blockSize), (0, blockSize)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < SCREEN_WIDTH and 0 <= ny < SCREEN_HEIGHT:
            if (nx, ny) not in colored_cells or colored_cells.get((nx, ny)) not in (BLUE, GREY):
                neighbors_to_color.append((nx, ny))
                algorithm_structure.push(((nx, ny), path + [(x, y)]))


    for neighbor in neighbors_to_color:
        if colored_cells.get(neighbor) != GREEN and colored_cells.get(neighbor) != RED:
            colored_cells[neighbor] = GREY




def display_path():
    global algorithm_path
    for (px, py) in algorithm_path:
        if colored_cells.get((px,py)) not in (GREEN, RED):
            colored_cells[(px, py)] = ORANGE  # path is ORANGE



def main():

    #setup main
    init_costs()
    drawGrid()
    mouse_held = False
    global color, algorithm, algorithm_active, algorithm_start_time, setting_costs

    while True:
        for event in pygame.event.get():    #handle events

            if event.type == pygame.QUIT:   #quit
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and not algorithm_active: #color cell or set costs
                mouse_held = True
                if setting_costs == True:
                    set_cost(*pygame.mouse.get_pos())
                else:
                    colorCell(*pygame.mouse.get_pos())

            elif event.type == pygame.MOUSEBUTTONUP:    #change color, first we fill the starting position, then the ending position, then the walls
                mouse_held = False
                if color == RED:
                    color = BLUE
                if color == GREEN:
                    color = RED

            elif event.type == pygame.KEYDOWN and color == BLUE and algorithm == NONE:  #start algorithm
                print(f"Start: ({startX}, {startY}), End: ({endX}, {endY})")

                if event.key == pygame.K_c:     #set costs
                    setting_costs = True

                if event.key == pygame.K_b:     #press b for BFS
                    algorithm = BFS
                    queue = util.Queue()
                    initialize_algorithm((startX, startY), (endX, endY), queue)

                elif event.key == pygame.K_d:   #press d for DFS
                    algorithm = DFS
                    stack = util.Stack()
                    initialize_algorithm((startX, startY), (endX, endY), stack)

                elif event.key == pygame.K_a:   #press a for ASTAR
                    algorithm = ASTAR
                    pqueue = util.PriorityQueue()
                    initialize_algorithm_cost((startX, startY), (endX, endY), pqueue)

                elif event.key == pygame.K_u: #press u for UFC
                    algorithm = UFC
                    pqueue = util.PriorityQueue()
                    initialize_algorithm_cost((startX, startY), (endX, endY), pqueue)


        if mouse_held and color == BLUE and not algorithm_active:   #walls are BLUE, we want to be able to draw them by click and drag
            if setting_costs == True:
                set_cost(*pygame.mouse.get_pos())
            else:
                colorCell(*pygame.mouse.get_pos())


        current_time = pygame.time.get_ticks()
        if algorithm_active and end_found == False and current_time - algorithm_start_time >= 100:  # 0.1 seconds delay
            if algorithm == BFS or algorithm == DFS:
                fs_step()
            elif algorithm == UFC:
                ufc_step()
            elif algorithm == ASTAR:
                as_step()
                
            algorithm_start_time = current_time  #Reset the start time for the next step


        if end_found == True:
            display_path()  #Show the path if found


        #Draw everything new on screen
        DISPLAYSURF.fill(WHITE)  
        for (x, y), cell_color in colored_cells.items():  
            pygame.draw.rect(DISPLAYSURF, cell_color, pygame.Rect(x, y, blockSize, blockSize))
        drawGrid()  
        pygame.display.update()
        FramePerSec.tick(FPS)

main()