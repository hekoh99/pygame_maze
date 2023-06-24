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

    def __init__(self, player, map, gameDisplay):
        self.map = map
        self.player = player
        self.gameDisplay = gameDisplay

    def drawMap(self):
        posY = 0
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
                    self.gameDisplay.blit(DOOR_OPENED, (posX * 50, posY * 50))
                posX += 1
            posY += 1
        self.player.placePlayer()

    def movePlayer(self, posX, posY):
        nxtPosX = self.player.posX + posX
        nxtPosY = self.player.posY + posY
        if self.map[nxtPosY][nxtPosX] != '1':
            self.player.move(posX, posY)

## 선(line) 및 도형 그리기 ##
# 파라미터 설명
# pygame.draw.shape(surface, color, pointlist(centerpoint), width)
# surface: 어느 게임 창에 위치시킬 것인지 설정
# color: 오브젝트 색상 설정
# pointlist: 튜플형식으로 각 포인트(각)의 좌표를 설정
# start_point, end_point, centerpoint: 시작 좌표, 끝점, 가운데 좌표
# width: 도형 테두리 굵기 지정
"""
# 선
pygame.draw.line(surface, color, start_point, end_point, width)
pygame.draw.lines(surface, color, closed, pointlist, width)

# 면
pygame.draw.polygon(surface, color, pointlist, width)

# 원
pygame.draw.circle(surface, color, center_point, radius, width)

# 타원
pygame.draw.ellipse(surface, color, bounding_rectangle, width)

# 직사각형
pygame.draw.rect(surface, color, rectangle_tuple, width)
#rectangle_tuple은 (사각형시작x좌표,사각형시작y좌표,가로길이,세로길이) 의 튜플로 이루어져 있음
"""
#도형 예제
# pygame.draw.circle(GameDisplay,BLACK,(100,50),30)
# pygame.draw.line(GameDisplay,BLUE,(200,20),(180,60))
# pygame.draw.line(GameDisplay,BLUE,(200,20),(220,60))
# pygame.draw.line(GameDisplay,BLUE,(180,60),(220,60))
# pygame.draw.rect(GameDisplay,RED,(300,20,50,50),2)
# pygame.draw.ellipse(GameDisplay,GREEN,(400,20,80,50),2)

def parseMap(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 'P':
                return i, j

def getMap(file):
    map = open(file, 'r')
    ret = map.readlines()
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
                print("keydown")
                if event.key == pygame.K_UP:
                    print("up key")
                    game.movePlayer(0, 1)
                if event.key == pygame.K_RIGHT:
                    game.movePlayer(1, 0)
                if event.key == pygame.K_LEFT:
                    game.movePlayer(-1, 0)
                if event.key == pygame.K_DOWN:
                    game.movePlayer(0, -1)
        game.drawMap() 