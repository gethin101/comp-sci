import pygame
import random
import math
import sys
import os

pygame.init()

# ----- Resource path for PyInstaller -----
def resource_path(relative_path):
    """ Get absolute path for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ----- Fullscreen Window -----
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = win.get_size()
pygame.display.set_caption("Granny Game")

# ----- Colors -----
WHITE = (255, 255, 255)
RED = (200, 50, 50)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
BLUE = (50, 100, 255)

# ----- Player -----
player_size = 80
base_speed = 5
player_speed = base_speed
player_pos = [WIDTH // 2, HEIGHT // 2]

# Zoomies settings
boost_multiplier = 2.0
boost_duration = 2.0
boost_cooldown = 4.0
boost_timer = 0.0
cooldown_timer = boost_cooldown
boost_active = False
trail_positions = []

# ----- Granny -----
granny_size = 100
granny_speed = 2.0
granny_max_speed = base_speed
granny_acceleration = 0.002

def spawn_granny():
    while True:
        x = random.randint(0, WIDTH - granny_size)
        y = random.randint(0, HEIGHT - granny_size)
        if math.hypot(x - player_pos[0], y - player_pos[1]) > 200:
            return [x, y]

granny_pos = spawn_granny()

# ----- Keys -----
key_size = 50
keys_needed = 4
keys_collected = 0
key_positions = [[random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)] for _ in range(keys_needed)]

# ----- Door -----
door_width, door_height = 150, 40
door_pos = [WIDTH // 2 - door_width // 2, 0]

# ----- Health -----
player_health = 100

# ----- Fireballs -----
fireballs = []
fireball_speed = 6
fireball_size = 32
fireball_cooldown = 1.5
last_fireball_time = 0

# ----- Counters -----
death_count = 0
escape_count = 0

# ----- Timer -----
escape_timer = 25.0
timer_font = pygame.font.SysFont("Arial", 60, bold=True)

# ----- Load Images -----
BACKGROUND_IMAGE = resource_path(os.path.join("assets", "background.png"))
GRANNY_IMAGE = resource_path(os.path.join("assets", "granny.png"))
KEY_IMAGE = resource_path(os.path.join("assets", "key.png"))
DENTURES_IMAGE = resource_path(os.path.join("assets", "dentures.png"))
DOOR_IMAGE = resource_path(os.path.join("assets", "door.png"))
FIREBALL_IMAGE = resource_path(os.path.join("assets", "fireball.png"))

try:
    background_img = pygame.image.load(BACKGROUND_IMAGE).convert()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    granny_img = pygame.image.load(GRANNY_IMAGE).convert_alpha()
    key_img = pygame.image.load(KEY_IMAGE).convert_alpha()
    dentures_img = pygame.image.load(DENTURES_IMAGE).convert_alpha()
    door_img = pygame.image.load(DOOR_IMAGE).convert_alpha()
    fireball_img = pygame.image.load(FIREBALL_IMAGE).convert_alpha()
except pygame.error as e:
    print(f"Image load error: {e}")
    sys.exit()

# Scale images
granny_img = pygame.transform.scale(granny_img, (granny_size, granny_size))
key_img = pygame.transform.scale(key_img, (key_size, key_size))
dentures_img = pygame.transform.scale(dentures_img, (player_size, player_size))
door_img = pygame.transform.scale(door_img, (door_width, door_height))
fireball_img = pygame.transform.scale(fireball_img, (fireball_size, fireball_size))

# Fonts
font = pygame.font.SysFont("Arial", 32)
big_font = pygame.font.SysFont("Arial", 48)

clock = pygame.time.Clock()
running = True
game_over = False
escaped = False

# ----- Fireball Class -----
class Fireball:
    def __init__(self, x, y):
        self.pos = [x, y]
        dx = player_pos[0] - x
        dy = player_pos[1] - y
        dist = math.hypot(dx, dy)
        self.vel = [(dx / dist) * fireball_speed, (dy / dist) * fireball_speed]
        self.bounce_count = 0

    def update(self):
        dx = player_pos[0] - self.pos[0]
        dy = player_pos[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.vel[0] += (dx / dist) * 0.05
            self.vel[1] += (dy / dist) * 0.05

        speed = math.hypot(self.vel[0], self.vel[1])
        if speed > 0:
            self.vel[0] = (self.vel[0] / speed) * fireball_speed
            self.vel[1] = (self.vel[1] / speed) * fireball_speed

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        if self.pos[0] <= 0 or self.pos[0] >= WIDTH - fireball_size:
            if self.bounce_count == 0:
                self.vel[0] *= -1
                self.bounce_count += 1
            else:
                return False
        if self.pos[1] <= 0 or self.pos[1] >= HEIGHT - fireball_size:
            if self.bounce_count == 0:
                self.vel[1] *= -1
                self.bounce_count += 1
            else:
                return False
        return True

    def draw(self):
        win.blit(fireball_img, self.pos)

# ----- Game Functions -----
def move_granny_towards_player():
    dx = player_pos[0] - granny_pos[0]
    dy = player_pos[1] - granny_pos[1]
    dist = math.hypot(dx, dy)
    if dist > 0:
        granny_pos[0] += (dx / dist) * granny_speed
        granny_pos[1] += (dy / dist) * granny_speed

def check_collision(rect1, rect2):
    return pygame.Rect(*rect1).colliderect(pygame.Rect(*rect2))

def reset_game():
    global player_pos, granny_pos, key_positions, keys_collected, granny_speed, player_health
    global fireballs, boost_timer, cooldown_timer, boost_active, game_over, escaped, escape_timer, trail_positions
    player_pos = [WIDTH // 2, HEIGHT // 2]
    granny_pos = spawn_granny()
    key_positions = [[random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)] for _ in range(keys_needed)]
    keys_collected = 0
    granny_speed = 2.0
    player_health = 100
    fireballs = []
    boost_timer = 0.0
    cooldown_timer = boost_cooldown
    boost_active = False
    game_over = False
    escaped = False
    escape_timer = 25.0
    trail_positions = []

# ----- Drawing -----
def draw_scene():
    win.blit(background_img, (0, 0))
    win.blit(door_img, door_pos)
    win.blit(font.render("DOOR", True, WHITE), (door_pos[0] + door_width // 2 - 30, door_pos[1] + 5))
    for pos in key_positions:
        win.blit(key_img, pos)

    # Blue trail
    if boost_active:
        for i, tpos in enumerate(trail_positions[-15:]):
            alpha = int(255 * (i+1)/15)
            size = player_size // 2
            s = pygame.Surface((size, size), pygame.SRCALPHA)
            s.fill((50, 100, 255, alpha))
            win.blit(s, (tpos[0] + player_size//4, tpos[1] + player_size//4))

    win.blit(dentures_img, player_pos)
    win.blit(granny_img, granny_pos)
    win.blit(font.render(f"Keys: {keys_collected}/{keys_needed}", True, WHITE), (10, 10))
    pygame.draw.rect(win, RED, (10, 50, 200, 20))
    pygame.draw.rect(win, GREEN, (10, 50, 200 * (player_health / 100), 20))
    for fb in fireballs:
        fb.draw()
    zoom_text = font.render("Zoomies", True, WHITE)
    win.blit(zoom_text, (WIDTH - 220, 10))
    pygame.draw.rect(win, RED, (WIDTH - 220, 50, 200, 20), 2)
    fill_ratio = max(0, (boost_duration - boost_timer) / boost_duration) if boost_active else max(0, cooldown_timer / boost_cooldown)
    pygame.draw.rect(win, RED, (WIDTH - 220, 50, 200 * fill_ratio, 20))
    win.blit(font.render(f"Deaths: {death_count}", True, WHITE), (10, HEIGHT - 40))
    escape_text = font.render(f"Escapes: {escape_count}", True, WHITE)
    win.blit(escape_text, (WIDTH - escape_text.get_width() - 10, HEIGHT - 40))
    color = RED if escape_timer <= 5 else WHITE
    timer_text = timer_font.render(f"{int(escape_timer)}", True, color)
    win.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, HEIGHT - 70))
    pygame.display.flip()

# ----- Main Loop -----
while True:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    if not game_over and not escaped:
        keys = pygame.key.get_pressed()
        escape_timer -= dt
        if escape_timer <= 0:
            game_over = True
            death_count += 1

        # Player movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_pos[0] += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_pos[1] += player_speed

        # Trail
        if boost_active:
            trail_positions.append(player_pos.copy())
        if len(trail_positions) > 30:
            trail_positions = trail_positions[-30:]

        # Zoomies
        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and cooldown_timer >= boost_cooldown:
            boost_active = True
            boost_timer = 0.0
            cooldown_timer = 0.0

        if boost_active:
            player_speed = base_speed * boost_multiplier
            boost_timer += dt
            if boost_timer >= boost_duration:
                boost_active = False
                player_speed = base_speed
        else:
            player_speed = base_speed
            if cooldown_timer < boost_cooldown:
                cooldown_timer += dt

        player_pos[0] = max(0, min(WIDTH - player_size, player_pos[0]))
        player_pos[1] = max(0, min(HEIGHT - player_size, player_pos[1]))

        move_granny_towards_player()
        if granny_speed < granny_max_speed:
            granny_speed += granny_acceleration

        # Fireballs
        if keys_collected >= 2:
            if pygame.time.get_ticks() / 1000 - last_fireball_time > fireball_cooldown:
                fireballs.append(Fireball(granny_pos[0], granny_pos[1]))
                last_fireball_time = pygame.time.get_ticks() / 1000

        new_fireballs = []
        for fb in fireballs:
            if fb.update():
                if check_collision((player_pos[0], player_pos[1], player_size, player_size),
                                   (fb.pos[0], fb.pos[1], fireball_size, fireball_size)):
                    player_health -= 25
                    if player_health <= 0:
                        game_over = True
                        death_count += 1
                    continue
                new_fireballs.append(fb)
        fireballs = new_fireballs

        # Keys
        for pos in key_positions[:]:
            if check_collision((player_pos[0], player_pos[1], player_size, player_size),
                               (pos[0], pos[1], key_size, key_size)):
                key_positions.remove(pos)
                keys_collected += 1

        # Granny collision
        if check_collision((player_pos[0], player_pos[1], player_size, player_size),
                           (granny_pos[0], granny_pos[1], granny_size, granny_size)):
            game_over = True
            death_count += 1

        # Escape
        if keys_collected == keys_needed and check_collision(
            (player_pos[0], player_pos[1], player_size, player_size),
            (door_pos[0], door_pos[1], door_width, door_height)):
            escaped = True
            escape_count += 1

        draw_scene()

    elif game_over:
        win.blit(background_img, (0, 0))
        main_text = big_font.render("You died! Press R to restart or ENTER to quit", True, RED)
        main_box = pygame.Rect(0, 0, main_text.get_width() + 40, main_text.get_height() + 20)
        main_box.center = (WIDTH // 2, HEIGHT // 2 - 80)
        pygame.draw.rect(win, BLACK, main_box)
        win.blit(main_text, (main_box.centerx - main_text.get_width() // 2, main_box.centery - main_text.get_height() // 2))
        if death_count == 5:
            bad_font = pygame.font.SysFont("Arial", 100, bold=True)
            bad_text = bad_font.render("You're so bad", True, RED)
            bad_box = pygame.Rect(0, 0, bad_text.get_width() + 60, bad_text.get_height() + 30)
            bad_box.center = (WIDTH // 2, HEIGHT // 2 + 120)
            pygame.draw.rect(win, BLACK, bad_box)
            win.blit(bad_text, (bad_box.centerx - bad_text.get_width() // 2, bad_box.centery - bad_text.get_height() // 2))
        pygame.display.flip()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_r]:
            reset_game()
        elif pressed[pygame.K_RETURN] or pressed[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    elif escaped:
        win.blit(background_img, (0, 0))
        text = big_font.render("You escaped! Press R to restart or ENTER to quit", True, GREEN)
        box_rect = pygame.Rect(0, 0, text.get_width() + 40, text.get_height() + 20)
        box_rect.center = (WIDTH // 2, HEIGHT // 2 - 50)
        pygame.draw.rect(win, BLACK, box_rect)
        win.blit(text, (box_rect.centerx - text.get_width() // 2, box_rect.centery - text.get_height() // 2))
        pygame.display.flip()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_r]:
            reset_game()
        elif pressed[pygame.K_RETURN] or pressed[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
