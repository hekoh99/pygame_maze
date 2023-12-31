import sys
import pygame
import time
from pygame.locals import *

## pygame 기능 사용을 시작하는 명령어 ##
pygame.init()

## 초당 프레임 단위 설정 ##
FPS = 30
FramePerSec = pygame.time.Clock()

## 컬러 세팅 ##
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

## 화면 사이즈
WIDTH = 1000
HEIGHT = 600

# 게임 화면
WALL = pygame.image.load("res/img/wall.png")
WALL = pygame.transform.scale(WALL, (50, 50))

FLOOR = pygame.image.load("res/img/floor.png")
FLOOR = pygame.transform.scale(FLOOR, (50, 50))

ITEM = pygame.image.load("res/img/present.png")
ITEM = pygame.transform.scale(ITEM, (50, 50))

DOOR_CLOSED = pygame.image.load("res/img/closed.png")
DOOR_CLOSED = pygame.transform.scale(DOOR_CLOSED, (60, 60))

DOOR_OPENED = pygame.image.load("res/img/opened.png")
DOOR_OPENED = pygame.transform.scale(DOOR_OPENED, (60, 60))

# PLAYER = pygame.image.load("player.png")
# PLAYER = pygame.transform.scale(PLAYER, (50, 50))

## SOUND
END_SOUND = pygame.mixer.Sound("res/sounds/birthday_background.mp3")
GUIDE_VOICE = pygame.mixer.Sound("res/sounds/Guide_voice.mp3")
DOOR_SOUND = pygame.mixer.Sound("res/sounds/doorOpen.mp3")

## 게임 문구
# GAME_FONT = pygame.font.Font( None, 15)
# CLICK_GUIDE = GAME_FONT.render("Click  Items", True, WHITE)
CLICK_GUIDE = pygame.image.load("res/img/guide_text.png")
CLICK_GUIDE = pygame.transform.scale(CLICK_GUIDE, (380, 120))

HAPPY_BIRTHDAY = pygame.image.load("res/img/happy_birthday_text.png")
HAPPY_BIRTHDAY = pygame.transform.scale(HAPPY_BIRTHDAY, (450, 200))

## 게임 상태 flag
## 게임 시작 전 : 0
## 게임 중 : 1
## 게임 성공 후 : 2
gameFlag = 0

# 선물 상자 이벤트
clickedItemNum = 0
SUNSET = pygame.image.load("res/img/sunset.png")
SUNSET = pygame.transform.scale(SUNSET, (126 * 4, 95 * 4))

CAKE = pygame.image.load("res/img/cake.png")
CAKE = pygame.transform.scale(CAKE, (1004 / 2, 741 / 2))

SMILE = pygame.image.load("res/img/happyFace.png")
SMILE = pygame.transform.scale(SMILE, (53 * 5, 78 * 5))

BYE = pygame.image.load("res/img/bye.png")
BYE = pygame.transform.scale(BYE, (842 / 3, 1112 / 3))

LAY = pygame.image.load("res/img/laydown.png")
LAY = pygame.transform.scale(LAY, (1146 / 2, 774 / 2))


class Player:
    posX = 0
    posY = 0
    playerImg = pygame.image.load("res/img/player.png")

    def __init__(self, posX, posY, img):
        self.posX = posX
        self.posY = posY
        self.playerImg = pygame.image.load(img)
        self.playerImg = pygame.transform.scale(self.playerImg, (50, 50))


    def move(self, posX, posY):
        self.posX += posX
        self.posY += posY

    def placePlayer(self):
        GameDisplay.blit(self.playerImg, (self.posX * 50, self.posY * 50))

class Game:
    map = []
    player = None
    gameDisplay = None
    collected = 0
    allCollected = False
    completed = False

    def __init__(self, player, map, gameDisplay):
        self.map = map
        self.player = player
        self.gameDisplay = gameDisplay
        self.collected = 0
        self.allCollected = False
        self.completed = False

    def drawMap(self):
        if self.completed == False:
            posY = 0
            door = DOOR_CLOSED
            if self.allCollected:
                door = DOOR_OPENED
            for i in map:
                posX = 0
                for j in i:
                    if j == '\n':
                        continue
                    if j == '1':
                        self.gameDisplay.blit(WALL, (posX * 50, posY * 50))
                    else : 
                        self.gameDisplay.blit(FLOOR, (posX * 50, posY * 50))

                    if j == 'C':
                        self.gameDisplay.blit(ITEM, (posX * 50, posY * 50))
                    elif j == 'E':
                        self.gameDisplay.blit(door, (posX * 50, posY * 50))
                    posX += 1
                posY += 1
            self.player.placePlayer()
        else :
            self.gameDisplay.fill(BLACK)
            ITEM_DONE = pygame.transform.scale(ITEM, (70, 70))
            init = 165
            self.gameDisplay.blit(ITEM_DONE, (init, 50))
            self.gameDisplay.blit(ITEM_DONE, (init + 150, 50))
            self.gameDisplay.blit(ITEM_DONE, (init + 150 * 2, 50))
            self.gameDisplay.blit(ITEM_DONE, (init + 150 * 3, 50))
            self.gameDisplay.blit(ITEM_DONE, (init + 150 * 4, 50))
            self.gameDisplay.blit(CLICK_GUIDE, (WIDTH/2 - 190, 15))
            self.gameDisplay.blit(HAPPY_BIRTHDAY, (WIDTH/2 - 230, HEIGHT / 4))
            self.gameDisplay.blit(self.player.playerImg, (WIDTH/2 - 25, HEIGHT * 2/3))
            # 선물 상자 클릭에 대한 이벤트
            if clickedItemNum == 1:
                self.gameDisplay.blit(CAKE, (WIDTH / 2 - (1004 / 4), 150))
            elif clickedItemNum == 2:
                self.gameDisplay.blit(SMILE, (WIDTH / 2 - (53 * 5 / 2), 150))
            elif clickedItemNum == 3:
                self.gameDisplay.blit(LAY, (WIDTH / 2 - (1146 / 4), 150))
            elif clickedItemNum == 4:
                self.gameDisplay.blit(SUNSET, (WIDTH / 2 - (126 * 4 / 2), 150))
            elif clickedItemNum == 5:
                self.gameDisplay.blit(BYE, (WIDTH / 2 - (842 / 6), 150))


    def movePlayer(self, posX, posY):
        nxtPosX = self.player.posX + posX
        nxtPosY = self.player.posY + posY
        if self.map[nxtPosY][nxtPosX] == '0' or self.map[nxtPosY][nxtPosX] == 'C' or self.map[nxtPosY][nxtPosX] == 'P' or (self.map[nxtPosY][nxtPosX] == 'E' and self.allCollected):
            self.player.move(posX, posY)
        if self.allCollected == False and self.map[nxtPosY][nxtPosX] == 'E':
            GUIDE_VOICE.play()
        if self.map[nxtPosY][nxtPosX] == 'C':
            self.collected += 1
            if self.collected == 5:
                self.allCollected = True
                DOOR_SOUND.play()
                DOOR_SOUND.fadeout(1000)
            self.map[nxtPosY][nxtPosX] = '0'
        if self.map[nxtPosY][nxtPosX] == 'E' and self.allCollected:
            self.completed = True
            global gameFlag
            gameFlag = 2
            END_SOUND.play()
            END_SOUND.set_volume(0.5)
            END_SOUND.fadeout(23500) # 23.5초

def parseMap(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 'P':
                return i, j

def getMap(file):
    map = open(file, 'r')
    mapInStr = map.readlines()
    ret = []
    for i in mapInStr:
        line = []
        for j in i:
            if (j != '\n'):
                line.append(j)
        ret.append(line)
    map.close()
    return ret

def getClickedItem():
    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos[0] >= 175 and mouse_pos[0] <= 225 :
        if mouse_pos[1] >= 60 and mouse_pos[1] <= 110 :
            return 1
    if mouse_pos[0] >= 328 and mouse_pos[0] <= 375 :
        if mouse_pos[1] >= 60 and mouse_pos[1] <= 110 :
            return 2
    if mouse_pos[0] >= 478 and mouse_pos[0] <= 525 :
        if mouse_pos[1] >= 60 and mouse_pos[1] <= 110 :
            return 3
    if mouse_pos[0] >= 628 and mouse_pos[0] <= 675 :
        if mouse_pos[1] >= 60 and mouse_pos[1] <= 110 :
            return 4
    if mouse_pos[0] >= 777 and mouse_pos[0] <= 824 :
        if mouse_pos[1] >= 60 and mouse_pos[1] <= 110 :
            return 5
    return 0

if __name__ == "__main__":
    ## 게임 창 설정 ##
    gameFlag = 1
    map = getMap("res/map/happy_birthday.map")
    GameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
    GameDisplay.fill(WHITE)
    i, j = parseMap(map)
    player = Player(j, i, "res/img/player.png")
    game = Game(player, map, GameDisplay)
    pygame.display.set_caption("Happy Birthday Minhyoung") # 창 이름 설정
    while True :
        FramePerSec.tick(FPS)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.movePlayer(0, -1)
                if event.key == pygame.K_RIGHT:
                    game.movePlayer(1, 0)
                if event.key == pygame.K_LEFT:
                    game.movePlayer(-1, 0)
                if event.key == pygame.K_DOWN:
                    game.movePlayer(0, 1)
            if event.type == pygame.MOUSEBUTTONDOWN and gameFlag == 2:
                clickedItemNum = getClickedItem()
        game.drawMap()