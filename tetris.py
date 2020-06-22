import sys
import random
import itertools
import time
import numpy as np
import pygame 

pygame.init()
# width of the rectangle
SCALE = 20
# width and height of the board 
W = 10
H = 20

screen = pygame.display.set_mode((W * SCALE, H * SCALE))
pygame.display.set_caption('Tetris')

board = np.zeros((H,W), dtype = int)

color = {
    0: (0,0,0),
    1: (255,255,255),
    2: (255,0,0),
    3: (0,255,0),
    4: (255,255,0),
    5: (0,0,255),
    6: (255,150,0),
    7: (255,0,255)
}

shape = {
    'O': np.array([[1,1],[1,1]]),
    'J': np.array([[2,0,0],[2,2,2]]),
    'I': np.array([[3,3,3,3]]),
    'L': np.array([[0,0,4],[4,4,4]]),
    'S': np.array([[0,5,5],[5,5,0]]),
    'T': np.array([[0,6,0],[6,6,6]]),
    'Z': np.array([[7,7,0],[0,7,7]])
}

dropping_shape = 'O'
x_shape = 0
y_shape = 0
orientation = 0

# text related - counting points
font = pygame.font.SysFont('Bradley Hand', 24)
text = {}
point = 0
 
def render_text():
     global text
     text = font.render(f'points:{point}', True,(255,255,255))
render_text()

def get_shape():
    array  = shape[dropping_shape]
    array = np.rot90(array, orientation)
    return array 

def display_shape(copy=True):
    """Return a copy of the board with the shape added to it.
    If copy=False, modify the original board."""
    new_board = np.copy(board) if copy else board

    array = get_shape()
    target_window = new_board[y_shape:y_shape+len(array), x_shape:array.shape[1]+x_shape]

    # Place shape (magic)
    collision = np.any(target_window[array > 0] > 0)
    target_window[array > 0] = array[array > 0]
    return (new_board, collision)

def draw_board(board):
    """Display the given board to the screen."""
    for y, rows in enumerate(board):
        for x, item in enumerate(rows):
            rect = pygame.Rect(x*SCALE, y*SCALE, SCALE, SCALE)
            pygame.draw.rect(screen, color[item],rect)

def check_coor():
    """Check that the shape is in bounds, and if not, correct the coordinates."""
    global x_shape, y_shape
    array = get_shape()
    x_shape = max(0, x_shape)
    x_shape = min(W - array.shape[1], x_shape)
    y_shape = min(H - array.shape[0], y_shape)

def check_landed():
    """Check if the shape has landed on existing blocks."""
    global y_shape
    array = get_shape()

    if y_shape == H - len(array):
        reset_shape()
    else:
        y_shape += 1
        _, collision = display_shape()
        y_shape -= 1
        if collision:
            reset_shape()

def delete_line():
    global point
    for y, rows in enumerate(board):
        if not 0 in rows:
            board[len(board)-y:] = board[:y]
            point += 10
            render_text()

def reset_shape():
    global y_shape
    global x_shape
    global dropping_shape
    display_shape(copy=False)
    dropping_shape =  random.choice(list(shape.keys()))
    x_shape = int(W/2)
    y_shape = 0
    

for frame in itertools.count():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_shape -= 1
                check_coor()
                if display_shape()[1]:
                    x_shape += 1
            if event.key == pygame.K_RIGHT:
                x_shape += 1
                check_coor()
                if display_shape()[1]:
                    x_shape -= 1
            if event.key == pygame.K_DOWN:
                check_landed()
                y_shape += 1
            if event.key == pygame.K_UP:
                orientation += 1
                orientation %= 4
    check_coor()
    copy = display_shape()[0]
    delete_line()
    draw_board(copy)
    screen.blit(text, (10,5))
    if frame % 10 == 0:
        check_landed()
        y_shape += 1
    pygame.display.flip()
    time.sleep(0.05)
