import pygame
import sys
import os
import re
import xml.etree.ElementTree  as et
from xml.dom import minidom

def initPlayers(playersDict,playingPlayers, pickedPlayingPlayersDict):
    xmldoc = minidom.parse('../resources/Sample_Game_3_metadata.xml')
    itemlist = xmldoc.getElementsByTagName('Player')
    tmpList = xmldoc.getElementsByTagName('PlayerChannels')
    idlist=tmpList[0].getElementsByTagName('PlayerChannel')
    tmppickedPLayers = xmldoc.getElementsByTagName('DataFormatSpecifications')
    pickedPlayersRoot = tmppickedPLayers[0].getElementsByTagName('DataFormatSpecification')[0]
    pickedPlayers = pickedPlayersRoot.getElementsByTagName('PlayerChannelRef')
    player = {}
    for p in itemlist:
        sid = p.getElementsByTagName('ShirtNumber')[0].firstChild.nodeValue
        pid = p.getAttribute('id')
        tid = p.getAttribute('teamId')
        name = p.getElementsByTagName('Name')[0].firstChild.data
        role = p.getElementsByTagName('Value')[0].firstChild.data
        player = {'sid': sid, 'pid': pid, 'tid': tid, 'name': name, 'role': role}
        playersDict[pid]=player

    for p in idlist:
        chid=p.getAttribute('id')
        temppid=p.getAttribute('playerId')
        d={'chid':chid}
        if temppid in playersDict.keys():
            playersDict[temppid]['chid']=chid
            pickedPlayingPlayersDict[chid]=playersDict[temppid]

    for p in pickedPlayers:
        if "_y" in p.getAttribute('playerChannelId'):
            tmpchid=p.getAttribute('playerChannelId')
            playingPlayers.append(p.getAttribute('playerChannelId'))


def main():
    playersDict = {}
    playingPlayers = []
    pickedPlayingPlayersDict = {}
    initPlayers(playersDict,playingPlayers, pickedPlayingPlayersDict)
    setupGame(playingPlayers,pickedPlayingPlayersDict)

def setupGame(playingPlayers,pickedPlayingPlayersDict):
    pygame.init()
    width = 2 * 479
    height = 2 * 359
    size = (width, height)
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    # load player data
    fh = open("../resources/firstframes.csv", "r")
    lines = fh.readlines()

    pitch = pygame.image.load("../resources/footballpitch.jpg")
    pitch = pygame.transform.scale(pitch, size)

    ball = pygame.image.load("../resources/ball.jpeg")
    ball = pygame.transform.scale(ball, (20, 20))
    rect = ball.get_rect()
    c_x = 23
    c_y = 100
    rad = 8

    x_speed = 2
    y_speed = 0
    speed = [x_speed, y_speed]
    WHITE = (255, 255, 255)
    AWAY = (155, 155, 55)
    HOME = (223, 20, 110)
    BLACK=(0,0,0)
    counter = 0
    runGame(rad,clock,counter,lines,screen,WHITE,AWAY,HOME,BLACK,width,height,pitch,rect,speed,playingPlayers,pickedPlayingPlayersDict)


def runGame(rad,clock,counter,lines,screen,WHITE,AWAY,HOME,BLACK,width,height,pitch,rect,speed,playingPlayers,pickedPlayingPlayersDict):
    while counter < len(lines):
        if "NaN" in lines[counter]:
            lines[counter]=re.sub("NaN","0.0",lines[counter])

        ll = [re.findall('([\w.]+)', x) for x in lines[counter].split(';') ]
        kk = [tuple(t) for t in ll]
        points = [(int(1 * (float(el[0]))*width), int(1 * (float(el[1]))*height)) for el in kk]

        screen.fill(WHITE)
        screen.blit(pitch, (0, 0))
        rect = rect.move(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if rect.left < 0 or rect.right > width:
            speed[0] = -1 * speed[0]

        pcounter=-1
        ballPos=points.pop()
        for point in points:
            pcounter+=1
            tmpchid=playingPlayers[pcounter]
            tmpTeam=pickedPlayingPlayersDict[tmpchid]['tid']
            tmpRole=pickedPlayingPlayersDict[tmpchid]['role']
            col=AWAY if tmpTeam=="FIFATMA" else HOME
            pygame.draw.circle(screen,col,point,rad)
        pygame.draw.circle(screen, BLACK, ballPos, (rad/2))
        pygame.display.update()
        clock.tick(40)
        counter += 1
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
