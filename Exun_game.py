import pygame
import random
import sys
import math
from pygame import mixer


pygame.init()
mixer.init()

clock = pygame.time.Clock()
screenw = 1300
screenh = 650
screen = pygame.display.set_mode((screenw, screenh))
pygame.display.set_caption('Games')

mixer.music.load('bgmusic.mp3')
mixer.music.set_volume(10)
mixer.music.play()
music_button = pygame.Rect(1175, 38, 90, 90)
music = True

start_button = pygame.Rect(531, 368, 237, 96)
finish = [[1240, 540], [1240, 600], [1240, 600], [1240, 600], [1240, 600]]
level = 0
score_font = pygame.font.Font(None, 20)
start_img = pygame.image.load("start.png")
finish_img = pygame.image.load("finish.png")
start_img = pygame.transform.scale(start_img,(screenw, screenh)) 
finish_img = pygame.transform.scale(finish_img,(screenw, screenh)) 

backgrounds = [[pygame.image.load("bg1.png")],
                [pygame.image.load("bg1.png")],
                [pygame.image.load("bg1.png")],
                [pygame.image.load("bg1.png")],
                [pygame.image.load("bg1.png")],]

for i in range(5):
    backgrounds[i][0] = pygame.transform.scale(backgrounds[i][0],(screenw, screenh))   

obstacles_levels = [[[pygame.Rect(1050, 500, 140, 60), (100, 56, 25)],
                    [pygame.Rect(130, 470, 140, 60), (100, 56, 25)],
                    [pygame.Rect(350, 380, 140, 160), (100, 56, 25)],
                    [pygame.Rect(620, 340, 140, 60), (100, 56, 25)],
                    [pygame.Rect(0, screenh-90, screenw, 20), (33, 197, 67)]],
                    [pygame.Rect(0, screenh-20, screenw, 20)],
                    [pygame.Rect(0, screenh-20, screenw, 20)],
                    [pygame.Rect(0, screenh-20, screenw, 20)],
                    [pygame.Rect(0, screenh-20, screenw, 20)]]
acid_lakes_levels = [[[pygame.Rect(540, 530, 330, 30), (255, 0, 0)]],
                    [],
                    [],
                    [],
                    []]

move_platforms_levels = [[[pygame.Rect(780, 450, 100, 10), 900, 780]],
                        [],
                        [],
                        [],
                        []]
return1 = False

temp_platforms_levels = [[],
                        [],
                        [],
                        [],
                        []]

spritesp1 = [pygame.image.load("sprite1.png"),
            pygame.image.load("sprite2.png")]

startx, starty = 0, 0
rightp1 = False
leftp1 = False
jumpp1 = False
p1x = startx
p1y = starty
p1i = 0
p1temp = 0
p1speed = 5
jumpcp1 = 0
onsurfacep1 = False
countp1 = 0
pointsp1 = 0

spritesp2 = [pygame.image.load("sprite1.png"),
            pygame.image.load("sprite2.png")]
rightp2 = False
leftp2 = False
jumpp2 = False
p2x = startx
p2y = starty
p2i = 0
p2temp = 0
p2speed = 5
jumpcp2 = 0
onsurfacep2 = False
countp2 = 0
pointsp2 = 0

score_text = score_font.render(f'{pointsp1} - {pointsp2}', True, (255, 255, 255))
textRect = score_text.get_rect()
textRect.center = (screenw//2, 50)

finish_screen = False
run = True
start = False
while run:
    screen.fill((0, 0, 0))
    if start:
        screen.blit(backgrounds[level][0], (0,0))
        score_text = score_font.render(f'{pointsp1} - {pointsp2}', True, (255, 255, 255))
        screen.blit(score_text, textRect)
        if level > 4:
            start = False
            finish_screen = True
            continue

        obstaces = obstacles_levels[level]
        acid_lakes = acid_lakes_levels[level]
        move_platforms = move_platforms_levels[level]
        temp_platforms = temp_platforms_levels[level]

        if (p1temp > 0) and (p1temp <= 10):
            p1i = 0
        elif (p1temp > 10) and (p1temp <= 20):
            p1i = 1
        elif p1temp > 20:
            p1temp = 0
        imagep1 = spritesp1[p1i]
        screen.blit(imagep1, (p1x, p1y))

        if (p2temp > 0) and (p2temp <= 10):
            p2i = 0
        elif (p2temp > 10) and (p2temp <= 20):
            p2i = 1
        elif p2temp > 20:
            p2temp = 0
        imagep2 = spritesp2[p2i]
        screen.blit(imagep2, (p2x, p2y))

        sizep1 = imagep1.get_size()
        sizep2 = imagep2.get_size()

        for i in obstaces:
            pygame.draw.rect(screen, i[1], i[0])
            if p1x == i[0].right and (p1y >= i[0].top-sizep1[1]) and (p1y <= i[0].bottom):
                rightp1 = False
                p1x = i[0].right+5

            if p1x == i[0].left-sizep1[0] and (p1y >= i[0].top-sizep1[1]) and (p1y <= i[0].bottom):
                leftp1 = False
                p1x = i[0].left-sizep1[0]-5

            if p2x == i[0].right and (p2y >= i[0].top-sizep2[1]) and (p2y <= i[0].bottom):
                rightp2 = False
                p2x = i[0].right+5

            if p2x == i[0].left-sizep2[0] and (p2y >= i[0].top-sizep2[1]) and (p2y <= i[0].bottom):
                leftp2 = False
                p2x = i[0].left-sizep2[0]-5

            if p1y == i[0].bottom and (p1x > i[0].left-sizep1[0]) and (p1x < i[0].right):
                p1y = i[0].bottom
                jumpp1 = False
            if p2y == i[0].bottom and (p2x > i[0].left-sizep2[0]) and (p2x < i[0].right):
                p2y = i[0].bottom
                jumpp2 = False

            if p1y+sizep1[1] == i[0].top and (p1x > i[0].left-sizep1[0]) and (p1x < i[0].right):
                onsurfacep1 = True
                jumpp1 = False
            if p2y+sizep2[1] == i[0].top and (p2x > i[0].left-sizep2[0]) and (p2x < i[0].right):
                onsurfacep2 = True
                jumpp2 = False

        for f in acid_lakes:
            pygame.draw.rect(screen, f[1], f[0])
            if (p1x >= f[0].left) and (p1x <= f[0].right) and (p1y >= f[0].top) and (p1y <= f[0].bottom):
                p1x = startx
                p1y = starty
                print("done")
            if (p2x >= f[0].left) and (p2x <= f[0].right) and (p2y >= f[0].top) and (p2y <= f[0].bottom):
                p2x = startx
                p2y = starty
                print("done")

        for a in move_platforms:
            pygame.draw.rect(screen, (255, 255, 255), a[0])
            if return1:
                if a[0].x > a[2]:
                    a[0].x -= 1
                else:
                    return1 = False
            elif a[0].x < a[1]:
                a[0].x += 1
            elif a[0].x >= a[1]:
                return1 = True

            if p1y == a[0].bottom and (p1x > a[0].left-sizep1[0]) and (p1x < a[0].right):
                p1y = a[0].bottom
                jumpp1 = False
            if p2y == a[0].bottom and (p2x > a[0].left-sizep2[0]) and (p2x < a[0].right):
                p2y = a[0].bottom
                jumpp2 = False

            if p1y+sizep1[1] == a[0].top and (p1x > a[0].left-sizep1[0]) and (p1x < a[0].right):
                onsurfacep1 = True
                jumpp1 = False
            if p2y+sizep2[1] == a[0].top and (p2x > a[0].left-sizep2[0]) and (p2x < a[0].right):
                onsurfacep2 = True
                jumpp2 = False

        for b in temp_platforms:
            pygame.draw.rect(screen, (255, 255, 255), b)
            if p1y == b.bottom and (p1x > b.left-sizep1[0]) and (p1x < b.right):
                p1y = b.bottom
            if p2y == b.bottom and (p2x > b.left-sizep2[0]) and (p2x < b.right):
                p2y = b.bottom

            if p1y+sizep1[1] == b.top and (p1x > b.left-sizep1[0]) and (p1x < b.right):
                onsurfacep1 = True
                jumpp1 = False
                countp1 += 1
                if countp1 > 100:
                    countp1 = 0
                    onsurfacep1 = False
                    p1y += 10
            if p2y+sizep2[1] == b.top and (p2x > b.left-sizep2[0]) and (p2x < b.right):
                onsurfacep2 = True
                jumpp2 = False
                countp2 += 1
                if countp2 > 100:
                    countp2 = 0
                    onsurfacep2 = False
                    print("done")


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    rightp1 = True
                if event.key == pygame.K_a:
                    leftp1 = True
                if event.key == pygame.K_RIGHT:
                    rightp2 = True
                if event.key == pygame.K_LEFT:
                    leftp2 = True
                if event.key == pygame.K_w:
                    if jumpp1:
                        pass
                    else:
                        jumpp1 = True
                        jumpcp1 = 0
                if event.key == pygame.K_UP:
                    if jumpp2:
                        pass
                    else:
                        jumpp2 = True
                        jumpcp2 = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    rightp1 = False
                if event.key == pygame.K_a:
                    leftp1 = False
                if event.key == pygame.K_RIGHT:
                    rightp2 = False
                if event.key == pygame.K_LEFT:
                    leftp2 = False
        
        if rightp1:
            p1x += p1speed
        if leftp1:
            p1x -= p1speed
        
        if rightp2:
            p2x += p2speed
        if leftp2:
            p2x -= p2speed

        if onsurfacep1:
            if jumpp1:
                if jumpcp1 < 10:
                    p1y -= 10
                    if p1y < 0:
                        p1y = 0
                elif (jumpcp1 > 16) and (jumpcp1 < 27):
                    p1y += 10
                    if p1y > screenh-sizep1[1]-5:
                        p1y = screenh-sizep1[1]-5
                elif jumpcp1 > 19:
                    jumpp1 = False
        else:
            p1y += 10
            if p1y > screenh-sizep1[1]-20:
                p1y = screenh-sizep1[1]-20
        if onsurfacep2:
            if jumpp2:
                if jumpcp2 < 10:
                    p2y -= 10
                    if p2y < 0:
                        p2y = 0
                elif (jumpcp2 > 16) and (jumpcp2 < 27):
                    p2y += 10
                    if p2y > screenh-sizep2[1]-5:
                        p2y = screenh-sizep2[1]-5
                elif jumpcp2 > 19:
                        jumpp2 = False
        else:
            p2y += 10
            if p2y > screenh-sizep2[1]-20:
                p2y = screenh-sizep2[1]-20

        if p1x > screenw-sizep1[0]-5:
            p1x = screenw-sizep1[0]-5
        elif p1x < 0:
            p1x = 0

        if p2x > screenw-sizep2[0]-5:
            p2x = screenw-sizep2[0]-5
        elif p2x < 0:
            p2x = 0

        p1temp += 0.5
        p2temp += 0.5
        jumpcp1 += 1
        jumpcp2 += 1
        if not jumpp1:
            onsurfacep1 = False
        if not jumpp2:
            onsurfacep2 = False
        
        if p1x >= finish[level][0]:
            pointsp1 += 1
            level += 1
            rightp1 = False
            leftp1 = False
            jumpp1 = False
            p1x = startx
            p1y = starty
            p1i = 0
            p1temp = 0
            p1speed = 5
            jumpcp1 = 0
            onsurfacep1 = False
            countp1 = 0
            rightp2 = False
            leftp2 = False
            jumpp2 = False
            p2x = startx
            p2y = starty
            p2i = 0
            p2temp = 0
            p2speed = 5
            jumpcp2 = 0
            onsurfacep2 = False
            countp2 = 0
        elif p2x >= finish[level][0]:
            pointsp2 += 1
            level += 1
            rightp1 = False
            leftp1 = False
            jumpp1 = False
            p1x = startx
            p1y = starty
            p1i = 0
            p1temp = 0
            p1speed = 5
            jumpcp1 = 0
            onsurfacep1 = False
            countp1 = 0
            rightp2 = False
            leftp2 = False
            jumpp2 = False
            p2x = startx
            p2y = starty
            p2i = 0
            p2temp = 0
            p2speed = 5
            jumpcp2 = 0
            onsurfacep2 = False
            countp2 = 0


    elif finish_screen:
        screen.fill((255, 255, 255))
        screen.blit(finish_img, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()


    else:
        pygame.draw.rect(screen, (255, 255, 255), start_button)
        pygame.draw.rect(screen, (255, 255, 255), music_button)
        screen.blit(start_img, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    start = True
                if music_button.collidepoint(event.pos):
                    if music:
                        mixer.music.pause()
                        music = False
                    else:
                        mixer.music.unpause()
                        music = True


    pygame.display.update()
    clock.tick(60)