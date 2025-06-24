import pygame
import sys

pygame.init()

WIDTH = 1003
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("NinjaFrog Dashboard")

background = pygame.image.load("assets/Background/background.png").convert_alpha()

music_on = True

bg_sound = pygame.mixer.Sound("assets/sfx/music.wav")
bg_sound.play()

custom_font = pygame.font.Font("assets/Jersey10-Regular.ttf", 64)
normal_color = (255, 255, 255)
hover_color = (128, 128, 128)


def draw_dashboard():
    global custom_font, normal_color, hover_color

    game_name = pygame.image.load("assets/Items/NinjaFrog.png").convert_alpha()
    play_text = custom_font.render("Play", True, normal_color)
    setting_text = custom_font.render("Setting", True, normal_color)
    level_text = custom_font.render("Level", True, normal_color)
    quit_text = custom_font.render("Quit", True, normal_color)

    mouse_pos = pygame.mouse.get_pos()
    if 450 <= mouse_pos[0] <= 450 + play_text.get_width() and 200 <= mouse_pos[1] <= 200 + play_text.get_height():
        play_text = custom_font.render("Play", True, hover_color)
    if 410 <= mouse_pos[0] <= 410 + setting_text.get_width() and 270 <= mouse_pos[1] <= 270 + setting_text.get_height():
        setting_text = custom_font.render("Setting", True, hover_color)
    if 440 <= mouse_pos[0] <= 440 + level_text.get_width() and 340 <= mouse_pos[
        1] <= 340 + level_text.get_height():
        level_text = custom_font.render("Level", True, hover_color)
    if 450 <= mouse_pos[0] <= 450 + quit_text.get_width() and 420 <= mouse_pos[1] <= 420 + quit_text.get_height():
        quit_text = custom_font.render("Quit", True, hover_color)

    screen.blit(background, (0, 0))
    screen.blit(game_name, (250, 100))
    screen.blit(play_text, (450, 200))
    screen.blit(setting_text, (410, 270))
    screen.blit(level_text, (440, 340))
    screen.blit(quit_text, (450, 420))


def draw_setting_screen():
    global music_on, custom_font, normal_color, hover_color
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Kiểm tra nếu người dùng nhấp vào "Quay lại"
                if 40 <= mouse_pos[0] <= 190 and 10 <= mouse_pos[1] <= 50:
                    return
                # Kiểm tra nếu người dùng nhấp vào "Music"
                if 540 <= mouse_pos[0] <= 640 and 200 <= mouse_pos[1] <= 240:
                    music_on = not music_on
                    if music_on:
                        bg_sound.play()
                    else:
                        bg_sound.stop()

        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background, (0, 0))
        back_text = custom_font.render("Back", True, normal_color)
        music = custom_font.render("Music:", True, normal_color)
        on_music = custom_font.render("On", True, normal_color)
        off_music = custom_font.render("Off", True, normal_color)
        if 10 <= mouse_pos[0] <= 10 + back_text.get_width() and 10 <= mouse_pos[1] <= 10 + back_text.get_height():
            back_text = custom_font.render("Back", True, hover_color)
        if 400 <= mouse_pos[0] <= 400 + music.get_width() and 200 <= mouse_pos[
            1] <= 200 + music.get_height():
            music = custom_font.render("Music:", True, hover_color)
        if 540 <= mouse_pos[0] <= 540 + on_music.get_width() and 200 <= mouse_pos[1] <= 200 + on_music.get_height():
            on_music = custom_font.render("On", True, hover_color)
        if 540 <= mouse_pos[0] <= 540 + off_music.get_width() and 200 <= mouse_pos[1] <= 200 + off_music.get_height():
            off_music = custom_font.render("Off", True, hover_color)

        music_text = on_music if music_on else off_music
        screen.blit(back_text, (10, 10))
        screen.blit(music, (400, 200))
        screen.blit(music_text, (540, 200))

        pygame.display.flip()
