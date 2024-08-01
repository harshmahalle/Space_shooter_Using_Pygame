import pygame
import random
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound effects

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
grey = (169, 169, 169)

# Set up display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")

# Clock
clock = pygame.time.Clock()

# Load and resize images for player, laser, and asteroid
player_img = pygame.image.load('images/player.jpg').convert_alpha()
# Resize player image
player_img = pygame.transform.scale(player_img, (60, 60))  
# Rotate image 180 degrees
#player_img = pygame.transform.rotate(player_img, 180)  

laser_img = pygame.image.load('images/laser.jpg').convert_alpha()
# Resize laser image
laser_img = pygame.transform.scale(laser_img, (10, 30))  

asteroid_img = pygame.image.load('images/asteroid.jpg').convert_alpha()
# Resize asteroid image
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))  

background_img = pygame.image.load('images/background.jpg').convert()

# Load sounds
laser_sound = pygame.mixer.Sound('sounds/laser.mp3')
hit_sound = pygame.mixer.Sound('sounds/asteroid-hitting-laser.mp3')
background_music = 'sounds/Sunset_Synthetics.mp3'

# Play background music
pygame.mixer.music.load(background_music)
# Loop the music
pygame.mixer.music.play(-1)  

# Button dimensions and colors
button_width = 200
button_height = 50
button_color = (100, 100, 255)
button_text_color = white

# Score
score = 0

def draw_button(surface, text, x, y, width, height, color, text_color):
    pygame.draw.rect(surface, color, pygame.Rect(x, y, width, height))
    font = pygame.font.SysFont(None, 36)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    surface.blit(text_surface, text_rect)

def draw_text(surface, text, x, y, size, color):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.x = screen_width // 2
        self.rect.y = screen_height - 70

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.x < screen_width - 60:
            self.rect.x += 5

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = laser_img
        self.rect = self.image.get_rect()
        self.rect.x = x + 27
        self.rect.y = y

    def update(self):
        self.rect.y -= 10
        if self.rect.y < 0:
            self.kill()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = asteroid_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 50)
        self.rect.y = random.randint(-100, -50)
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > screen_height:
            self.kill()

def show_game_over_screen():
    global score
    while True:
        screen.fill(black)
        draw_text(screen, f"Score: {score}", screen_width / 2 - 50, screen_height / 2 - 150, 36, white)
        draw_button(screen, "Restart", screen_width / 2 - button_width / 2, screen_height / 2 - button_height / 2 - 60, button_width, button_height, button_color, button_text_color)
        draw_button(screen, "Quit", screen_width / 2 - button_width / 2, screen_height / 2 - button_height / 2 + 10, button_width, button_height, button_color, button_text_color)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if screen_width / 2 - button_width / 2 <= mouse_pos[0] <= screen_width / 2 + button_width / 2:
                    if screen_height / 2 - button_height / 2 - 60 <= mouse_pos[1] <= screen_height / 2 - button_height / 2:
                        score = 0
                        # Restart the game
                        return True 
                    elif screen_height / 2 - button_height / 2 + 10 <= mouse_pos[1] <= screen_height / 2 + button_height / 2 + 10:
                        pygame.quit()
                        # Quit the game
                        sys.exit()  

def start_game():
    global score
    player = Player()
    all_sprites = pygame.sprite.Group()
    lasers = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    all_sprites.add(player)
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    laser = Laser(player.rect.x, player.rect.y)
                    all_sprites.add(laser)
                    lasers.add(laser)
                    # Play laser sound
                    laser_sound.play()  

        # Spawn asteroids randomly
        if random.randint(1, 30) == 1:
            asteroid = Asteroid()
            all_sprites.add(asteroid)
            asteroids.add(asteroid)

        # Update all sprites
        all_sprites.update()

        # Check for collisions between lasers and asteroids
        for laser in lasers:
            hits = pygame.sprite.spritecollide(laser, asteroids, True)
            for hit in hits:
                laser.kill()
                # Play hit sound
                hit_sound.play()  
                # Increment score for each asteroid hit
                score += 1  

        # Check for collisions between player and asteroids
        if pygame.sprite.spritecollide(player, asteroids, False):
            game_over = True

        # Draw everything
        screen.blit(background_img, (0, 0))  
        all_sprites.draw(screen)
        draw_text(screen, f"Score: {score}", 10, 10, 36, white)
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    if show_game_over_screen():
        start_game()

def show_start_screen():
    while True:
        screen.fill(black)
        draw_button(screen, "Start Game", screen_width / 2 - button_width / 2, screen_height / 2 - button_height / 2, button_width, button_height, button_color, button_text_color)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if screen_width / 2 - button_width / 2 <= mouse_pos[0] <= screen_width / 2 + button_width / 2:
                    if screen_height / 2 - button_height / 2 <= mouse_pos[1] <= screen_height / 2 + button_height / 2:
                        start_game()

show_start_screen()

