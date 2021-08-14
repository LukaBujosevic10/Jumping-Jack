import pygame
import numpy
from pygame import mixer
from pygame.locals import *
pygame.init()
window = pygame.display.set_mode((500,700))
global level
level = 1
global colors
colors = [(0,255,0),(255,255,0),(5,208,235),(255,0,127)]
def makeLevel(level):
    global player,prolazi,speeds,sirina_rupe,hole_speeds
    global jumping,fall,pressed_up,skok,count,game_over,sprat,granica,gm_count,finished
    player = pygame.Rect(250,675,20,20)
    #MAKE ARRAY OF X POSITION OF HOLES
    prolazi = numpy.random.randint(460,size=(10))
    #MAKE ARRAY OF HOLE SPEED
    speeds= []
    for i in range(1,level+1):
        speeds.append(i)
        speeds.append(i*-1)
    sirina_rupe = 70
    hole_speeds = [speeds[numpy.random.randint(len(speeds))] for i in range(9)]
    jumping = False
    pressed_up = False
    skok = True
    count = 0
    game_over = False
    fall = False
    gm_count = 0
    finished = False
#CRTANJE NA EKRANU
def drawWindow(player):
    window.fill((0,0,0))
    #DRAW PLATFORM
    for i in range(10):
        #DRAW WALL
        sprat = pygame.Rect(0,i*70+65, 500,5)
        pygame.draw.rect(window,colors[(i+level)%len(colors)],sprat);
        #DRAW HOLES
        if i != 9: #NOT TO DRAW ON FIRST FLOOR
            if hole_speeds[i] > 0: #IF IT GOES TO LEFT
                if prolazi[i]+sirina_rupe > 500: #IF PART OF THE HOLE IS OUT OF SCREEN
                    nova = pygame.Rect(0,i*70+65, (prolazi[i]+sirina_rupe)-500,5)
                    pygame.draw.rect(window,(0,0,0),nova);
                if(prolazi[i]>500): #IF WHOLE HOLE IS OUT OF SCREEN
                    prolazi[i]=0
            else: #IF IT GOES TO RIGHT
                 if prolazi[i] < 0: #IF PART OF THE HOLE IS OUT OF SCREEN
                     nova = pygame.Rect(500+prolazi[i],i*70+65, prolazi[i]*(-1),5)
                     pygame.draw.rect(window,(0,0,0),nova);
                 if(prolazi[i]+sirina_rupe<0): #IF WHOLE HOLE IS OUT OF SCREEN
                     prolazi[i]=500-sirina_rupe
            rupa = pygame.Rect(prolazi[i],i*70+65, sirina_rupe,5)
            prolazi[i]=prolazi[i]+hole_speeds[i]
            pygame.draw.rect(window,(0,0,0),rupa)
    #DRAW PLAYER
    if player.x > 500:
        player.x=0
    elif(player.x+20 > 500):
        nova = pygame.Rect(0,player.y, 20,20)
        pygame.draw.rect(window,(255,0,0),nova,3,7)
    if player.x < 0:
        nova = pygame.Rect(500+player.x,player.y, 20,20)
        pygame.draw.rect(window,(255,0,0),nova,3,7)
    if(player.x+20 <0):
        player.x = 500+player.x
    pygame.draw.rect(window,(255,0,0),player,3,7);
    #font2 = pygame.font.SysFont(None, 48)
    font = pygame.font.SysFont(None,30)
    img = font.render('Level '+str(level), True, colors[(i-1)%len(colors)])
    window.blit(img, (410, 20))
    pygame.display.update()

def main():
    global jumping,fall,pressed_up,skok,count,game_over,sprat,granica,gm_count,jump_sound,move_sound,gameover_sound,finished
    mixer.init()
    clock = pygame.time.Clock()
    run = True
    jump_sound = mixer.Sound("blimp.wav")
    move_sound = mixer.Sound("kvik.mp3")
    gameover_sound = mixer.Sound("game_over.mp3")
    finished = False
    #OKRETANJE SVAKI FRAME
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                run = False
        if(game_over == False):
            key_presed = pygame.key.get_pressed()
            pomeranje(key_presed)
            if jumping == True:
                skakanje()
            else:
                if fall == False:
                    fall = provera_podloge()

                if(fall == True):
                    pad(granica)
                else:
                    skok = True
            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                pressed_up = False
            if jumping == True:
                provera_gameovera(sprat)
            elif fall == True:
                sprat = (player.y)//70
                provera_next_levela(sprat)
                provera_gameovera(sprat)
            drawWindow(player)
        else:
            gm_count+=1
            if finished == True:
                font = pygame.font.SysFont(None,90)
                img = font.render('Level completed', True, (0,255,0))
                window.blit(img,(0,350))
                pygame.display.update()
            if gm_count == 90:
                makeLevel(level)
                gm_count = 0
                game_over = False
    pygame.quit()

def provera_gameovera(sprat):
    global game_over
    gornja_linija = sprat*70+65
    donja_linija = gornja_linija+5
    igrac_gornja = player.y
    igrac_donja = player.y+20
    leva_rupa = prolazi[sprat]
    desna_rupa = prolazi[sprat]+sirina_rupe
    if(player.x > leva_rupa and player.x+20 < desna_rupa): #DA LI JE U RUPI
        u_rupi = True
    else:
        u_rupi = False
    if(((igrac_gornja < gornja_linija and igrac_donja >gornja_linija) or (igrac_gornja < donja_linija and igrac_donja > donja_linija) or (igrac_gornja < gornja_linija and igrac_donja > donja_linija)) and u_rupi == False):
        mixer.Sound.play(gameover_sound)
        game_over = True
def pomeranje(key_presed):
    global jumping,fall,pressed_up,skok,sprat
    if key_presed[pygame.K_LEFT] and jumping==False and fall == False:
        #mixer.Sound.play(move_sound)
        player.x-=5
        pressed_up = False
    elif(key_presed[pygame.K_RIGHT] and jumping==False and fall == False):
        #mixer.Sound.play(move_sound)
        player.x+=5
        pressed_up = False
    elif(key_presed[pygame.K_UP] and jumping == False and pressed_up == False and skok==True and fall==False):
        mixer.Sound.play(jump_sound)
        sprat = (player.y)//70-1
        jumping = True
        pressed_up=True
        skok = False
def skakanje():
    global jumping,count
    count+=1
    player.y-=3
    if count==30:
        jumping=False
        count=0

def provera_podloge():
    global granica
    pom = player.y // 70
    gornja_linija = pom*70+65
    if player.y+20 < gornja_linija:
        granica = gornja_linija
        return True
    elif (player.x > prolazi[pom] and player.x+20 < prolazi[pom] +sirina_rupe) and pom != 9:
        granica = (pom+1)*70+65
        return True
    else:
        return False
def pad(granica):
    global fall
    if(granica-player.y < 23):
        player.y=granica-20
        fall = False
    else:
        player.y+=3
def provera_next_levela(sprat):
    global level,game_over,finished
    if sprat == 0:
        finished = True
        game_over = True
        level+=1
if __name__ == "__main__":
    makeLevel(level)
    main()
