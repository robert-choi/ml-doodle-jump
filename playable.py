###################################
#   Created by Robert Choi 2020   #
#  https://github.com/robert-choi #
###################################

import pygame
from os import path
from random import randint
from config import *
from jumper import *
from platforms import *

def generate_plats(platforms, sprites):
    last_y = platforms[-1].rect.y
    plat_y = last_y-50
    last_id = platforms[-1].id + 1
    while True:
        plat_created = False
        if randint(0,70)==1:    # 1/70 chance of generating plat every pixel
            if randint(1,7) == 7:   # Lucky 7 of bouncy platform appearing:
                new_plat = Bouncy_platform(randint(1, 265), plat_y, last_id)
            else:
                new_plat = Platform(randint(1,265), plat_y, last_id)     
            plat_created = True    
        elif plat_y < last_y-150:   # To ensure the game is possible
            new_plat = Platform(randint(1,265), plat_y, last_id)
            plat_created = True
        if plat_created:
            platforms.append(new_plat)
            sprites.add(new_plat)
            last_y = plat_y
            plat_y -= 50
            last_id +=1
        plat_y -= 1
        if plat_y < -1000:
            break

def update_display(sprites, score):
    win.fill(white)
    sprites.draw(win)
    win.blit(font.render(f'Top Score: {int(score)//10}', True, black), (200, 10))
    pygame.display.update()

pygame.init()
win = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Doodle Jump")
font = pygame.font.Font('freesansbold.ttf', 16)

def main():

    doodlers = [Jumper(randint(1,265), 600)]
    all_sprites = pygame.sprite.LayeredUpdates()
    platforms = [Platform(randint(1,265), 600, 0)]
    for doodle in doodlers:
        all_sprites.add(doodle)
    generate_plats(platforms, all_sprites)
    top_scorrer = doodlers[0]

    clock = pygame.time.Clock()
    score = 0
    running = True

    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        all_sprites.update()

        if len(doodlers) < 1:   # Check if doodlers exist
            running = False
            break

        for plat in platforms:  # Platform creation and deletion
            if not plat.alive:
                platforms.remove(plat)
                plat.kill()
        if len(platforms) < 10:
            generate_plats(platforms, all_sprites)

        if top_scorrer.max_height:  # Scroll all objects down
            for plat in platforms:
                plat.rect.y -= top_scorrer.y_vel
            for doodle in doodlers:
                if not doodle == top_scorrer:
                    doodle.rect.y -= top_scorrer.y_vel

        for doodle in doodlers:     # Doodle behaviour for bounce and score
            doodle.handle_keys()
            for plat in platforms:
                doodle.check_coll_bounce(plat)
            if doodle.score > score:
                score = doodle.score
                top_scorrer = doodle

        update_display(all_sprites, score)


if __name__ == '__main__':
    main()