import json
from ObjectsGame import *
from dashboard import *

game_state = "playing"


def load_map(path):
    with open(path, 'r') as f:
        map_data = json.load(f)
    objects_data = map_data["objects_data"]
    blocks = []
    enemies = []
    fires = []
    saws = []
    spikes = []
    spike_heads = []
    checkpoints = []
    clouds = []
    for obj in objects_data:
        if obj["type"] == "block":
            for pos in obj["pos"]:
                for i in range(pos[2]):
                    block = Block(pos[0] + (64 * i), pos[1], 64, 96, 0)
                    blocks.append(block)
        elif obj["type"] == "block_small":
            for pos in obj["pos"]:
                block = Block(pos[0], pos[1], 33, 192, 16)
                blocks.append(block)
        elif obj["type"] == "enemy":
            enemy = Enemy(obj["pos"][0], obj["pos"][1], 35, 30, obj["pos"][2], obj["pos"][3])
            enemies.append(enemy)
        elif obj["type"] == "fire":
            fire = Fire(obj["pos"][0], obj["pos"][1], 16, 32)
            fire.on()
            fires.append(fire)
        elif obj["type"] == "saw":
            saw = Saw(obj["pos"][0], obj["pos"][1], 38)
            saw.on()
            saws.append(saw)
        elif obj["type"] == "spike":
            spike = Spike(obj["pos"][0], obj["pos"][1], 16)
            spikes.append(spike)
        elif obj["type"] == "spike_head":
            spike_head = SpikeHead(obj["pos"][0], obj["pos"][1], 54, 52)
            spike_heads.append(spike_head)
        elif obj["type"] == "checkpoint":
            checkpoint = Checkpoint(obj["pos"][0], obj["pos"][1], 64, 128, "Flag Idle")
            checkpoints.append(checkpoint)
        elif obj["type"] == "cloud":
            clouds.append(obj["pos"])

    return blocks, enemies, fires, saws, spikes, checkpoints, spike_heads, clouds


def load_levels():
    level_list = []
    levels = load_sprite_sheet("Menu", "Levels", 72, 64)
    for level_image in levels:
        level_img = pygame.image.load("assets/Menu/Levels/" + level_image + ".png")
        level_list.append(level_img)
    return level_list


def selectedLevel(window, level_flag):
    global custom_font, normal_color, hover_color
    levels = load_levels()

    while level_flag:
        back = custom_font.render("Back", True, normal_color)
        mouse_pos = pygame.mouse.get_pos()
        if 50 <= mouse_pos[0] <= 50 + back.get_width() and 50 <= mouse_pos[1] <= 50 + back.get_height():
            back = custom_font.render("Back", True, hover_color)
        window.blit(background, (0, 0))
        window.blit(back, (50, 50))
        x = 200
        for level_image in levels:
            window.blit(level_image, (x, 100))
            x += level_image.get_width() + 30
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if  50 <= mouse_x <= 50 + back.get_width() and 50 <= mouse_y <= 50 + back.get_height():
                    main()
                x = 200
                for i, level_image in enumerate(levels):
                    if x <= mouse_x <= x + level_image.get_width() and 100 <= mouse_y <= 100 + level_image.get_height():
                        main_game(window, i)
                        break
                    x += level_image.get_width() + 20


def gameOver(window, level):
    global game_state, custom_font, normal_color, hover_color
    menu = custom_font.render("Menu", True, normal_color)
    again = custom_font.render("Again", True, normal_color)
    show = custom_font.render("Game Over!", True, (0, 0, 0))

    while game_state == "lost":
        mouse_pos = pygame.mouse.get_pos()
        if 450 <= mouse_pos[0] <= 450 + menu.get_width() and 320 <= mouse_pos[1] <= 320 + menu.get_height():
            menu = custom_font.render("Menu", True, hover_color)
        else:
            menu = custom_font.render("Menu", True, normal_color)

        if 450 <= mouse_pos[0] <= 450 + again.get_width() and 250 <= mouse_pos[1] <= 250 + again.get_height():
            again = custom_font.render("Again ", True, hover_color)
        else:
            again = custom_font.render("Again", True, normal_color)

        window.blit(show, (WIDTH / 2 - 128, 150))
        window.blit(again, (450, 250))
        window.blit(menu, (450, 320))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 450 <= mouse_pos[0] <= 450 + menu.get_width() and 320 <= mouse_pos[1] <= 320 + menu.get_height():
                    game_state = "playing"
                    main()
                if 450 <= mouse_pos[0] <= 450 + again.get_width() and 250 <= mouse_pos[1] <= 250 + again.get_height():
                    game_state = "playing"
                    main_game(window, level)
        pygame.time.Clock().tick(30)


def win(window, level):
    global game_state, custom_font, normal_color, hover_color
    win_bg = custom_font.render("You Win!", True, (0, 0, 0))
    menu = custom_font.render("Menu", True, normal_color)
    continue_game = custom_font.render("Next Level", True, normal_color)
    end = End(400 + win_bg.get_width(), 100, 64, 64, "Pressed")

    while game_state == "win":
        mouse_pos = pygame.mouse.get_pos()
        if 430 <= mouse_pos[0] <= 430 + menu.get_width() and 300 <= mouse_pos[1] <= 300 + menu.get_height():
            menu = custom_font.render("Menu", True, hover_color)
        else:
            menu = custom_font.render("Menu", True, normal_color)
        if 380 <= mouse_pos[0] <= 380 + continue_game.get_width() and 250 <= mouse_pos[
            1] <= 250 + continue_game.get_height():
            continue_game = custom_font.render("Next Level ", True, hover_color)
        else:
            continue_game = custom_font.render("Next Level", True, normal_color)

        window.blit(win_bg, (400, 150))
        end.draw(window)
        window.blit(continue_game, (380, 250))
        window.blit(menu, (430, 300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 420 <= mouse_pos[0] <= 420 + menu.get_width() and 300 <= mouse_pos[1] <= 300 + menu.get_height():
                    game_state = "playing"
                    main()
                if 400 <= mouse_pos[0] <= 400 + continue_game.get_width() and 250 <= mouse_pos[
                    1] <= 250 + continue_game.get_height():
                    game_state = "playing"
                    main_game(window, level + 1)
        pygame.time.Clock().tick(30)


def main_game(window, level):
    global game_state, bg_sound
    clock = pygame.time.Clock()
    background, bg_img = get_background("Blue.png")
    hearts, hearts_img = draw_heart()

    offset_x = 0
    scroll_area_width = 200

    player = Player(100, 100, 50, 50)

    path = "assets/map" + str(level + 1) + ".json"

    # Tải map từ file JSON
    blocks, enemies, fires, saws, spikes, checkpoints, spike_heads, clouds = load_map(path)

    # Thêm các đối tượng đã tải vào danh sách objects
    objects = blocks + fires + saws + spikes + spike_heads
    bg_sound.stop()

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.jump_count < 2:
                    player.jump()
        if game_state == "playing":
            player.loop(FPS)
            for fire in fires:
                fire.loop()
            for saw in saws:
                saw.loop()
            for checkpoint in checkpoints:
                checkpoint.loop()
            for spike_head in spike_heads:
                spike_head.loop()
            handle_move(player, objects, enemies)
            draw_bg(window, background, bg_img, player, objects, offset_x, checkpoints, hearts, hearts_img,
                    enemies, clouds)  # Truyền None cho đối tượng enemy
            if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or \
                    ((player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                offset_x += player.x_vel
            if len(hearts) == 0 or player.rect.y >= 720:
                game_state = "lost"
                gameOver(window, level)
                pygame.display.update()
            if checkpoints:
                if player.rect.x >= checkpoints[0].rect.x:
                    for floor_sprite in blocks:
                        if player.rect.colliderect(floor_sprite.rect):
                            game_state = "win"
                            win(window, level)
                            pygame.display.update()

    pygame.quit()
    quit()


def main():
    global mouse_pos
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 450 <= mouse_pos[0] <= 550 and 200 <= mouse_pos[1] <= 250:
                    main_game(screen, 0)
                elif 410 <= mouse_pos[0] <= 560 and 270 <= mouse_pos[1] <= 320:
                    draw_setting_screen()
                elif 450 <= mouse_pos[0] <= 530 and 340 <= mouse_pos[1] <= 390:
                    selectedLevel(screen, True)
                elif 450 <= mouse_pos[0] <= 530 and 420 <= mouse_pos[1] <= 470:
                    pygame.quit()
                    sys.exit()

        mouse_pos = pygame.mouse.get_pos()
        draw_dashboard()
        pygame.display.flip()


# Bắt đầu chương trình
if __name__ == "__main__":
    main()
