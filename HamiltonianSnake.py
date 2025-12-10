# Snake game solved using a Hamiltonian Cycle
# Grid size can be changed to any even value
# Clicking inside the game window or closing it can cause it to crash so don't touch anything while it is running
# Movement, fruit spawn, and collision all operate on grid coordinates.


import pygame
import time
import random


# Game Settings
snake_speed = 15        # Speed of the snake, can be raised to simulate faster
WINDOW_SIZE = 720       # Size of display window
GRID_SIZE = 10          # Size of grid (x and y axis), will be square in shape
CELL_SIZE = WINDOW_SIZE // GRID_SIZE  # Size of each grid cell


# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red   = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue  = pygame.Color(0, 0, 255)


# Pygame Setup
pygame.init()
pygame.display.set_caption("Hamiltonian Snake")
game_window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
fps = pygame.time.Clock()


# Initial Snake State (grid coords)
snake_position = [1, GRID_SIZE/2]   # Start position for snake head
snake_body = [
    [3, GRID_SIZE/2],         # Starting head position
    [2, GRID_SIZE/2],         # Starting body segment 1 position
    [1, GRID_SIZE/2]          # Starting body segment 2 position
]


# Set snake starting direction
direction = 'Right'  
change_to = direction


#Create path of Hamiltonian Cycle which snake will follow
def generate_hamiltonian_cycle(rows, cols):
    path = []
    for col in range(cols):
        if col % 2 == 0:  # even column: top to bottom
            if col == 0:
                for row in range(rows):
                    path.append([col, row])
            else:
                for row in range(rows):
                    if row !=0:
                        path.append([col, row])
        else:  # odd column: bottom to top
            if col == cols - 1:
                for row in reversed(range(rows)):
                    path.append([col, row])
                for c in reversed(range(cols)):
                    if (c != 0) & (c!= cols-1):
                        path.append([c, 0])
            else:
                for row in reversed(range(rows)):
                    if row !=0:
                        path.append([col, row])
    return path


#Call function and store in 'cycle' variable
cycle = generate_hamiltonian_cycle(GRID_SIZE, GRID_SIZE)


#Find next postition's coordinates
def findNextPos(snake_position):
    for i in range(len(cycle)):
        if cycle[i] == snake_position:
            if i != (len(cycle) -1):
                return cycle[i+1]
            else:
                return cycle[0]


#Use current position and next postition to get direction
def getDirection(snake_position, next_cell):
    if snake_position[0] < next_cell[0]:
        newDir = 'RIGHT'
    elif snake_position[0] > next_cell[0]:
        newDir = 'LEFT'
    elif snake_position[1] < next_cell[1]:
        newDir = 'DOWN'
    elif snake_position[1] > next_cell[1]:
        newDir = 'UP'
    return newDir


#Check if new fruit is in a space not already taken by snake's body, otherwise generate a new valid location
def isValidFruitPostition(snake_body, fruit_pos):
    for i in range(len(snake_body)):
        if snake_body[i] == fruit_pos:
            rand = random.randrange(1, (len(cycle) - len(snake_body)))
            for i in range(len(cycle)):
                if cycle[i] == snake_position:
                    fruit_pos = cycle[(i + rand) % (len(cycle))]
    return fruit_pos


# Generate a first fruit in a random grid position, ensuring it isn't inside the snake at the start
fruit_position = [random.randrange(0, GRID_SIZE),
                  random.randrange(0, GRID_SIZE)]
fruit_position = isValidFruitPostition(snake_body, fruit_position)
fruit_spawn = True

score = 0


# Display the current score
def show_score(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(f"Score : {score}", True, color)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (10, 10)
    game_window.blit(score_surface, score_rect)


# Game Over Screen
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render(
        f'Your Score is : {score}', True, red
    )
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (WINDOW_SIZE / 2, WINDOW_SIZE / 4)

    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)

    pygame.quit()
    quit()


# Main Game Loop
while True:

    # Check if direction of snake needs to change according to the Hamiltonian cycle path
    change_to = getDirection(snake_position, findNextPos(snake_position))


    # Prevent snake from reversing directly
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    elif change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    elif change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    elif change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'


    # Move snake using grid steps
    if direction == 'UP':
        snake_position[1] -= 1
    elif direction == 'DOWN':
        snake_position[1] += 1
    elif direction == 'LEFT':
        snake_position[0] -= 1
    elif direction == 'RIGHT':
        snake_position[0] += 1


    # Snake growth & fruit collision
    snake_body.insert(0, list(snake_position))

    if snake_position == fruit_position:    # Eat fruit, gain score
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:     # Spawn a new fruit, ensuring it isn't inside the snake's body
        fruit_position = [random.randrange(0, GRID_SIZE),
                          random.randrange(0, GRID_SIZE)]
        
        fruit_position = isValidFruitPostition(snake_body, fruit_position)
        fruit_spawn = True


    # Drawing everything
    game_window.fill(black)


    # Draw snake
    for pos in snake_body:
        if pos == snake_position:   # Make snake's head blue for easier distinction
            pygame.draw.rect(
            game_window,
            blue,
            pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE,
                        CELL_SIZE, CELL_SIZE)
            )
        else:
            pygame.draw.rect(       # Make snake's body green
                game_window,
                green,
                pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE,
                            CELL_SIZE, CELL_SIZE)
            )


    # Draw fruit
    pygame.draw.rect(
        game_window,
        red,
        pygame.Rect(fruit_position[0] * CELL_SIZE,
                    fruit_position[1] * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE)
    )


    # Game Over Conditions
    if (snake_position[0] < 0 or snake_position[0] >= GRID_SIZE or
        snake_position[1] < 0 or snake_position[1] >= GRID_SIZE):
        game_over()


    # Check self-collision
    for block in snake_body[1:]:
        if snake_position == block:
            game_over()


    show_score(white, 'times new roman', 20)    # Display score in the top left corner


    pygame.display.update()     # Update the game
    fps.tick(snake_speed)
