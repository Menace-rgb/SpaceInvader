import pygame as pg
import random
import math 


#initializing pygame
pg.init()
w = 900
h = 600
score_value = 0
#creating screen
screen = pg.display.set_mode((w,h))




background = pg.image.load('background.png')
laser = pg.image.load('laser.png')
explode = pg.image.load('explode.png')
display_duration = 1000
start_time = None
clock = pg.time.Clock()

#title and icon
pg.display.set_caption("Space Invader")
icon = pg.image.load('space-travel.png')
pg.display.set_icon(icon)

#restart
def restart_game():
    pass


#player
playerImg = pg.image.load('space-shuttle.png')
XPl = 375
YPl = 500
XChange = 0
YChange = 0


def player(x,y):
    screen.blit(playerImg, (x, y))


#enemy
enemyImg = []
XEn = []
YEn = []
EnXChange = []
EnYChange = []
EnNum = 7
for i in range(EnNum):
    image = [pg.image.load('enemy.png'),pg.image.load('enemy2.png'),pg.image.load('enemy3.png'),pg.image.load('enemy4.png'),pg.image.load('enemy5.png')]
    randomc = random.choice(image)
    if i <=5:
        enemyImg.append(image[i-1])
    else:
        enemyImg.append(randomc)
    XEn.append(random.randint(0,w-64))
    YEn.append(random.randint(0, 150 ))
    EnXChange.append((random.choice([1,-1]))*0.1 + 100*score_value )
    EnYChange.append(0.0075 + 100*score_value)



def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))


#laser
laserImg = pg.image.load('laser.png')
XLa = XPl
YLa = YPl
LaYChange = 1
La_State= 'ready'

#score

font = pg.font.Font('freesansbold.ttf',35)
textX= 15
textY= 15

def show_score(x,y):
    score = font.render("Score: "+ str(score_value),True, (255, 255,255))
    screen.blit (score,(x,y) )

over_font = pg.font.Font('freesansbold.ttf',75)


def game_over_text():
    
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                restart_game()
    game = over_font.render("GAME OVER",True, (255, 0,0))
    screen.blit (game,(200,200) )
    restart = over_font.render("Press 'R' to  restart", True, (0,255,0))
    screen.blit(restart, (100, 300))
    

    


    
las1x = 0
lasy = 0
las2x = 0
def fireLaser(x,y):
    global La_State
    La_State = 'fire'
    global las1x
    global lasy
    global las2x
    las1x = x+10
    lasy = y+10
    las2x = x+40
    screen.blit(laserImg, (las1x, lasy))
    screen.blit(laserImg, (las2x, lasy))
    

def isCollison(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))
    if distance < 40:
        return True
    else:
        return False



#game loop
running = True

while running:
    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        #for keystrokes
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                XChange = -0.4
            if event.key == pg.K_RIGHT:
                XChange = 0.4
            if event.key == pg.K_UP:
                YChange = -0.4
            if event.key == pg.K_DOWN:
                YChange = 0.4

            if event.key == pg.K_SPACE:
                if La_State == 'ready':
                    LaX = XPl
                    fireLaser(LaX, YLa)

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT :
                XChange = -0.01
                YChange = 0
            elif event.key == pg.K_RIGHT:
                YChange = 0  
                XChange = 0.01
            elif event.key == pg.K_UP:
                YChange = -0.01  
                XChange = 0 
            elif event.key == pg.K_DOWN:
                YChange = 0.01  
                XChange = 0
            
               


    XPl += XChange
    YPl += YChange
    if XPl <= 0:
        XPl = 0
    elif XPl >= w-64:
        XPl = w-64

    if YPl <= 0:
        YPl = 0
    elif YPl >= h-64:
        YPl = h-64

    player(XPl, YPl)

        #collison for player and enemy
    for i in range(EnNum):
            #Game Over
        col = isCollison(XPl, YPl, XEn[i], YEn[i])
        if col:
            start_time = pg.time.get_ticks()
            elapsed_time = pg.time.get_ticks() - start_time
            if elapsed_time < 1000:
                screen.blit(explode, (XPl, YPl) )
                pg.display.flip()
                YPl = 2000
            clock.tick(60)
            for j in range(EnNum):
                YEn[j] = 2000
            game_over_text()
                
        
        #setting boundaries
    for i in range(EnNum):
        #Game Over
        if YEn[i]> 400:
            for j in range(EnNum):
                YEn[j] = 2000
            
            game_over_text()
            break

        if XEn[i] <= 0:
            XEn[i] = 0
            EnXChange[i] *= -1 
        elif XEn[i] >= w-64:
            XEn[i] = w-64
            EnXChange[i] *= -1

        
        elif YEn[i] >= h-128:
            YEn[i] = h-128
        XEn[i] += EnXChange[i]
        YEn[i] += EnYChange[i]
            #collison
        collison = isCollison(XEn[i], YEn[i], las1x, lasy) or isCollison(XEn[i], YEn[i], las2x, lasy)
        if collison:
            YLa = YPl
            La_State = 'ready'
            score_value += 1
                #explosion
            start_time = pg.time.get_ticks()
            elapsed_time = pg.time.get_ticks() - start_time
            if elapsed_time < display_duration:
                screen.blit(explode, (XEn[i], YEn[i]) )
                pg.display.flip()

                #print(score_value)
            XEn[i] = random.randint(0, w-64)
            YEn[i] = random.randint(0, 150)
            EnXChange[i]+= score_value*0.0001
            EnYChange[i] += score_value*0.0002
            LaYChange += score_value*0.001
            

                
        enemy (XEn[i], YEn[i],i)


        

        #laser movement
    if La_State == 'fire':
        fireLaser(LaX, YLa)
        YLa -= LaYChange

        
    if YLa < 0:
        La_State = 'ready'
        #print('Im ready')
        YLa = YPl

    show_score(textX, textY)      



    

        
    pg.display.update()
