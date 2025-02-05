import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# ----- Game Settings -----
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Car Race")

clock = pygame.time.Clock()
FPS = 60

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

# Define two lane center positions (left and right)
lane_x = [WIDTH // 4, 3 * WIDTH // 4]

# ----- Player Car Settings -----
player_width, player_height = 50, 90
player_lane = 0  # start in left lane (0: left, 1: right)
player_x = lane_x[player_lane] - player_width // 2
player_y = HEIGHT - player_height - 10  # near the bottom
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

# ----- Obstacle Settings -----
obstacle_width, obstacle_height = 50, 90
obstacles = []  # list to hold obstacle Rects

# Use a timer to control when new obstacles are added (in milliseconds)
obstacle_interval = 1500  # new obstacle every 1500 ms
last_obstacle_time = pygame.time.get_ticks()

# ----- Game Speed and Scoring -----
base_speed = 5  # starting speed of obstacles
game_speed = base_speed
score = 0

# Set up a font for displaying score and game-over text
font = pygame.font.SysFont(None, 36)

# ----- Game Functions -----
def reset_game():
    """Reset game variables to start a new game."""
    global obstacles, game_speed, score, player_lane, player_rect, last_obstacle_time
    obstacles = []
    game_speed = base_speed
    score = 0
    player_lane = 0
    player_rect.x = lane_x[player_lane] - player_width // 2
    last_obstacle_time = pygame.time.get_ticks()

def game_over():
    """Display a game over message and wait for a restart."""
    over_text = font.render("Game Over! Press Space to Restart", True, RED)
    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2,
                            HEIGHT // 2 - over_text.get_height() // 2))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
    reset_game()

# Start the game
reset_game()

# ----- Main Game Loop -----
running = True
while running:
    dt = clock.tick(FPS)  # time in milliseconds since last frame
    
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Change lanes when space bar is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Toggle between lane 0 and 1
                player_lane = 1 - player_lane
                player_rect.x = lane_x[player_lane] - player_width // 2

    # --- Update Game State ---
    current_time = pygame.time.get_ticks()
    # Spawn a new obstacle if enough time has passed
    if current_time - last_obstacle_time > obstacle_interval:
        # Randomly choose one of the two lanes for the new obstacle
        lane = random.choice([0, 1])
        obstacle_x = lane_x[lane] - obstacle_width // 2
        obstacle_y = -obstacle_height  # start just above the screen
        obstacles.append(pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height))
        last_obstacle_time = current_time

    # Increase score (distance traveled) based on game speed and time elapsed
    score += game_speed * dt / 1000  # dt is in ms, so divide by 1000 for seconds

    # Increase game speed gradually as the score increases.
    # (Here, every 50 points increases speed by 1 unit.)
    game_speed = base_speed + int(score / 50)
    
    # Update the positions of obstacles
    for obstacle in obstacles:
        obstacle.y += game_speed

    # Remove obstacles that have moved off the bottom of the screen
    obstacles = [obs for obs in obstacles if obs.y < HEIGHT]

    # Check for collisions between the player's car and any obstacle
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            game_over()

    # --- Drawing ---
    screen.fill(WHITE)
    
    # Optionally draw a dividing line between lanes
    pygame.draw.line(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)
    
    # Draw the player's car
    pygame.draw.rect(screen, BLUE, player_rect)
    
    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)
    
    # Draw the current score
    score_text = font.render(f"Score: {int(score)}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()

pygame.quit()
