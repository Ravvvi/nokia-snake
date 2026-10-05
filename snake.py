import pygame
import sys
import random
import os
import json

# Initialize Pygame
pygame.init()
pygame.font.init()

# Game Constants
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE
BASE_FPS = 8
MAX_FPS = 12

# File for High Scores
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCORE_FILE = os.path.join(BASE_DIR, "snake_scores.json")

# Classic Nokia 3310 Color Palette
NOKIA_BG = (168, 198, 78)    
NOKIA_FG = (33, 40, 25)      

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Classic Nokia Snake (Level System)")
clock = pygame.time.Clock()

font_title = pygame.font.SysFont("Courier New", 40, bold=True)
font_menu = pygame.font.SysFont("Courier New", 18, bold=True)
font_score = pygame.font.SysFont("Courier New", 18, bold=True)

def load_scores():
    try:
        with open(SCORE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_score(new_score):
    if new_score == 0: 
        return 
    scores = load_scores()
    scores.append(new_score)
    scores.sort(reverse=True) 
    scores = scores[:5]
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f)

def spawn_food(snake_body, walls_blocks):
    while True:
        x = random.randint(0, GRID_WIDTH - 1) * CELL_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
        if (x, y) not in snake_body and (x, y) not in walls_blocks:
            return (x, y)

def build_level(level):
    # Adjust spawn position based on level
    if level == 3:
        start_x = (GRID_WIDTH // 4) * CELL_SIZE
    else:
        start_x = (GRID_WIDTH // 2) * CELL_SIZE
        
    start_y = (GRID_HEIGHT // 2) * CELL_SIZE
    
    snake = [
        (start_x, start_y),
        (start_x - CELL_SIZE, start_y),
        (start_x - 2 * CELL_SIZE, start_y)
    ]
    direction = "RIGHT"
    next_direction = "RIGHT"
    
    walls = []
    if level == 2:
        # Level 2: Hard Border Walls
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            walls.append((x, 0)) 
            walls.append((x, SCREEN_HEIGHT - CELL_SIZE)) 
        for y in range(CELL_SIZE, SCREEN_HEIGHT - CELL_SIZE, CELL_SIZE):
            walls.append((0, y)) 
            walls.append((SCREEN_WIDTH - CELL_SIZE, y)) 
            
    elif level == 3:
        # Level 3: Full Vertical Split Wall
        mid_x = (GRID_WIDTH // 2) * CELL_SIZE
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            walls.append((mid_x, y))
            
    elif level == 4:
        # Level 4: Custom Drawn Walls 
        # Horizontal wall on top right
        for x in range(12 * CELL_SIZE, SCREEN_WIDTH, CELL_SIZE):
            walls.append((x, 5 * CELL_SIZE))
            
        # Vertical wall on bottom left
        for y in range(9 * CELL_SIZE, SCREEN_HEIGHT, CELL_SIZE):
            walls.append((7 * CELL_SIZE, y))
            
        # Vertical wall on bottom right
        for y in range(12 * CELL_SIZE, SCREEN_HEIGHT, CELL_SIZE):
            walls.append((22 * CELL_SIZE, y))

    food = spawn_food(snake, walls)
    score = 0
    return snake, direction, next_direction, food, score, walls

# --- INITIAL GAME STATE ---
game_state = "MENU"
running = True
high_scores = load_scores()
current_fps = BASE_FPS
current_level = 1

snake, direction, next_direction, food, score, walls = build_level(current_level)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if game_state == "MENU":
                # Level Selection Logic
                if event.key == pygame.K_1:
                    current_level = 1
                    snake, direction, next_direction, food, score, walls = build_level(current_level)
                    current_fps = BASE_FPS
                    game_state = "PLAYING"
                    high_scores = load_scores()
                elif event.key == pygame.K_2:
                    current_level = 2
                    snake, direction, next_direction, food, score, walls = build_level(current_level)
                    current_fps = BASE_FPS
                    game_state = "PLAYING"
                    high_scores = load_scores()
                elif event.key == pygame.K_3:
                    current_level = 3
                    snake, direction, next_direction, food, score, walls = build_level(current_level)
                    current_fps = BASE_FPS
                    game_state = "PLAYING"
                    high_scores = load_scores()
                elif event.key == pygame.K_4:
                    current_level = 4
                    snake, direction, next_direction, food, score, walls = build_level(current_level)
                    current_fps = BASE_FPS
                    game_state = "PLAYING"
                    high_scores = load_scores()
                    
            elif game_state == "GAMEOVER":
                if event.key == pygame.K_RETURN:
                    game_state = "MENU"
                    high_scores = load_scores()

            elif game_state == "PLAYING":
                if event.key == pygame.K_UP and direction != "DOWN":
                    next_direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    next_direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    next_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    next_direction = "RIGHT"

    # --- GAME LOGIC & DRAWING ---
    screen.fill(NOKIA_BG)

    if game_state == "MENU":
        pygame.draw.rect(screen, NOKIA_FG, (10, 10, SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), 4)
        
        title = font_title.render("SNAKE II", True, NOKIA_FG)
        lvl1_txt = font_menu.render("Press [1] - Lvl 1", True, NOKIA_FG)
        lvl2_txt = font_menu.render("Press [2] - Lvl 2", True, NOKIA_FG)
        lvl3_txt = font_menu.render("Press [3] - Lvl 3", True, NOKIA_FG)
        lvl4_txt = font_menu.render("Press [4] - Lvl 4", True, NOKIA_FG)
        score_title = font_menu.render("TOP SCORES", True, NOKIA_FG)
        
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))
        screen.blit(lvl1_txt, (SCREEN_WIDTH//2 - lvl1_txt.get_width()//2, 70))
        screen.blit(lvl2_txt, (SCREEN_WIDTH//2 - lvl2_txt.get_width()//2, 100))
        screen.blit(lvl3_txt, (SCREEN_WIDTH//2 - lvl3_txt.get_width()//2, 130))
        screen.blit(lvl4_txt, (SCREEN_WIDTH//2 - lvl4_txt.get_width()//2, 160))
        screen.blit(score_title, (SCREEN_WIDTH//2 - score_title.get_width()//2, 210))
        
        if not high_scores:
            no_score = font_score.render("No scores yet!", True, NOKIA_FG)
            screen.blit(no_score, (SCREEN_WIDTH//2 - no_score.get_width()//2, 240))
        else:
            for i, s in enumerate(high_scores):
                s_txt = font_score.render(f"{i+1}.   {s}", True, NOKIA_FG)
                screen.blit(s_txt, (SCREEN_WIDTH//2 - s_txt.get_width()//2, 240 + (i * 25)))

    elif game_state == "PLAYING":
        direction = next_direction
        
        head_x, head_y = snake[0]
        
        if direction == "UP": head_y -= CELL_SIZE
        elif direction == "DOWN": head_y += CELL_SIZE
        elif direction == "LEFT": head_x -= CELL_SIZE
        elif direction == "RIGHT": head_x += CELL_SIZE
            
        if current_level in [1, 3, 4]:
            if head_x < 0:
                head_x = SCREEN_WIDTH - CELL_SIZE
            elif head_x >= SCREEN_WIDTH:
                head_x = 0
            if head_y < 0:
                head_y = SCREEN_HEIGHT - CELL_SIZE
            elif head_y >= SCREEN_HEIGHT:
                head_y = 0
                
        new_head = (head_x, head_y)
        
        is_dead = False
        
        # Self Collision
        if new_head in snake:
            is_dead = True
        elif current_level == 2 and (head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT):
            is_dead = True
        elif current_level in [2, 3, 4] and new_head in walls:
            is_dead = True
            
        if is_dead:
            save_score(score)
            game_state = "GAMEOVER"
        else:
            snake.insert(0, new_head)
            if new_head == food:
                score += 10
                food = spawn_food(snake, walls)
                current_fps = min(MAX_FPS, BASE_FPS + (len(snake) - 3) // 3)
            else:
                snake.pop() 

        # Draw Walls
        for wx, wy in walls:
            wall_rect = pygame.Rect(wx, wy, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, NOKIA_FG, wall_rect)
            inner_bg = pygame.Rect(wx + 4, wy + 4, CELL_SIZE - 8, CELL_SIZE - 8)
            pygame.draw.rect(screen, NOKIA_BG, inner_bg)

        # Draw Food
        food_rect = pygame.Rect(food[0] + 2, food[1] + 2, CELL_SIZE - 4, CELL_SIZE - 4)
        pygame.draw.rect(screen, NOKIA_FG, food_rect)

        # Draw Snake
        for i, segment in enumerate(snake):
            seg_rect = pygame.Rect(segment[0] + 1, segment[1] + 1, CELL_SIZE - 2, CELL_SIZE - 2)
            pygame.draw.rect(screen, NOKIA_FG, seg_rect)

    elif game_state == "GAMEOVER":
        pygame.draw.rect(screen, NOKIA_FG, (10, 10, SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), 4)
        
        end_text = font_title.render("GAME OVER", True, NOKIA_FG)
        score_txt = font_menu.render(f"Final Score: {score}", True, NOKIA_FG)
        retry_txt = font_score.render("Press [ENTER] to return", True, NOKIA_FG)
        
        screen.blit(end_text, (SCREEN_WIDTH//2 - end_text.get_width()//2, SCREEN_HEIGHT//2 - 60))
        screen.blit(score_txt, (SCREEN_WIDTH//2 - score_txt.get_width()//2, SCREEN_HEIGHT//2 + 10))
        screen.blit(retry_txt, (SCREEN_WIDTH//2 - retry_txt.get_width()//2, SCREEN_HEIGHT//2 + 60))

    pygame.display.flip()
    
    if game_state == "PLAYING":
        clock.tick(current_fps)
    else:
        clock.tick(15) 

pygame.quit()
sys.exit()