import sys
import pygame
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
WIDTH = 640
HEIGHT = 440

# 게임 화면
WALL = pygame.image.load("wall.png")
WALL = pygame.transform.scale(WALL, (50, 50))

FLOOR = pygame.image.load("floor.png")
FLOOR = pygame.transform.scale(FLOOR, (50, 50))

ITEM = pygame.image.load("present.png")
ITEM = pygame.transform.scale(ITEM, (50, 50))

DOOR_CLOSED = pygame.image.load("closed.png")
DOOR_CLOSED = pygame.transform.scale(DOOR_CLOSED, (60, 60))

DOOR_OPENED = pygame.image.load("opened.png")
DOOR_OPENED = pygame.transform.scale(DOOR_OPENED, (60, 60))

# PLAYER = pygame.image.load("player.png")
# PLAYER = pygame.transform.scale(PLAYER, (50, 50))

class Player:
    posX = 0
    posY = 0
    playerImg = pygame.image.load("player.png")

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

    def movePlayer(self, posX, posY):
        nxtPosX = self.player.posX + posX
        nxtPosY = self.player.posY + posY
        if self.map[nxtPosY][nxtPosX] != '1':
            self.player.move(posX, posY)
        if self.map[nxtPosY][nxtPosX] == 'C':
            self.collected += 1
            if self.collected == 1:
                self.allCollected = True
            self.map[nxtPosY][nxtPosX] = '0'
        if self.map[nxtPosY][nxtPosX] == 'E' and self.allCollected:
            self.completed = True


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

if __name__ == "__main__":
    ## 게임 창 설정 ##
    map = getMap("easy.map")
    GameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
    GameDisplay.fill(WHITE)
    i, j = parseMap(map)
    player = Player(i, j, "player.png")
    game = Game(player, map, GameDisplay)
    pygame.display.set_caption("PYGAME Example") # 창 이름 설정
    while True :
        FramePerSec.tick(FPS)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.movePlayer(0, 1)
                if event.key == pygame.K_RIGHT:
                    game.movePlayer(1, 0)
                if event.key == pygame.K_LEFT:
                    game.movePlayer(-1, 0)
                if event.key == pygame.K_DOWN:
                    game.movePlayer(0, -1)
        game.drawMap()