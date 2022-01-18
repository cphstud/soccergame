import pygame
import sys
import re
from xml.dom import minidom
from settings import *
from Player import Player
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import asyncio
from pathlib import Path
from tempfile import gettempdir
import aiofiles



def initPlayers(playersDict,playersDictO,playingPlayers, pickedPlayingPlayersDict):
    xmldoc = minidom.parse('../resources/Sample_Game_3_metadata.xml')
    itemlist = xmldoc.getElementsByTagName('Player')
    tmpList = xmldoc.getElementsByTagName('PlayerChannels')
    idlist=tmpList[0].getElementsByTagName('PlayerChannel')
    tmppickedPLayers = xmldoc.getElementsByTagName('DataFormatSpecifications')
    pickedPlayersRoot = tmppickedPLayers[0].getElementsByTagName('DataFormatSpecification')[0]
    pickedPlayers = pickedPlayersRoot.getElementsByTagName('PlayerChannelRef')
    for p in itemlist:
        sid = p.getElementsByTagName('ShirtNumber')[0].firstChild.nodeValue
        pid = p.getAttribute('id')
        tid = p.getAttribute('teamId')
        name = p.getElementsByTagName('Name')[0].firstChild.data
        role = p.getElementsByTagName('Value')[0].firstChild.data
        player = {'sid': sid, 'pid': pid, 'tid': tid, 'name': name, 'role': role}
        oPlayer = Player(0, 0, tid, sid,role, name)
        playersDict[pid]=player
        playersDictO[pid]=player

    for p in idlist:
        chid=p.getAttribute('id')
        temppid=p.getAttribute('playerId')
        if temppid in playersDict.keys():
            playersDict[temppid]['chid']=chid
            pickedPlayingPlayersDict[chid]=playersDict[temppid]

    for p in pickedPlayers:
        if "_y" in p.getAttribute('playerChannelId'):
            tmpchid=p.getAttribute('playerChannelId')
            playingPlayers.append(p.getAttribute('playerChannelId'))


def setupGame(playingPlayers,pickedPlayingPlayersDict):
    pygame.init()
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
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

    x_speed = 2
    y_speed = 0
    speed = [x_speed, y_speed]
    #WHITE = (255, 255, 255)
    #AWAY = (155, 155, 55)
    #HOME = (223, 20, 110)
    #BLACK=(0,0,0)
    counter = 0
    runGame(pitch,clock,counter,lines,screen,rect,speed,playingPlayers,pickedPlayingPlayersDict)


def drawVor(points):
    fname="../resources/foo.png"
    vor = Voronoi(points)
    fig = voronoi_plot_2d(vor)
    #plt.show()
    plt.savefig(fname)
    vordiag=pygame.image.load(fname)
    return vordiag



def pause(screen,clock,counter,points):
    paused=True
    while paused:
        print(counter)
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    print("go vor")
                    diag=drawVor(points)
                    screen.blit(diag,(0,0))
                    print("done vor")
                elif event.key == pygame.K_c:
                    paused=False
                elif event.key == pygame.K_q:
                    pygame.quit()
        pygame.display.update()
        clock.tick(4)



def runGame(pitch,clock,counter,lines,screen,rect,speed,playingPlayers,pickedPlayingPlayersDict):
    font = pygame.font.Font(None, 32)
    fontPlayer = pygame.font.SysFont('Arial', 12)
    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    playerNumberColor=pygame.Color('ghostwhite')
    active = False
    text = ''
    while counter < len(lines):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if text.isdigit():
                            print("NUM: ",text)
                            counter=int(text)
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                if event.key == pygame.K_p:
                    print("K: ",pygame.key.name(event.key))
                    pause(screen,clock,counter,points)
                elif event.key == pygame.K_b:
                    print("B: ", pygame.key.name(event.key))
                    pause(screen,clock, counter,points)
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                else:
                    pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive


            #if event.type == pygame.MOUSEBUTTONDOWN:
            #    pygame.quit()
            #    sys.exit()
        if "NaN" in lines[counter]:
            lines[counter]=re.sub("NaN","0.0",lines[counter])

        ll = [re.findall('([\w.]+)', x) for x in lines[counter].split(';') ]
        kk = [tuple(t) for t in ll]
        points = [(int(1 * (float(el[0]))*WIDTH), int(1 * (float(el[1]))*HEIGHT)) for el in kk]

        screen.fill(WHITE)
        screen.blit(pitch, (0, 0))
        rect = rect.move(speed)
        if rect.left < 0 or rect.right > WIDTH:
            speed[0] = -1 * speed[0]

        pcounter=-1
        ballPos=points.pop()
        for point in points:
            pcounter+=1
            tmpchid=playingPlayers[pcounter]
            tmpTeam=pickedPlayingPlayersDict[tmpchid]['tid']
            tmpRole=pickedPlayingPlayersDict[tmpchid]['role']
            tmpNumOnShirt=pickedPlayingPlayersDict[tmpchid]['sid']
            col=AWAY if tmpTeam=="FIFATMA" else HOME
            noteOnPlayer = fontPlayer.render(pickedPlayingPlayersDict[tmpchid]['sid'],True,playerNumberColor)
            pygame.draw.circle(screen,col,point,RAD)
            screen.blit(noteOnPlayer,point)

        pygame.draw.circle(screen, BLACK, ballPos, (RAD / 2))
        ####

        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        xwidth = max(200, txt_surface.get_width() + 10)
        input_box.w = xwidth
        # Blit the text.
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)

        ###
        pygame.display.update()
        clock.tick(120)
        counter += 1
    pygame.quit()
    sys.exit()

def main():
    playersDict = {}
    playersDictO = {}
    playingPlayers = []
    pickedPlayingPlayersDict = {}
    initPlayers(playersDict,playersDictO,playingPlayers, pickedPlayingPlayersDict)
    setupGame(playingPlayers,pickedPlayingPlayersDict)

if __name__ == '__main__':
    main()
