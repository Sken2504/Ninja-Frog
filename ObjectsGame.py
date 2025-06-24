from os import listdir
from os.path import isfile, join
from dashboard import *

FPS = 60
PLAYER_VEL = 10

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheet(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def load_block(size, x, y):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(x, y, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


# Player
class Player(pygame.sprite.Sprite):
    GRAVITY = 1.5
    SPRITES = load_sprite_sheet("MainCharacters", "NinjaFrog", 32, 32, True)
    jump_sound = pygame.mixer.Sound("assets/sfx/jump.wav")
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = 'left'
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0
        self.jump_sound.play()

    def make_hit(self):
        self.hit = True
        self.hit_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != 'left':
            self.direction = 'left'
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != 'right':
            self.direction = 'right'
            self.animation_count = 0

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, window, offset_x):
        window.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, window, offset_x):
        window.blit(self.image, (self.rect.x - offset_x, self.rect.y))


# Block
class Block(Object):
    def __init__(self, x, y, size, picture_x, picture_y):
        super().__init__(x, y, size, size)
        block = load_block(size, picture_x, picture_y)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheet("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.update()
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


class Saw(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, size):
        super().__init__(x, y, size, size, "saw")
        self.saw = load_sprite_sheet("Traps", "Saw", size, size)
        self.image = self.saw["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.saw[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.update()
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


class Spike(Object):

    def __init__(self, x, y, size):
        super().__init__(x, y, size, size, "spike")
        self.spike = load_sprite_sheet("Traps", "Spikes", size, size)
        self.image = self.spike["Idle"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "Idle"


class SpikeHead(Object):
    ANIMATION_DELAY = 10

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "spike_head")
        self.spike_head = load_sprite_sheet("Traps", "SpikeHead", width, height)
        self.image = self.spike_head["Idle"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "Blink"

    def loop(self):
        sprites = self.spike_head[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.update()
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


class End(pygame.sprite.Sprite):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height, name="Idle"):
        super().__init__()
        self.end = load_sprite_sheet("Items", "End", width, height)
        if name != "Idle":
            self.animation_name = "End " + "(" + name + ")" + " (64x64)"
        else:
            self.animation_name = "End " + "(" + name + ")"
        self.images = self.end[self.animation_name][0]
        self.image = self.images.copy()
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Checkpoint:
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height, name="No Flag"):
        self.checkpoints = load_sprite_sheet("Items", "Checkpoints", width, height)
        self.animation_count = 0
        if name != "No Flag":
            self.animation_name = "Checkpoint " + "(" + name + ")" + "(64x64)"
        else:
            self.animation_name = "Checkpoint " + "(" + name + ")"
        self.images = self.checkpoints[self.animation_name][0]
        self.image = self.images.copy()
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, window, offset_x):
        window.blit(self.image, (self.rect.x - offset_x, self.rect.y))

    def loop(self):
        checkpoints = self.checkpoints[self.animation_name]
        checkpoints_index = (self.animation_count //
                             self.ANIMATION_DELAY) % len(checkpoints)
        self.image = checkpoints[checkpoints_index]
        self.animation_count += 1
        if self.animation_count // self.ANIMATION_DELAY > len(checkpoints):
            self.animation_count = 0


# Enemy
class Enemy(pygame.sprite.Sprite):
    SPRITES = load_sprite_sheet("MainCharacters", "PinkMan", 32, 32, True)
    ANIMATION_DELAY = 8

    def __init__(self, x, y, width, height, limit_left, limit_right):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height))
        self.limit_left = limit_left
        self.limit_right = limit_right

        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 4
        self.direction = 'right'
        self.animation_count = 0

    def update(self):
        if self.rect.x <= self.limit_left:
            self.direction = 'right'
        elif self.rect.x >= self.limit_right:
            self.direction = 'left'

        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

    def update_sprite(self, player):
        sprite_sheet = "idle"
        if player.x_vel != 0:
            sprite_sheet = "run"
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)

        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def draw(self, window, offset_x, player):
        self.update_sprite(player)
        window.blit(self.image, (self.rect.x - offset_x, self.rect.y))


# Background
def get_background(name):
    img = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = img.get_rect()
    titles = []
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            titles.append(pos)
    return titles, img


def draw_heart():
    path = join("assets", "Items", "heart.png")
    img = pygame.image.load(path)
    titles = []
    for i in range(5):
        pos = (i * 20 + 10, 10)
        titles.append(pos)
    return titles, img


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collide_objects = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collide_objects = obj
            break
    player.move(-dx, 0)
    player.update()
    return collide_objects


collision_cooldown = 2 * FPS
collision_cooldown_remaining = 0


def handle_move(player, objects, enemies):
    global collision_count
    global collision_cooldown_remaining

    collision_cooldown_remaining = max(0, collision_cooldown_remaining - 1)

    keys = pygame.key.get_pressed()
    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)
    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)
    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)

    if collision_cooldown_remaining <= 0:
        to_check = [collide_left, collide_right, *vertical_collide]
        for obj in to_check:
            if obj and (obj.name == "fire" or obj.name == "saw" or obj.name == "spike"):
                player.make_hit()
                collision_count += 1
                collision_cooldown_remaining = collision_cooldown
                break

        for enemy in enemies:
            if pygame.sprite.collide_mask(player, enemy):
                player.make_hit()
                collision_count += 1
                collision_cooldown_remaining = collision_cooldown
                break

    collision_cooldown_remaining = max(0, collision_cooldown_remaining - 1)


def handle_vertical_collision(player, objects, dy):
    collied_objects = []
    for o in objects:
        if pygame.sprite.collide_mask(player, o):
            if dy > 0:
                player.rect.bottom = o.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = o.rect.bottom
                player.hit_head()
            collied_objects.append(o)
    return collied_objects


deleted = False
collision_count = 0


def draw_bg(window, background, bg_img, player, objects, offset_x, checkpoints, hearts, hearts_img, enemies, clouds):
    global collision_count
    cloud_img = pygame.image.load("assets/clouds/clouds.png")
    for i in background:
        window.blit(bg_img, i)
    if clouds:
        for cloud in clouds:
            screen.blit(cloud_img, (cloud[0], cloud[1]))
    if objects:
        for o in objects:
            o.draw(window, offset_x)
    player.draw(window, offset_x)
    if enemies:
        for enemy in enemies:
            enemy.draw(window, offset_x, player)
    if checkpoints:
        for checkpoint in checkpoints:
            checkpoint.draw(window, offset_x)
    for i in hearts:
        window.blit(hearts_img, i)
    if collision_count == 1:
        if len(hearts) > 0:
            hearts.pop()
            collision_count = 0

    pygame.display.update()
