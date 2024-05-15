import pygame
import sys
import random

PLAYER = "Player"
DIFFICULTY = "easy"


if DIFFICULTY.lower() == "random":
    DIFFICULTY = random.choice(["easy","hard"])
    print(DIFFICULTY)

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WIDTH = 800
HEIGHT = 600
if DIFFICULTY == "hard":
    WIDTH = 1000
    HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pygame Template')
clock = pygame.time.Clock()
timer_font = pygame.font.SysFont(None, 24)
game_over_font = pygame.font.SysFont(None, 72)
sub_font = pygame.font.SysFont(None, 48)
# Set up the game

class Leaderboard():
    def __init__(self):
        pass # TODO Implement leaderboard system

class Cell():
    def __init__(self, x, y, w, index:tuple, screen=screen):
        self.x = x
        self.y = y
        self.index = index
        self.width = w
        self.rect = pygame.Rect(x, y, w, w)

        self.screen = screen

        self.is_mine = True if random.random() < 0.12 else False
        self.is_flagged = False
        self.is_open = False

    def populate_neighbors(self, grid):
        self.neighbors = []

        idx_x = self.index[0]
        idx_y = self.index[1]

        if idx_x != 0:
            if idx_y != 0:
                self.neighbors.append(grid[idx_x - 1][idx_y - 1])
            self.neighbors.append(grid[idx_x - 1][idx_y])
            if idx_y != len(grid[idx_x]) - 1:
                self.neighbors.append(grid[idx_x - 1][idx_y + 1])
        if idx_x != len(grid) - 1:
            if idx_y != 0:
                self.neighbors.append(grid[idx_x + 1][idx_y - 1])
            self.neighbors.append(grid[idx_x + 1][idx_y])
            if idx_y != len(grid[idx_x]) - 1:
                self.neighbors.append(grid[idx_x + 1][idx_y + 1])
        if idx_y != len(grid[idx_x]) - 1:
            self.neighbors.append(grid[idx_x][idx_y + 1])
        if idx_y != 0:
            self.neighbors.append(grid[idx_x][idx_y - 1])
        

        self.num_adjacent_mines = len([cell for cell in self.neighbors if cell.is_mine])
        if self.num_adjacent_mines:
            self.font = pygame.font.SysFont(None, int(self.width*0.7))
            self.text = self.font.render(str(self.num_adjacent_mines), True, (0, 0, 0))


    def draw(self):
        if self.is_open:
            pygame.draw.rect(screen, (204, 204, 204), self.rect)
            pygame.draw.rect(screen, (102, 102, 102), self.rect, 1)
            if cell.is_mine:
                pygame.draw.circle(screen, (51, 51, 51), (self.x + self.width/2, self.y + self.width/2), self.width/4)
                pygame.draw.line(screen, (51, 51, 51), self.rect.bottomleft, self.rect.topright, 3)
                pygame.draw.line(screen, (51, 51, 51), self.rect.topleft, self.rect.bottomright, 3)
                if cell.is_flagged:
                    pygame.draw.circle(screen, (255, 0, 0), (self.x + self.width/2, self.y + self.width/2), self.width/4)
            elif self.num_adjacent_mines:
                self.screen.blit(self.text, (self.x + self.width/2 - self.text.get_width()/2, self.y + self.width/2 - self.text.get_height()/2))
        else:
            pygame.draw.rect(screen, (255, 255, 255), self.rect)
            pygame.draw.rect(screen, (153, 153, 153), self.rect, 1)
            if self.is_flagged:
                pygame.draw.circle(screen, (255, 0, 0), (self.x + self.width/2, self.y + self.width/2), self.width/4)
    
    def flag(self):
        if not self.is_open:
            self.is_flagged = not self.is_flagged
    
    def clicked(self):
        self.is_open = True
        if self.is_mine:
            global game_over
            game_over = True
        elif not self.num_adjacent_mines:
            for cell in self.neighbors:
                if not cell.is_open:
                    cell.clicked()
        
        if not self.is_mine:
            self.is_flagged = False


num_cols = 20 if DIFFICULTY == "easy" else 40
temp_w = WIDTH // num_cols
while not bool(WIDTH % temp_w == 0 and HEIGHT % temp_w == 0):
        num_cols -= 1
        temp_w = WIDTH // num_cols
        print(num_cols)

w = WIDTH // num_cols
print(w)

cells = [[Cell(x, y, w, (x//w,y//w)) for y in range(0, HEIGHT, w)] for x in range(0, WIDTH, w)]
non_mines = [cell for row in cells for cell in row if not cell.is_mine]
for row in cells:
    for cell in row:
        cell.populate_neighbors(cells)
print(len([cell for row in cells for cell in row if cell.is_mine]))

def reset():
    global cells, non_mines, timer_start
    cells = [[Cell(x, y, w, (x//w,y//w)) for y in range(0, HEIGHT, w)] for x in range(0, WIDTH, w)]
    non_mines = [cell for row in cells for cell in row if not cell.is_mine]
    for row in cells:
        for cell in row:
            cell.populate_neighbors(cells)
    timer_start = pygame.time.get_ticks()

def seconds_to_string(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

# Main game loop
running = True
game_over = False
game_win = False
DEBUG = False
timer_start = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if not game_over:
                if event.button == 3:
                    for row in cells:
                        for cell in row:
                            if cell.rect.collidepoint(mouse_pos):
                                cell.flag()
                if event.button == 1:
                    for row in cells:
                        for cell in row:
                            if cell.rect.collidepoint(mouse_pos):
                                cell.clicked()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if game_over:
                    reset()
                    game_over = False
                    game_win = False
            if event.key == pygame.K_d:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL and mods & pygame.KMOD_ALT and not game_over:
                    DEBUG = not DEBUG
            if event.key == pygame.K_w:
                if DEBUG:
                    for cell in non_mines:
                        cell.is_open = True

    # Game logic goes here
    if not game_over:
        if not game_win:
            timer = (pygame.time.get_ticks() - timer_start) // 1000
        if all(cell.is_open for cell in non_mines):
            game_win = True
            game_over = True
    else:
        if not game_win: # loss
            for row in cells:
                for cell in row:
                    if cell.is_mine:
                        cell.is_open = True

    # Draw everything
    screen.fill((0, 0, 0))

    for row in cells:
        for cell in row:
            cell.draw()
    

    timer_colour = (0,0,0) if not DEBUG else (255,0,0)
    timer_text = timer_font.render(seconds_to_string(timer), True, timer_colour)
    screen.blit(timer_text, (10, 10))

    if game_win:
        win_text = game_over_font.render("YOU WIN!", True, (0, 255, 0), (200,200,200))
        score_text = sub_font.render(f"Your time: {seconds_to_string(timer)}", True, (0, 0, 0), (200,200,200))
        retry_text = sub_font.render("Press R to retry", True, (0, 0, 0), (200,200,200))
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - win_text.get_height()//2))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, (HEIGHT//2) + (score_text.get_height()//2) + (score_text.get_height())))
        screen.blit(retry_text, (WIDTH//2 - retry_text.get_width()//2, (HEIGHT//2) + (retry_text.get_height()//2) + (retry_text.get_height() * 2.5)))

    elif game_over:
        lose_text = game_over_font.render("KABOOM!", True, (255, 0, 0), (200,200,200))
        num_false_flags = len([cell for row in cells for cell in row if cell.is_flagged and not cell.is_mine])
        score_text = sub_font.render(f"False flags: {num_false_flags}", True, (0, 0, 0), (200,200,200))
        retry_text = sub_font.render("Press R to retry", True, (0, 0, 0), (200,200,200))
        screen.blit(lose_text, (WIDTH//2 - lose_text.get_width()//2, HEIGHT//2 - lose_text.get_height()//2))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, (HEIGHT//2) + (score_text.get_height()//2) + (score_text.get_height())))
        screen.blit(retry_text, (WIDTH//2 - retry_text.get_width()//2, (HEIGHT//2) + (retry_text.get_height()//2) + (retry_text.get_height() * 2.5)))
    


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
