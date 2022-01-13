import pygame
import sys
import os
import re
import xml.etree.ElementTree  as et
from xml.dom import minidom

def initPlayers():
    xmldoc = minidom.parse('../resources/Sample_Game_3_metadata.xml')
    itemlist = xmldoc.getElementsByTagName('Player')
    tmpList = xmldoc.getElementsByTagName('PlayerChannels')
    idlist=tmpList[0].getElementsByTagName('PlayerChannel')
    tmppickedPLayers=xmldoc.getElementsByTagName('DataFormatSpecifications')
    rootpickedPlayers=tmppickedPLayers[0].getElementsByTagName('DataFormatSpecification')
    pickedPlayers=rootpickedPlayers[0].getElementsByTagName('PlayerChannelRef')
    player = {}
    for p in itemlist:
        sid = p.getElementsByTagName('ShirtNumber')[0].firstChild.nodeValue
        pid = p.getAttribute('id')
        tid = p.getAttribute('teamId')
        name = p.getElementsByTagName('Name')[0].firstChild.data
        role = p.getElementsByTagName('Value')[0].firstChild.data
        player = {'sid': sid, 'pid': pid, 'tid': tid, 'name': name, 'role': role}
        players.append(player)
        playersDict[pid]=player
    for p in idlist:
        chid=p.getAttribute('id')
        temppid=p.getAttribute('playerId')
        d={'chid':chid}
        print(d)
        if temppid in playersDict.keys():
            playersDict[temppid]['chid']=chid
            print("S ",playersDict[temppid])

    for p in pickedPlayers:
        pass
    print("done")

players = []
playersDict = {}
playingPlayersDict = {}
initPlayers()
#sys.exit(0)
pygame.init()
width = 2 * 479
height = 2 * 359
size = (width, height)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

print(os.getcwd())
# load player data
#fh = open("../resources/twoplayers1ball", "r")
fh = open("../resources/test2", "r")
lines = fh.readlines()

wood_bg = pygame.image.load("../resources/footballpitch.jpg")
# wood_bg=pygame.image.load("resources/green2.png")
wood_bg = pygame.transform.scale(wood_bg, size)
# tree=pygame.image.load("resources/tree.png")

ball = pygame.image.load("../resources/ball.jpeg")
ball = pygame.transform.scale(ball, (20, 20))
rect = ball.get_rect()
c_x = 23
c_y = 100
rad = 12
# circle=pygame.draw.circle(screen,(234,211,34),(c_x,c_y),rad)

x_speed = 2
y_speed = 0
speed = [x_speed, y_speed]
WHITE = (255, 255, 255)
AWAY = (155, 155, 55)
HOME = (23, 200, 210)
BLACK=(0,0,0)
counter = 0

while counter < len(lines):
    print(lines[counter])

    ll = [re.findall('([\w.]+)', x) for x in lines[counter].split(';') ]
    kk = [tuple(t) for t in ll]
    if "NaN" in lines[counter]:
        counter +=1
        continue
    points = [(int(1 * (float(el[0]))*width), int(1 * (float(el[1]))*height)) for el in kk]

    screen.fill(WHITE)
    screen.blit(wood_bg, (0, 0))
    # x_pos=x_pos+1
    rect = rect.move(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # screen.blit(wood_bg, (0,0))
    #screen.blit(ball, rect)

    if rect.left < 0 or rect.right > width:
        speed[0] = -1 * speed[0]

    # rect.move(speed)
    # screen.blit(tree, (100,100))
    #points=[(0.84219,0.51681), (0.63861,0.19465), (0.50125,0.48725)]
    #[pygame.draw.circle(screen,(234,211,34),point,rad) for point in points]
    pcounter=0
    ballPos=points.pop()
    for point in points:
        pcounter+=1
        print(players[pcounter]['tid'])
        col=AWAY if players[pcounter]['tid']=="FIFATMA" else HOME
        pygame.draw.circle(screen,col,point,rad)
    pygame.draw.circle(screen, BLACK, ballPos, (rad/2))
    #pygame.draw.circle(screen,(134,111,34),points[1],rad)
    #pygame.draw.circle(screen,(0,0,0),points[2],rad)
    pygame.display.update()
    clock.tick(40)
    counter += 1
pygame.quit()
sys.exit()


