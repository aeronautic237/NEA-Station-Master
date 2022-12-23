#Made by Saambavan Thambiayah

#imports the rather unecessary libraries(!)
import pygame
import sys
import time
import csv
import threading

#initialise pygame
pygame.font.init()
pygame.init()

#make a screen
screen = pygame.display.set_mode((1280,720))
#increase in y-axis = decrease in altitude

#change the title and image of the window
pygame.display.set_caption("Station Master")
pygame.display.set_icon(pygame.image.load("icon.jpg"))

#This is our repository of colours
menuScreenColour= [100,100,128]
black=[0,0,0]
white=[225,225,225]
lightGreen=[50,225,50]
darkGrey=[75,75,75]
gold=[225,215,0]
lightBlue=[0,128,225]
pink = [255, 124, 200]
red = [255, 0, 0]
green = [0, 255, 0]

#Our repository of fonts
title = pygame.font.SysFont("Sans-serif", 200)
buttonFont = pygame.font.SysFont("Sans-serif", 100)
clockTextFont = pygame.font.SysFont("Sans-serif",50)
clockFont = pygame.font.SysFont("Sans-serif",100)
normal = pygame.font.SysFont("Sans-serif", 25)
criteriaFont = pygame.font.SysFont("Sans-serif", 40)

#declaring the state of the game - may not be necessary
gamestate = "menu"

#declare array
researchProgress = [[0 for x in range(2)] for y in range(33)]#create an array in which to store the data
trackLayout = [[0 for x in range(32)] for y in range(13)]#create an array in which the trackLayout is stored
entryLayout = [[0 for x in range(2)] for y in range(4)]#create an array in which the entry points are stored
timetableArray = [[0 for x in range(80)] for y in range(8)]#creates an array in which the timetable is to be stored

#defing the various functions of the game here

#this will increment the clock - needs to be called every second (or more depending on the multiplier
def incrementClock():
    pygame.draw.rect(screen, menuScreenColour, [510, 15, 310, 60])
    global timeHour
    global timeMinute
    global timeSecond
    int(timeSecond)
    int(timeHour)
    int(timeMinute)
    timeSecond = int(timeSecond) + 1 # increment seconds
    if int(timeSecond) == 60: # increment minutes
        timeSecond = 0
        timeMinute = int(timeMinute) + 1
    if int(timeMinute) == 60: # increment hours
        timeMinute = 0
        timeHour = int(timeHour) + 1
    if int(timeHour) == 24: # increment days (reset clock)
        timeHour = 4
    #if int(timeSecond) < 10:
     #   timeSecond = "0" + str(timeSecond)
    #if int(timeMinute) < 10:
     #   timeMinute = "0" + str(timeMinute)
    #if int(timeHour) < 10:
     #   timeHour = "0" + str(timeHour)
    print(timeSecond)
    print(timeMinute)
    print(timeHour)
    write(str(timeHour).zfill(2) + ":" + str(timeMinute).zfill(2) + ":" + str(timeSecond).zfill(2), clockFont, white, 510, 15)
    pygame.display.update()


def mainMenu():

    #This will draw the menu
    screen.fill((menuScreenColour))
    startButton = button(black, [440, 300, 400, 100], "Play", buttonFont, white, 570, 315)
    startButton.drawButton()
    quitButton = button(black, [440, 440, 400, 100], "Quit", buttonFont, white, 570, 455)
    quitButton.drawButton()
    write("Station Master", title, lightGreen, 150, 75)
    pygame.display.update()
    #menu has been drawn

    #now we need to make it functional
    waiting = True
    #will wait for an input
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                sys.exit()
            #reassigns the position of the mouse for everyevent
            mousePos = pygame.mouse.get_pos()
            if startButton.buttonCoords.collidepoint((mousePos)):
                startButton.changeButtonColour(darkGrey)
                if event.type == pygame.MOUSEBUTTONUP:#checks if the start button is pressed
                    with open("saveData/researched.txt","r") as fileOut:
                        reader = csv.reader(fileOut)
                        z=0
                        for row in reader:
                            researchProgress[z][0] = row[0]
                            researchProgress[z][1] = row[1]
                            z += 1#the above will assign each element of the text file to an element in the array
                        print(researchProgress)#debugging
                    game()
                    waiting = False
                    break
            elif quitButton.buttonCoords.collidepoint((mousePos)):
                quitButton.changeButtonColour(darkGrey)
                if event.type == pygame.MOUSEBUTTONUP:#checks if the quit button is pressed
                    waiting = False
                    #maybe add a screen here that says it is closing?
                    pygame.quit()
                    sys.exit()
                    break
            else:
                startButton.changeButtonColour(black)
                quitButton.changeButtonColour(black)
                #pygame.display.update()

#This is where the game is run
def game():
    multiplier = 1 # speed of the clock
    #this is mainly for debugging purposes, may not be necessary in the final build
    print("Starting Game")
    gameState = "game"
    timestate = "paused"
    #this is where we draw the first part of the game
    #drawing the tracks, stations, signals, and points
    screen.fill(black)
    with open("saveData/tracksPlatforms.txt", "r") as file:
        reader = csv.reader(file)
        i = 0
        for row in reader:
            trackLayout[i] = row
            i+=1
        i = 0
        for i in range(len(trackLayout)):
            for j in range(len(trackLayout[i])):
                if trackLayout[i-2][j] == "1": # normal track
                    pygame.draw.line(screen, white, ((40 * j) + 40, (140 + (40 * i))),((40 * j) + 80, (140 + (40 * i))))
                elif trackLayout[i-2][j] == "2": # upwards points
                    pygame.draw.line(screen, gold, ((40 * j) + 40, (140 + (40 * i))),((40 * j) + 80, (140 + (40 * i))))
                    pygame.draw.line(screen, gold, ((40 * j) + 60, (140 + (40 * i))),((40 * j) + 60, (120 + (40 * i))))
                elif trackLayout[i-2][j] == "3":#downwards points
                    pygame.draw.line(screen, gold, ((40 * j) + 40, (140 + (40 * i))),((40 * j) + 80, (140 + (40 * i))))
                    pygame.draw.line(screen, gold, ((40 * j) + 60, (140 + (40 * i))),((40 * j) + 60, (160 + (40 * i))))
                #replaces the square with a leftward set of signals
                elif trackLayout[i-2][j] == "5":
                    #signals will be triangles
                    pygame.draw.line(screen, white, ((40 * j) + 40, (140 + (40 * i))),((40 * j) + 80, (140 + (40 * i))))
                    pygame.draw.polygon(screen, red, (((40*j) + 53, (120 + (40 * i))),((40 * j) + 80 , (40 * i) + 140),((40 * j) + 53, (40 * i) + 160)))#This is a signal
                    pygame.display.update()
                #replaces the train with a rightward set of signals
                elif trackLayout[i-2][j] == "6":
                    pygame.draw.line(screen, white, ((40 * j) + 40, (140 + (40 * i))),((40 * j) + 80, (140 + (40 * i))))
                    pygame.draw.polygon(screen, red, (((40*j) + 67, (120 + (40 * i))),((40 * j) + 40 , (40 * i) + 140),((40 * j) + 67, (40 * i) + 160)))#This is a signal
                    pygame.display.update()
    with open("saveData/entryPoints.txt", "r") as file:
        reader = csv.reader(file)
        i = 0
        for row in reader:
            entryLayout[i] = row
            i += 1
        i = 0
        for i in range(4):
            for j in range(2):
                if entryLayout[i][j] == "1":
                    pygame.draw.line(screen, white, ((1240*j),(40 * i) + 300),((1240*j) + 40,(40 * i) + 300))
                    
    drawPlatform()
    #draw the top and bottom bar
    pygame.draw.rect(screen, menuScreenColour, [0, 0, 1280, 100])
    pygame.draw.rect(screen, menuScreenColour, [0, 620, 1280, 100])
    #add placeholders for the menu items
    #placeholder for money
    write("£ 0000", buttonFont, gold, 10, 10)
    #clock placeholder
    clockIcon = pygame.image.load("Clock_Icon.jpg")
    clockIcon = pygame.transform.scale(clockIcon, (75, 75))
    screen.blit(clockIcon, (420, 10))
    #placeholder to play the clock
    playClock = button(darkGrey, [920, 10, 75,75], "", buttonFont, white, 850, 20)
    playClockIcon = pygame.image.load("play_icon.png")
    playClockIcon = pygame.transform.scale(playClockIcon, (70, 70))
    playClock.drawButton()
    screen.blit(playClockIcon, (922.5, 12.5))
    #placeholder for the 5X clock speed
    clockX5 = button(darkGrey, [1000, 10, 75,75], "5x", clockTextFont, white, 1020, 30)
    clockX5.drawButton()
    clockX15 = button(darkGrey, [1080, 10, 75, 75], "15x", clockTextFont, white, 1090, 30)
    clockX15.drawButton()
    #placeholder for the 25X clock speed
    clockX25 = button(darkGrey, [1160, 10, 75, 75], "25x", clockTextFont, white, 1170, 30)
    clockX25.drawButton()
    pygame.draw.rect(screen, pink, [500, 10, 330, 75], 5)
    #list of multipliers:
    multipliers = [playClock, clockX5, clockX15, clockX25]
    #write("00:00:00", clockFont, white, 510, 15)
    #RDButton
    RDButton = button(darkGrey, [10, 635, 75, 75], "R&D", clockTextFont, white, 10, 655)
    RDButton.drawButton()
    #buy things button
    constructButton = button(darkGrey, [110, 635, 100, 75], "Shop", clockTextFont, white, 115, 655)
    constructButton.drawButton()
    #accepted and offered contract
    contractButton = button(darkGrey, [235, 635, 180, 75], "Contracts", clockTextFont, white, 240, 655)
    contractButton.drawButton()
    #potential fact button
    timetableButton = button(darkGrey, [430, 635, 170, 75], "Timetable", clockTextFont, white, 435, 655)
    timetableButton.drawButton()
    #return to main menu button
    menuButton = button(pink, [1200, 635, 75, 75], "", clockTextFont, white, 1210, 655)
    menuButton.drawButton()
    pygame.display.update()
    #this is where we do the mechanics
    waiting = True
    incrementer = RepeatedTimer(multiplier, incrementClock)
    while waiting == True:
        for event in pygame.event.get():
            if menuButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                menuButton.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    gamestate = "menu"
                    incrementer.stop()
                    mainMenu()
            elif RDButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                RDButton.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    incrementer.stop()
                    research()
            elif constructButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                constructButton.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    incrementer.stop()
                    shop()
            elif contractButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                contractButton.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    incrementer.stop()
                    contracts(menuButton)
            elif timetableButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                timetableButton.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    incrementer.stop()
                    timetableScreen(menuButton)
            elif playClock.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                playClock.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    multiplier = 1
            elif clockX5.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                clockX5.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    multiplier = 0.2
            elif clockX15.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                clockX15.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    multiplier = 1 / 15
            elif clockX25.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                clockX25.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    multiplier = 1 / 25
            elif event.type == pygame.QUIT:
                waiting = False
                incrementer.stop()
                pygame.quit()
                sys.exit()
            else:
                menuButton.changeButtonColour(darkGrey)
                RDButton.changeButtonColour(darkGrey)
                constructButton.changeButtonColour(darkGrey)
                contractButton.changeButtonColour(darkGrey)
                timetableButton.changeButtonColour(darkGrey)
                for i in range(0, len(multipliers)):
                    multipliers[i].changeButtonColour(darkGrey)
                    
    #train1 = train(white, 1230, 350, 50, 20, -1)
    #train1.drawTrain()
    #time.sleep(1)
    #train1.approachPlat()
    #time.sleep(5)
    #train1.departPlat()
    #train1.destroyTrain()
    #pygame.display.update()

def research():

    global researchProgress
    #This procedure will output an image (which is the format that the facts are in)
    #It should also show an unlock button if the criteria to unlock the technology are met, so that the user can unlock it if they want to
    def drawFact(item,i):
        global money
        filename = str(item[i]) + ".jpg"
        filename = "TECHNOLOGY/" + filename
        screen.fill(black)
        pygame.draw.rect(screen, darkGrey, [0, 620, 1280, 100])
        returnButton.drawButton()
        fact = pygame.image.load(filename)
        screen.blit(fact,(150,20))
        pygame.display.update()#This is the fact drawn
        unlockButton = button(darkGrey, [550,375,500,50], "Unlock now?", criteriaFont, white, 725, 388)
        queryDrawButton = False
        returnPrev = False
        while returnPrev == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()#red X in the top right corner programmed
                elif returnButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                    returnButton.changeButtonColour(pink)
                    if event.type == pygame.MOUSEBUTTONUP:
                        returnPrev = True
                        break#return button programmed
                else:
                    returnButton.changeButtonColour(menuScreenColour)
                    with open("criteria/research.txt", "r") as fileOut:#file containing every research, their critaria, and their effects
                        reader=csv.reader(fileOut)
                        for row in reader:
                            if row[0]==str(item[i]):
                                cost = int(row[1])
                                criterion1=row[2]
                                criterion2=row[3]
                                effect1=row[4]
                                effect2=row[5]#takes down the effects and criteria recquired for unlocking
                    #The below code checks if the criterion have been met
                    with open("saveData/researched.txt", "r") as fileOut:#file that saves the user's game
                        reader = csv.reader(fileOut)
                        for row in reader:
                            if row[0] == criterion1:#check if criterion 1 is fulfilled
                                if row[1] == "1":
                                    queryDrawButton = True
                                else:
                                    queryDrawButton = False
                                    break
                            if criterion2 != "0":#validate the existence of a second criterion
                                if row[0] == criterion2:#check if criterion 2 is fulfilled, if it exists
                                    if row[1] == "1":
                                        queryDrawButton = True
                                    else:
                                        queryDrawButton = False
                                        break
                            if row[0] == item[i]:
                                if row[1] == "0":#check if the item has already been unlocked
                                    queryDrawButton = True
                                    if criterion1 == criterion2:#checks if the item has no criteria for unlocking
                                        queryDrawButton = True
                                        break
                                else:
                                    queryDrawButton = False
                                    break
                   
            #will draw the button if the criteria is met
                if queryDrawButton:
                    if money >= cost:
                        unlockButton.drawButton()
                        pygame.display.update()#draw the button if there is enough money
                        if unlockButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                            unlockButton.changeButtonColour(menuScreenColour)#hover functionality
                            if event.type == pygame.MOUSEBUTTONUP:
                                for j in range (0,33):#updates the array which will be copied over to the list
                                    if researchProgress[j][0] == item[i]:
                                        researchProgress[j][1] = "1"#sets the appropriate element to unlocked
                                saveGame()
                                money = money - cost#deducts the cost of the technology
                                print(money)#more debugging
                                #apply effects
                                if effect1 == "IR":
                                    global incidentRecoverySpeed
                                    incidentRecoverySpeed = incidentRecoverySpeed/2 #increase the speed at which incidents are dealt with
                                elif effect1 == "5IR":
                                    global incidentRisk
                                    incidentRisk = 15 #reduce risk of an incident occuring by 50%
                                elif effect1 == "C":
                                    pass #This effect will be applied on the contract screen
                                else:
                                    global SPADRisk
                                    SPADRisk = SPADRisk - int(effect1) #decrease the risk of a SPAD
                                if effect2 == "SP":
                                    global signalPriceBoost
                                    signalPriceBoost = signalPriceBoost + 10 #increase the price of a signal
                                queryDrawButton = False
                                pygame.draw.rect(screen, black, [550, 375, 500, 50])
                        else:
                            unlockButton.changeButtonColour(darkGrey)

        research()

    #This will draw the tech tree for each category
    def drawTree(category):
        returnButton.changeButtonColour(darkGrey)


        
        #draws the tech tree based on which category has been selected
        #I have labelled the buttons based on what they will say, so it is pretty self- explanatory
        #There are two lists, one called items and the other item. Items is a list of button, item is a list of files
        if category == "facility":
            pygame.draw.rect(screen, black, [250, 0, 1030, 600])
            helpPoint = technoButton(darkGrey, [300, 50, 150, 50], "Help Points", normal, white, 325, 65)
            helpPoint.drawtechButton(100, 0)
            helpPatrol = technoButton(darkGrey, [550, 50, 150, 50], "Help patrol", normal, white, 575, 65)
            helpPatrol.drawtechButton(100, 0)
            bicycle = technoButton(darkGrey, [300, 150, 150, 50], "Bicycle racks", normal, white, 322, 165)
            bicycle.drawtechButton(100, -100)
            pAndR = technoButton(darkGrey, [550, 150, 150, 50], "Park and Ride", normal, white, 568, 165)
            pAndR.drawtechButton(100, 0)
            timeTable = technoButton(darkGrey, [300, 250, 150, 50], "TimeTables", normal, white, 327, 265)
            timeTable.drawtechButton(100, -200)
            DMI = technoButton(darkGrey, [550, 250, 150, 50], "DMIs", normal, white, 605, 265)
            DMI.drawtechButton(100, 0)
            LCD = technoButton(darkGrey, [800, 250, 150, 50], "LCDs", normal, white, 855, 265)
            LCD.drawtechButton(100, 0)
            toilet = technoButton(darkGrey, [300, 350, 150, 50], "toilets", normal, white, 347, 365)
            toilet.drawtechButton(100, -300)
            items = [helpPoint, helpPatrol, bicycle, pAndR, timeTable, DMI, LCD, toilet]
            item = ["helpPoint", "helperPatrol", "bike", "parkRide", "timetable", "DMI", "LCD", "toilet"]
            pygame.display.update()
        elif category == "signal":
            pygame.draw.rect(screen, black, [250, 0, 1030, 600])
            semaphore = technoButton(darkGrey, [250, 150, 150, 50], "semaphores", normal, white, 275, 165)
            semaphore.drawtechButton(50, 0)
            repeater = technoButton(darkGrey, [450, 150, 150, 50], "repeaters", normal, white, 485, 165)
            repeater.drawtechButton(50, 0)
            litSems = technoButton(darkGrey, [450, 250, 150, 50], "lit semaphores", normal, white, 465, 265)
            litSems.drawtechButton(50, -100)
            threeCols = technoButton(darkGrey, [650, 150, 150, 50], "3-aspect signals", normal, white, 658, 165)
            threeCols.drawtechButton(50, 0)
            threeCols.drawtechButton(50, 100)
            fourCols = technoButton(darkGrey, [850, 150, 150, 50], "4-aspect signals", normal, white, 860, 165)
            fourCols.drawtechButton(50, 0)
            TVM = technoButton(darkGrey, [1050, 250, 150, 50], "TVM-430", normal, white, 1090, 265)
            TVM.drawtechButton(50, -100)
            ETCS = technoButton(darkGrey, [1050, 150, 150, 50], "ETCS", normal, white, 1100, 165)
            ETCS.drawtechButton(50, 0)
            items = [semaphore, repeater, litSems, threeCols, fourCols, TVM, ETCS]
            item = ["semaphore", "repeater", "lit", "three", "four", "TVM", "ETCS"]
            pygame.display.update()
        elif category == "safety":
            pygame.draw.rect(screen, black, [250, 0, 1030, 600])
            tripCock = technoButton(darkGrey, [300, 250, 150, 50], "trip-cocks", normal, white, 335, 265)
            tripCock.drawtechButton(100, 0)
            AWS = technoButton(darkGrey, [550, 250, 150, 50], "AWS", normal, white, 605, 265)
            AWS.drawtechButton(100, 0)
            speedCamera = technoButton(darkGrey, [800, 250, 150, 50], "Speed Monitoring", normal, white, 803, 265)
            speedCamera.drawtechButton(100, 0)
            speedCamera.drawtechButton(100, 100)
            TPWS = technoButton(darkGrey, [550, 350, 150, 50], "TPWS", normal, white, 600, 365)
            TPWS.drawtechButton(100, -100)
            items = [tripCock, AWS, speedCamera, TPWS]
            item = ["tripCock", "AWS", "OTMR", "TPWS"]
            pygame.display.update()
        elif category == "comms":
            pygame.draw.rect(screen, black, [250, 0, 1030, 600])
            sigBoxBell = technoButton(darkGrey, [300, 350, 150, 50], "Signal box bell", normal, white, 315, 365)
            sigBoxBell.drawtechButton(100, 0)
            trackSidePhone = technoButton(darkGrey, [550, 350, 150, 50], "Track-side phones", normal, white, 552, 365)
            trackSidePhone.drawtechButton(100, 0)
            inCabPhone = technoButton(darkGrey, [800, 350, 150, 50], "In-Cab phones", normal, white, 815, 365)
            inCabPhone.drawtechButton(100, 0)
            GSMR = technoButton(darkGrey, [1050, 350, 150, 50], "GSM-R", normal, white, 1095, 365)
            GSMR.drawtechButton(100, 0)
            items = [sigBoxBell, trackSidePhone, inCabPhone, GSMR]
            item = ["sigBoxBell", "trackPhone", "cabPhone", "GSMR"]
            pygame.display.update()
        else:#this one is for the track - just to save memory
            pygame.draw.rect(screen, black, [250, 0, 1030, 600])
            threeRail = technoButton(darkGrey, [300, 450, 150, 50], "3rd Rail", normal, white, 342, 465)
            threeRail.drawtechButton(100, 0)
            OHLE = technoButton(darkGrey, [550, 450, 150, 50], "OHLE", normal, white, 600, 465)
            OHLE.drawtechButton(100, 0)
            OHLEspeed = technoButton(darkGrey, [800, 450, 150, 50], "High speed OHLE", normal, white, 804, 465)
            OHLEspeed.drawtechButton(100, 0)
            fourRail = technoButton(darkGrey, [800, 350, 150, 50], "4th Rail", normal, white, 842, 365)
            fourRail.drawtechButton(100, 100)
            flangeGreaser = technoButton(darkGrey, [300, 350, 150, 50], "flange-Greasers", normal, white, 311, 365)
            flangeGreaser.drawtechButton(100, 100)
            points = technoButton(darkGrey, [300, 250, 150, 50], "points", normal, white, 350, 265)
            points.drawtechButton(100, 200)
            checkRail = technoButton(darkGrey, [550, 250, 150, 50], "check-rails", normal, white, 580, 265)
            checkRail.drawtechButton(100, 0)
            welding = technoButton(darkGrey, [800, 250, 150, 50], "Welding", normal, white, 840, 265)
            welding.drawtechButton(100, 0)
            superElevate = technoButton(darkGrey, [1050, 250, 150, 50], "Super-elevation", normal, white, 1060, 265)
            superElevate.drawtechButton(100, 0)
            items = [threeRail, OHLE, OHLEspeed, fourRail, flangeGreaser, points, checkRail, welding, superElevate]
            item = ["thirdRail", "OHLE", "OHLE HS", "fourthRail", "greaser", "points", "checkRail", "welding", "superElevate"]
            pygame.display.update()
        returnButton.drawButton()
        #this is where we check whether the items are clicked
        waiting = True
        while waiting == True:
            for event in pygame.event.get():
                i = 0
                for i in range(len(items)):
                    if items[i].buttonCoords.collidepoint((pygame.mouse.get_pos())):
                        items[i].changeButtonColour(pink)#giving each button hover functionality
                        if event.type == pygame.MOUSEBUTTONUP:
                            waiting = False
                            drawFact(item,i)#call the drawFact function and break from the loop
                    elif returnButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                        returnButton.changeButtonColour(pink)
                        if event.type == pygame.MOUSEBUTTONUP:
                            waiting = False
                            research()#programmed return button
                    else:
                        items[i].changeButtonColour(darkGrey)
                        returnButton.changeButtonColour(menuScreenColour)
                if event.type == pygame.QUIT:
                    waiting = False
                    pygame.quit()
                    sys.exit()#This is the red X in the top right hand corner of the window
                
    
    #draws the initial screen for the research tab, drawing the buttons
    screen.fill(black)
    pygame.draw.rect(screen, darkGrey, [0, 620, 1280, 100])
    facility = button(darkGrey, [50, 50, 150, 50], "Station Facilities", normal, white, 55, 65)
    facility.drawButton()
    signal = button(darkGrey, [50, 150, 150, 50], "Signalling", normal, white, 80, 165)
    signal.drawButton()
    safety = button(darkGrey, [50, 250, 150, 50], "Safety systems", normal, white, 60, 265)
    safety.drawButton()
    comms = button(darkGrey, [50, 350, 150, 50], "Communications", normal, white, 55, 365)
    comms.drawButton()
    track = button(darkGrey, [50, 450, 150, 50], "Tracks", normal, white, 95, 465)
    track.drawButton()
    returnButton = button(menuScreenColour, [1200, 635, 75, 75], "", clockTextFont, white, 1210, 655)
    returnButton.drawButton()
    pygame.display.update()
    #now we check which button has been pressed
    waiting = True
    while waiting == True:
        for event in pygame.event.get():
            if facility.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                facility.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    #waiting = False
                    drawTree("facility")
            elif signal.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                signal.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    #waiting = False
                    drawTree("signal")
            elif safety.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                safety.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    #waiting = False
                    drawTree("safety")
            elif comms.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                comms.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    #waiting = False
                    drawTree("comms")
            elif track.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                track.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    #waiting=False
                    drawTree("t")
            elif returnButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                returnButton.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting=False
                    saveGame()                                
                    game()#copies the contents of the array to the text, and then returns to the game
            elif event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                sys.exit()
            else:
                facility.changeButtonColour(darkGrey)
                signal.changeButtonColour(darkGrey)
                safety.changeButtonColour(darkGrey)
                comms.changeButtonColour(darkGrey)
                track.changeButtonColour(darkGrey)
                returnButton.changeButtonColour(menuScreenColour)
    
def shop():
    #re-draw the bottom bar
    pygame.draw.rect(screen, menuScreenColour, [0, 620, 1280, 100])
    #re-draw the return button
    returnButton = button(darkGrey, [1200, 635, 75, 75], "", clockTextFont, white, 1210, 655)
    returnButton.drawButton()
    #construct new button objects
    #build track
    buyTrack = button(darkGrey, [10, 635, 100, 75], "Track", clockTextFont, white, 15, 655)
    buyTrack.drawButton()
    #build signals
    buySignal = button(darkGrey, [135, 635, 140, 75], "Signals", clockTextFont, white, 140, 655)
    buySignal.drawButton()
    #buld platforms
    buyPlatform = button(darkGrey, [300, 635, 175, 75], "Platforms", clockTextFont, white, 305, 655)
    buyPlatform.drawButton()
    #print it all on screen
    pygame.display.update()
    waiting = True
    #the rest of the function will wait for an input as to what the user wishes to buy
    while waiting:
        for event in pygame.event.get():
            if buyTrack.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                buyTrack.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    purchaseTrack(buyTrack, returnButton)
            elif buySignal.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                buySignal.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    purchaseSignal(returnButton)
            elif buyPlatform.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                buyPlatform.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    purchasePlatform()
            elif returnButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                returnButton.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    game()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                buyTrack.changeButtonColour(darkGrey)
                buySignal.changeButtonColour(darkGrey)
                buyPlatform.changeButtonColour(darkGrey)
                returnButton.changeButtonColour(darkGrey)

def purchaseTrack(buyTrack, returnButton):
    #The save grid will be 32x13 for track, with each square being 40x40
    #change the bottom bar with the relevant options
    pygame.draw.rect(screen, menuScreenColour, [0, 620, 1280, 100])
    buyTrack.drawButton()
    returnButton.drawButton()
    buyPoints = button(darkGrey, [135, 635, 120, 75], "Points", clockTextFont, white, 140, 655)
    buyPoints.drawButton()
    buyEntry = button(darkGrey, [275, 635, 130, 75],  "Entries", clockTextFont, white, 280, 655)
    buyEntry.drawButton()
    waiting = True
    #Again, the following will wait for the user to select an option form the bottom of the screen
    while waiting:
        for event in pygame.event.get():
            if buyTrack.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                buyTrack.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    #code for building track goes here
                    buildTrack(returnButton)
            elif buyPoints.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                buyPoints.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    #code for building points goes here
                    buildPoints(returnButton)
            elif buyEntry.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                buyEntry.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    #code for buying entry points
                    buildEntry(returnButton)
            elif returnButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                returnButton.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    shop()
            elif event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                sys.exit()
            else:
                buyTrack.changeButtonColour(darkGrey)
                buyPoints.changeButtonColour(darkGrey)
                buyEntry.changeButtonColour(darkGrey)
                returnButton.changeButtonColour(darkGrey)
                pygame.display.update()

def buildTrack(returnButton):
    global money # "money referenced before assignment"
    #cover up the other buttons
    pygame.draw.rect(screen, menuScreenColour, [135, 635, 300, 75])
    positionCoord = pygame.mouse.get_pos()# position of the mouse
    position = pygame.Rect((positionCoord[0]-(positionCoord[0]%40),positionCoord[1]-(positionCoord[1]%40)),(40,40))#location on the array
    notFinished = True
    #copy the contents of the TrackLayout file into an array for easier handling.
    with open ("saveData/tracksPlatforms.txt", "r") as fileOut:
        reader = csv.reader(fileOut)
        j=-1
        for row in reader:
            j += 1
            if j < 14:
                trackLayout[j] = row
    while notFinished:
        pygame.draw.rect(screen, white, position)
        #pygame.draw.rect(screen, white, [position[0]-(position[0]%40),position[1]-(position[1]%40),40,40])
        for event in pygame.event.get():
            positionCoord = pygame.mouse.get_pos() # variable stores the position of the mouse
            if positionCoord[1] > 139 and positionCoord[1] < 580 and positionCoord[0] > 39 and positionCoord[0] < 1240 and (positionCoord[0] < 540 or positionCoord[0] > 740):
                #the above line will check if the cursor is in a buildable area before moving the rectangle.
                oldPosition = pygame.Rect((positionCoord[0]-(positionCoord[0]%40),positionCoord[1]-(positionCoord[1]%40)),(40,40))
                positionCoord = pygame.mouse.get_pos()#new position of the mouse
                storeCoordx, storeCoordy = int(position[0]/40), int(position[1]/40)# stores the coordinates of the mouse against the .txt grid (idexed from 1
                pygame.draw.rect(screen, white, position) # draw a white box to show where the mouse is.
                pygame.display.update()
                if position.collidepoint((pygame.mouse.get_pos())) == False:#checks if the mouse has left the box
                    #replaces the white square with a track piece if there is meant to be one there
                    if trackLayout[storeCoordy-5][storeCoordx-1] == "1":
                        pygame.draw.rect(screen, black, position)
                        pygame.draw.line(screen, white, (position[0],position[1]+20),(position[0] + 40 , position[1] + 20))
                        pygame.display.update()
                    #replaces the white square with a blank piece if no track is meant to be there
                    elif trackLayout[storeCoordy-5][storeCoordx-1] == "0":
                        pygame.draw.rect(screen, black, position)
                        pygame.display.update()
                    #replaces the gold square with an upward pointing set of points if it is meant to be there
                    elif trackLayout[storeCoordy - 5][storeCoordx - 1] == "2":
                        pygame.draw.rect(screen, black, position)
                        pygame.draw.line(screen, gold, (position[0],position[1]+20),(position[0] + 40 , position[1] + 20))
                        pygame.draw.line(screen, gold, (position[0] + 20 , position[1]+20),(position[0] + 20 , position[1] - 0))
                        pygame.display.update()
                    #replaces the gold square with a downward pointing set of points if it is meant to be there
                    elif trackLayout[storeCoordy - 5][storeCoordx - 1] == "3":
                        pygame.draw.rect(screen, black, position)
                        pygame.draw.line(screen, gold, (position[0],position[1] + 20),(position[0] + 40 , position[1] + 20))
                        pygame.draw.line(screen, gold, (position[0] + 20,position[1] + 20),(position[0] + 20 , position[1] + 40))
                        pygame.display.update()
                    #replaces the square with a leftward set of signals
                    elif trackLayout[storeCoordy - 5][storeCoordx - 1] == "5":
                        #signals will be triangles
                        pygame.draw.rect(screen, black, position)
                        pygame.draw.line(screen, white, (position[0],position[1]+20),(position[0] + 40 , position[1] + 20))
                        pygame.draw.polygon(screen, red, ((position[0] + 13, position[1]),(position[0] + 40 , position[1] + 20),(position[0] + 13,position[1] + 40)))#This is a signal
                        pygame.display.update()
                    #replaces the train with a rightward set of signals
                    elif trackLayout[storeCoordy - 5][storeCoordx - 1] == "6":
                        pygame.draw.rect(screen, black, position)
                        pygame.draw.line(screen, white, (position[0], position[1] + 20), (position[0] + 40 , position[1] + 20))
                        pygame.draw.polygon(screen, red, ((position[0] + 27, position[1]),(position[0], position[1] + 20), (position[0] + 27,position[1] + 40)))
                        pygame.display.update()
                    position = pygame.Rect((positionCoord[0]-(positionCoord[0]%40),positionCoord[1]-(positionCoord[1]%40)),(40,40))
                print(storeCoordy) # DEBUG
                print(storeCoordx) # DEBUG
                if event.type == pygame.MOUSEBUTTONUP:#checks for a click
                    #condition if the square has a track in it already
                    if trackLayout[storeCoordy-5][storeCoordx-1] == "1":
                        trackLayout[storeCoordy-5][storeCoordx-1] = "0"
                        print(trackLayout) #DEBUG
                        money = money + 700 #You will not get a full refund for destroying track
                    #condition if the selected quare has no track in it already.
                    elif trackLayout[storeCoordy-5][storeCoordx-1] == "0":
                        trackLayout[storeCoordy-5][storeCoordx-1] = "1"
                        print(trackLayout) #DEBUG
                        money = money - 800 #costs 800 to build track
            #check for whether the return button was hovered over/clicked
            elif returnButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                returnButton.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    with open("saveData/tracksPlatforms.txt", "w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerows(trackLayout)
                    shop()
            else:
                returnButton.changeButtonColour(darkGrey)

#This will do the same thing as the buildTrack procedure, but is adapted for points
def buildPoints(returnButton):
    global money
    #cover up the other buttons
    pygame.draw.rect(screen, menuScreenColour, [0, 620, 125, 100])
    pygame.draw.rect(screen, menuScreenColour, [275, 635, 150, 75])
    positionCoord = pygame.mouse.get_pos()# position of the mouse
    position = pygame.Rect((positionCoord[0]-(positionCoord[0]%40),positionCoord[1]-(positionCoord[1]%40)),(40,40))#location on the array
    notFinished = True
    #copy the contents of the TrackLayout file into an array for easier handling.
    with open ("saveData/tracksPlatforms.txt", "r") as fileOut:
        reader = csv.reader(fileOut)
        j=-1
        for row in reader:
            j += 1
            if j < 14:
                trackLayout[j] = row
    while notFinished:
        pygame.draw.rect(screen, gold, position)
        for event in pygame.event.get():
            positionCoord = pygame.mouse.get_pos() # variable stores the position of the mouse
            if positionCoord[1] > 139 and positionCoord[1] < 580 and positionCoord[0] > 39 and positionCoord[0] < 1240 and (positionCoord[0] < 540 or positionCoord[0] > 740):
                #the above line will check if the cursor is in a buildable area before moving the rectangle.
                oldPosition = pygame.Rect((positionCoord[0]-(positionCoord[0]%40),positionCoord[1]-(positionCoord[1]%40)),(40,40))
                positionCoord = pygame.mouse.get_pos()#new position of the mouse
                storeCoordx, storeCoordy = int(position[0]/40), int(position[1]/40)# stores the coordinates of the mouse against the .txt grid (idexed from 1
                pygame.draw.rect(screen, gold, position) # draw a gold box to show where the mouse is.
                pygame.display.update()
                if position.collidepoint((pygame.mouse.get_pos())) == False:#checks if the mouse has left the box
                    #replaces the gold square with a track piece if there is meant to be one there
                    if trackLayout[storeCoordy-5][storeCoordx-1] == "1":
                        pygame.draw.rect(screen, black, position)
                        pygame.draw.line(screen, white, (position[0],position[1]+20),(position[0] + 40 , position[1] + 20))
                        pygame.display.update()
                    #replaces the gold square with a blank piece if no track is meant to be there
                    elif trackLayout[storeCoordy-5][storeCoordx-1] == "0":
                        pygame.draw.rect(screen, black, position)
                        pygame.display.update()
                    #replaces the gold square with an upward pointing set of points if it is meant to be there
                    elif trackLayout[storeCoordy - 5][storeCoordx - 1] == "2":
                        pygame.draw.rect(screen, black, position)
                        pygame.draw.line(screen, gold, (position[0],position[1]+20),(position[0] + 40 , position[1] + 20))
                        pygame.draw.line(screen, gold, (position[0] + 20 , position[1]+20),(position[0] + 20 , position[1] - 0))
                        pygame.display.update()
                    #replaces the gold square with a downward pointing set of points if it is meant to be there
                    elif trackLayout[storeCoordy - 5][storeCoordx - 1] == "3":
                        pygame.draw.rect(screen, black, position)
                        pygame.draw.line(screen, gold, (position[0],position[1] + 20),(position[0] + 40 , position[1] + 20))
                        pygame.draw.line(screen, gold, (position[0] + 20,position[1] + 20),(position[0] + 20 , position[1] + 40))
                        pygame.display.update()
                    #replaces the square with a leftward set of signals
                    elif trackLayout[storeCoordy - 5][storeCoordx - 1] == "5":
                        #signals will be triangles
                        pygame.draw.rect(screen, black, position)
                        pygame.draw.line(screen, white, (position[0],position[1]+20),(position[0] + 40 , position[1] + 20))
                        pygame.draw.polygon(screen, red, ((position[0] + 13, position[1]),(position[0] + 40 , position[1] + 20),(position[0] + 13,position[1] + 40)))#This is a signal
                        pygame.display.update()
                    #replaces the train with a rightward set of signals
                    elif trackLayout[storeCoordy - 5][storeCoordx - 1] == "6":
                        pygame.draw.rect(screen, black, position)
                        pygame.draw.line(screen, white, (position[0], position[1] + 20), (position[0] + 40 , position[1] + 20))
                        pygame.draw.polygon(screen, red, ((position[0] + 27, position[1]),(position[0], position[1] + 20), (position[0] + 27,position[1] + 40)))
                        pygame.display.update()
                    position = pygame.Rect((positionCoord[0]-(positionCoord[0]%40),positionCoord[1]-(positionCoord[1]%40)),(40,40))
                    
                print(storeCoordy) # DEBUG
                print(storeCoordx) # DEBUG
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:#checks for a left click
                    #condition if the square has a track in it already
                    if trackLayout[storeCoordy-5][storeCoordx-1] == "1" or trackLayout[storeCoordy-5][storeCoordx-1] == "3":
                        trackLayout[storeCoordy-5][storeCoordx-1] = "2"
                        print(trackLayout) #DEBUG
                        money = money + 900 #You will not get a full refund for destroying track
                    #condition if the selected quare has a set of points in it already
                    elif trackLayout[storeCoordy-5][storeCoordx-1] == "2":
                        trackLayout[storeCoordy-5][storeCoordx-1] = "1"
                        print(trackLayout) #DEBUG
                        money = money - 1000 #costs 1000 to build points
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3: #checks for a right click
                    #condition if the square has a track in it already
                    if trackLayout[storeCoordy-5][storeCoordx-1] == "1" or trackLayout[storeCoordy-5][storeCoordx-1] == "2":
                        trackLayout[storeCoordy-5][storeCoordx-1] = "3"
                        print(trackLayout) # DEBUG
                        money = money - 1000
                    #condition if the square has a set of points in it already
                    elif trackLayout[storeCoordy-5][storeCoordx-1] == "3":
                        trackLayout[storeCoordy-5][storeCoordx-1] = "1"
                        print(trackLayout) # DeBUG
                        money = money + 900
            #check for whether the return button was hovered over/clicked
            elif returnButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                returnButton.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    with open("saveData/tracksPlatforms.txt", "w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerows(trackLayout)
                    shop()
            else:
                returnButton.changeButtonColour(darkGrey)

def buildEntry(returnButton):
    global money
    global numberEntry
    #cover up the other buttons
    pygame.draw.rect(screen, menuScreenColour, [0, 620, 275, 100])
    notFinished = True
    #need to open the file for entry points
    with open("saveData/entryPoints.txt", "r", newline="") as file:
        reader = csv.reader(file)
        i = -1
        for row in reader:
            i += 1
            print(i)
            print(entryLayout)
            entryLayout[i] = row
            print(entryLayout)
    #need to create the buttons that will act as the buildable areas - for this, a subclass is needed.
    entryButton1 = entryButton(black, (0, 280, 40, 40), "", clockTextFont, black, 0, 0, 0, 0, entryLayout[0][0])
    entryButton1.drawButton()
    entryButton2 = entryButton(black, (0, 320, 40, 40), "", clockTextFont, black, 0, 0, 0, 1, entryLayout[1][0])
    entryButton2.drawButton()
    entryButton3 = entryButton(black, (0, 360, 40, 40), "", clockTextFont, black, 0, 0, 0, 2, entryLayout[2][0])
    entryButton3.drawButton()
    entryButton4 = entryButton(black, (0, 400, 40, 40), "", clockTextFont, black, 0, 0, 0, 3, entryLayout[3][0])
    entryButton4.drawButton()
    entryButton5 = entryButton(black, (1240, 280, 40, 40), "", clockTextFont, black, 0, 0, 1, 0, entryLayout[0][1])
    entryButton5.drawButton()
    entryButton6 = entryButton(black, (1240, 320, 40, 40), "", clockTextFont, black, 0, 0, 1, 1, entryLayout[1][1])
    entryButton6.drawButton()
    entryButton7 = entryButton(black, (1240, 360, 40, 40), "", clockTextFont, black, 0, 0, 1, 2, entryLayout[2][1])
    entryButton7.drawButton()
    entryButton8 = entryButton(black, (1240, 400, 40, 40), "", clockTextFont, black, 0, 0, 1, 3, entryLayout[3][1])
    entryButton8.drawButton()
    pygame.display.update()
    #need to chec whether the cursor is in the buildable area.
    while notFinished:
        for event in pygame.event.get():
            if entryButton1.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                entryButton1.changeButtonColour(menuScreenColour)
                if event.type == pygame.MOUSEBUTTONUP:
                    entryButton1.setState()
                    money = money - 2500
            elif entryButton2.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                entryButton2.changeButtonColour(menuScreenColour)
                if event.type == pygame.MOUSEBUTTONUP:
                    entryButton2.setState()
                    money = money - 2500
            elif entryButton3.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                entryButton3.changeButtonColour(menuScreenColour)
                if event.type == pygame.MOUSEBUTTONUP:
                    entryButton3.setState()
                    money = money - 2500
            elif entryButton4.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                entryButton4.changeButtonColour(menuScreenColour)
                if event.type == pygame.MOUSEBUTTONUP:
                    entryButton4.setState()
                    money = money - 2500
            elif entryButton5.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                entryButton5.changeButtonColour(menuScreenColour)
                if event.type == pygame.MOUSEBUTTONUP:
                    entryButton5.setState()
                    money = money - 2500
            elif entryButton6.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                entryButton6.changeButtonColour(menuScreenColour)
                if event.type == pygame.MOUSEBUTTONUP:
                    entryButton6.setState()
                    money = money - 2500
            elif entryButton7.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                entryButton7.changeButtonColour(menuScreenColour)
                if event.type == pygame.MOUSEBUTTONUP:
                    entryButton7.setState()
                    money = money - 2500
            elif entryButton8.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                entryButton8.changeButtonColour(menuScreenColour)
                if event.type == pygame.MOUSEBUTTONUP:
                    entryButton8.setState()
                    money = money - 2500
                #check for whether the return button was hovered over/clicked
            elif returnButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                returnButton.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    with open("saveData/entryPoints.txt", "w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerows(entryLayout)
                        numberEntry += 1
                    shop()
            else:
                returnButton.changeButtonColour(darkGrey)
                entryButton1.changeButtonColour(black)
                entryButton2.changeButtonColour(black)
                entryButton3.changeButtonColour(black)
                entryButton4.changeButtonColour(black)
                entryButton5.changeButtonColour(black)
                entryButton6.changeButtonColour(black)
                entryButton7.changeButtonColour(black)
                entryButton8.changeButtonColour(black)
                

def purchasePlatform():
    global money
    global platPrice
    global platCount
    if money < platPrice:
        print()#nothing will happen if you try and buy without enough funds
    else:
        #platforms will only be bought once there is track on wither side.
        #with open ("saveData/tracksPlatforms.txt", "r") as fileOut:
         #   reader = csv.reader(fileOut)
          #  j=-1
           # for row in reader:
            #    j += 1
             #   if j < 14:
              #      trackLayout[j] = row
        i = 0
        for i in range(len(trackLayout)):
            if trackLayout[i-2][17] != "0" and trackLayout[i-2][12] != "0" and trackLayout[i-2][15] == "0":
                trackLayout[i-2][15] = "4"
                money = money - platPrice
                platCount = platCount + 1#records the number of platforms in possesion
                platPrice = platPrice + 5000##increase price of a new platform by £5000
                break
        with open("saveData/tracksPlatforms.txt", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(trackLayout)
    drawPlatform()
    shop()

def drawPlatform(): #I will need to preset the location of platforms, and then show them when the user buys a platform. This will need to be done in several screens so it is best to do this in a function
        for i in range(len(trackLayout)):
            #column 16 of the array will hold where the platforms are.
            if trackLayout[i-2][15] == "4":# denotes platforms because 1, 2, 3, and 0 are taken by tracks, points, and gaps
                pygame.draw.rect(screen, darkGrey, [560, 110 + (40 * i), 160, 20])
                pygame.draw.line(screen, white, (560, 140 + (40 * i)),(720, 140 + (40 * i)))

def purchaseSignal(returnButton):
    global money
    #These will be 1-way signals - left and right click (for direction to point in)
    i = 0
    for i in range(len(trackLayout)):
        for j in range(len(trackLayout[i])):
            if trackLayout[i-2][j] == "1": # normal track
                pygame.draw.line(screen, white, ((40 * j) + 40, (140 + (40 * i))),((40 * j) + 80, (140 + (40 * i))))
            elif trackLayout[i-2][j] == "2": # upwards points
                pygame.draw.line(screen, gold, ((40 * j) + 40, (140 + (40 * i))),((40 * j) + 80, (140 + (40 * i))))
                pygame.draw.line(screen, gold, ((40 * j) + 60, (140 + (40 * i))),((40 * j) + 60, (120 + (40 * i))))
            elif trackLayout[i-2][j] == "3":#downwards points
                pygame.draw.line(screen, gold, ((40 * j) + 40, (140 + (40 * i))),((40 * j) + 80, (140 + (40 * i))))
                pygame.draw.line(screen, gold, ((40 * j) + 60, (140 + (40 * i))),((40 * j) + 60, (160 + (40 * i))))
    positionCoord = pygame.mouse.get_pos()# position of the mouse
    position = pygame.Rect((positionCoord[0]-(positionCoord[0]%40),positionCoord[1]-(positionCoord[1]%40)),(40,40))#location on the array
    notFinished = True
    while notFinished:
        pygame.draw.rect(screen, white, position)
        #pygame.draw.rect(screen, white, [position[0]-(position[0]%40),position[1]-(position[1]%40),40,40])
        for event in pygame.event.get():
            positionCoord = pygame.mouse.get_pos() # variable stores the position of the mouse
            if positionCoord[1] > 139 and positionCoord[1] < 580 and positionCoord[0] > 39 and positionCoord[0] < 1240 and (positionCoord[0] < 540 or positionCoord[0] > 740):
                #the above line will check if the cursor is in a buildable area before moving the rectangle.
                oldPosition = pygame.Rect((positionCoord[0]-(positionCoord[0]%40),positionCoord[1]-(positionCoord[1]%40)),(40,40))
                positionCoord = pygame.mouse.get_pos()#new position of the mouse
                storeCoordx, storeCoordy = int(position[0]/40), int(position[1]/40)# stores the coordinates of the mouse against the .txt grid (idexed from 1
                pygame.draw.rect(screen, white, position) # draw a white box to show where the mouse is.
                pygame.display.update()
                if position.collidepoint((pygame.mouse.get_pos())) == False:#checks if the mouse has left the box
                    #replaces the white square with a track piece if there is meant to be one there
                    if trackLayout[storeCoordy-5][storeCoordx-1] == "1":
                        pygame.draw.rect(screen, black, position)
                        pygame.draw.line(screen, white, (position[0],position[1]+20),(position[0] + 40 , position[1] + 20))
                        pygame.display.update()
                    #replaces the white square with a blank piece if no track is meant to be there
                    elif trackLayout[storeCoordy-5][storeCoordx-1] == "0":
                        pygame.draw.rect(screen, black, position)
                        pygame.display.update()
                    #replaces the gold square with an upward pointing set of points if it is meant to be there
                    elif trackLayout[storeCoordy - 5][storeCoordx - 1] == "2":
                        pygame.draw.rect(screen, black, position)
                        pygame.draw.line(screen, gold, (position[0],position[1]+20),(position[0] + 40 , position[1] + 20))
                        pygame.draw.line(screen, gold, (position[0] + 20 , position[1]+20),(position[0] + 20 , position[1] - 0))
                        pygame.display.update()
                    #replaces the gold square with a downward pointing set of points if it is meant to be there
                    elif trackLayout[storeCoordy - 5][storeCoordx - 1] == "3":
                        pygame.draw.rect(screen, black, position)
                        pygame.draw.line(screen, gold, (position[0],position[1] + 20),(position[0] + 40 , position[1] + 20))
                        pygame.draw.line(screen, gold, (position[0] + 20,position[1] + 20),(position[0] + 20 , position[1] + 40))
                        pygame.display.update()
                    #replaces the square with a leftward set of signals
                    elif trackLayout[storeCoordy - 5][storeCoordx - 1] == "5":
                        #signals will be triangles
                        pygame.draw.rect(screen, black, position)
                        pygame.draw.line(screen, white, (position[0],position[1]+20),(position[0] + 40 , position[1] + 20))
                        pygame.draw.polygon(screen, red, ((position[0] + 13, position[1]),(position[0] + 40 , position[1] + 20),(position[0] + 13,position[1] + 40)))#This is a signal
                        pygame.display.update()
                    #replaces the train with a rightward set of signals
                    elif trackLayout[storeCoordy - 5][storeCoordx - 1] == "6":
                        pygame.draw.rect(screen, black, position)
                        pygame.draw.line(screen, white, (position[0], position[1] + 20), (position[0] + 40 , position[1] + 20))
                        pygame.draw.polygon(screen, red, ((position[0] + 27, position[1]),(position[0], position[1] + 20), (position[0] + 27,position[1] + 40)))
                        pygame.display.update()
                    position = pygame.Rect((positionCoord[0]-(positionCoord[0]%40),positionCoord[1]-(positionCoord[1]%40)),(40,40))
                print(storeCoordy) # DEBUG
                print(storeCoordx) # DEBUG
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:#checks for a left click
                    #condition if the square has a signal in it already
                    if trackLayout[storeCoordy-5][storeCoordx-1] == "1" or trackLayout[storeCoordy-5][storeCoordx-1] == "6":
                        trackLayout[storeCoordy-5][storeCoordx-1] = "5"
                        print(trackLayout) #DEBUG
                        money = money + 600 #You will not get a full refund for destroying signal
                    #condition if the selected quare has a signal in it already
                    elif trackLayout[storeCoordy-5][storeCoordx-1] == "5":
                        trackLayout[storeCoordy-5][storeCoordx-1] = "1"
                        print(trackLayout) #DEBUG
                        money = money - 700 #costs 700 to build signal
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3: #checks for a right click
                    #condition if the square has a signal in it already
                    if trackLayout[storeCoordy-5][storeCoordx-1] == "1" or trackLayout[storeCoordy-5][storeCoordx-1] == "5":
                        trackLayout[storeCoordy-5][storeCoordx-1] = "6"
                        print(trackLayout) # DEBUG
                        money = money - 700
                    #condition if the square has a signal in it already
                    elif trackLayout[storeCoordy-5][storeCoordx-1] == "6":
                        trackLayout[storeCoordy-5][storeCoordx-1] = "1"
                        print(trackLayout) # DeBUG
                        money = money + 600
            #check for whether the return button was hovered over/clicked
            elif returnButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                returnButton.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    with open("saveData/tracksPlatforms.txt", "w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerows(trackLayout)
                    shop()
            else:
                returnButton.changeButtonColour(darkGrey)

#this function will be where the contracts can be bought.
def contracts(returnButton):
    pygame.draw.rect(screen, black, [0, 100, 1280, 520])  # fill screen
    northern = button(darkGrey, [40, 120, 390, 125], "North Trains", clockTextFont, white, 50, 130) # North Trains button
    southEastern = button(darkGrey, [440, 120, 390, 125], "East South Railway", clockTextFont, white, 450, 130) # East and South Railway button
    scotRail = button(darkGrey, [840, 120, 390, 125], "Country Rail", clockTextFont, white, 850, 130) # Country Rail button
    southern = button(darkGrey, [40, 260, 390, 125], "South Side Railway", clockTextFont, white, 50, 270) # South Side Railway button
    thamesLink = button(darkGrey, [440, 260, 390, 125], "RiverLink", clockTextFont, white, 450, 270) #  Riverlink button
    crossRail = button(darkGrey, [840, 260, 390, 125], "PlusRail", clockTextFont, white, 850, 270) # PlusRail button
    tube = button(darkGrey, [40, 400, 390, 125], "Underneath Line", clockTextFont, white, 50, 410) # underneath Line button
    SEHS = button(darkGrey, [840, 400, 390, 125], "First High Speed", clockTextFont, white, 850, 410) # First High Speed button
    #draw the buttons
    northern.drawButton()
    southEastern.drawButton()
    scotRail.drawButton()
    southern.drawButton()
    thamesLink.drawButton()
    crossRail.drawButton()
    tube.drawButton()
    SEHS.drawButton()
    pygame.display.update()#update screens.
    # list of all TOCs in game - just in case
    TOClist = [northern, southEastern, scotRail, southern, thamesLink, crossRail, tube, SEHS]
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if northern.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                northern.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    drawContracts("northern", returnButton)
            elif southEastern.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                southEastern.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    drawContracts("southEastern", returnButton)
            elif scotRail.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                scotRail.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    drawContracts("scotRail", returnButton)
            elif southern.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                southern.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    drawContracts("southern", returnButton)
            elif thamesLink.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                thamesLink.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    drawContracts("thamesLink", returnButton)
            elif crossRail.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                crossRail.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    drawContracts("crossRail", returnButton)
            elif tube.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                tube.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    drawContracts("tube", returnButton)
            elif SEHS.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                SEHS.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    drawContracts("SEHS", returnButton)
            elif returnButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                returnButton.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    game()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                i = 0 # decided to try something new here.
                for i in range(len(TOClist)):
                    TOClist[i].changeButtonColour(darkGrey)
                    returnButton.changeButtonColour(darkGrey)

#function to draw the contracts you can buy
def drawContracts(TOC, returnButton):
    global numberTrains
    contractsList = [] # the list that will contain the data
    pygame.draw.rect(screen, black, [0, 100, 1280, 520]) # cover screen
    with open("saveData/contracts/" + TOC + ".txt","r",newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            contractsList.append(row) # fill the list with the data
    i = 0
    if TOC == "northern":
        contract1 = button(darkGrey, [400, 250, 150, 50], "1 car, 2 tpd", normal, white, 425, 265)
        contract2 = button(darkGrey, [650, 250, 150, 50], "2 cars, 4 tpd", normal, white, 675, 265)
        contracts = [contract1, contract2]
        for i in range ( len ( contracts ) ):
            contracts[i].drawButton()
        pygame.display.update()
    elif TOC == "southEastern":
        contract1 = button(darkGrey, [50, 250, 150, 50], "2 cars, 2 tpd", normal, white, 75, 265)
        contract2 = button(darkGrey, [250, 250, 150, 50], "2 cars, 6 tpd", normal, white, 275, 265)
        contract2 = button(darkGrey, [450, 250, 150, 50], "3 cars, 12 tpd", normal, white, 475, 265)
        contract3 = button(darkGrey, [650, 250, 150, 50], "4 cars, 12 tpd", normal, white, 675, 265)
        contract4 = button(darkGrey, [850, 250, 150, 50], "6 cars, 24, tpd", normal, white, 875, 265)
        contract5 = button(darkGrey, [1050, 250, 150, 50], "7 cars, 48 tpd", normal, white, 1075, 265)
        contract6 = button(darkGrey, [250, 350, 150, 50], "3 cars, 4 tpd", normal, white, 275, 365)
        contract7 = button(darkGrey, [450, 350, 150, 50], "4 cars, 6 tpd", normal, white, 475, 365)
        contract8 = button(darkGrey, [650, 350, 150, 50], "6 cars, 12 tpd", normal, white, 675, 365)
        contract9 = button(darkGrey, [850, 350, 150, 50], "8 cars, 12 tpd", normal, white, 875, 365)
        contract10 = button(darkGrey, [1050, 350, 150, 50], "10 cars, 24 tpd", normal, white, 1075, 365)
        contracts = [contract1, contract2, contract3, contract4, contract5, contract6, contract7, contract8, contract9, contract10]
        for i in range ( len ( contracts ) ):
            contracts[i].drawButton()
        pygame.display.update()
    elif TOC == "scotRail":
        contract1 = button(darkGrey, [250, 250, 150, 50], "3 cars, 12 tpd", normal, white, 275, 265)
        contract2 = button(darkGrey, [450, 250, 150, 50], "4 cars, 12 tpd", normal, white, 475, 265)
        contract3 = button(darkGrey, [650, 250, 150, 50], "5 cars, 24 tpd", normal, white, 675, 265)
        contract4 = button(darkGrey, [850, 250, 150, 50], "8 cars, 48 tpd", normal, white, 875, 265)
        contract5 = button(darkGrey, [450, 350, 150, 50], "3 cars, 24 tpd", normal, white, 475, 365)
        contract6 = button(darkGrey, [650, 350, 150, 50], "4 cars, 48 tpd", normal, white, 675, 365)
        contract7 = button(darkGrey, [850, 350, 150, 50], "5 cars, 96 tpd", normal, white, 875, 365)
        contracts = [contract1, contract2, contract3, contract4, contract5, contract6, contract7]
        for i in range ( len ( contracts ) ):
            contracts[i].drawButton()
        pygame.display.update()
    elif TOC == "southern":
        contract1 = button(darkGrey, [150, 250, 150, 50], "4 cars, 24 tpd", normal, white, 175, 265)
        contract2 = button(darkGrey, [350, 250, 150, 50], "4 cars, 48, tpd", normal, white, 375, 265)
        contract3 = button(darkGrey, [550, 250, 150, 50], "8 cars, 36 tpd", normal, white, 575, 265)
        contract4 = button(darkGrey, [750, 250, 150, 50], "8 cars, 48 tpd", normal, white, 775, 265)
        contract5 = button(darkGrey, [950, 250, 150, 50], "12 cars, 48 tpd", normal, white, 975, 265)
        contracts = [contract1, contract2, contract3, contract4, contract5]
        for i in range ( len ( contracts ) ):
            contracts[i].drawButton()
        pygame.display.update()
    elif TOC == "thamesLink":
        contract1 = button(darkGrey, [400, 250, 150, 50], "8 cars, 24 tpd", normal, white, 425, 265)
        contract2 = button(darkGrey, [600, 250, 150, 50], "8 cars, 24 tpd", normal, white, 625, 265)
        contract3 = button(darkGrey, [800, 250, 150, 50], "12 cars, 96 tpd", normal, white, 825, 265)
        contracts = [contract1, contract2, contract3]
        for i in range ( len ( contracts ) ):
            contracts[i].drawButton()
        pygame.display.update()
    elif TOC == "crossRail":
        contract1 = button(darkGrey, [300, 250, 200, 50], "7 cars, 288 tpd", normal, white, 325, 265)
        contract2 = button(darkGrey, [550, 250, 200, 50], "9 cars, 576 tpd", normal, white, 575, 265)
        contract3 = button(darkGrey, [800, 250, 200, 50], "11 cars, 576 tpd", normal, white, 825, 265)
        contracts = [contract1, contract2, contract3]
        for i in range ( len ( contracts ) ):
            contracts[i].drawButton()
        pygame.display.update()
    elif TOC == "tube":
        contract1 = button(darkGrey, [520, 250, 200, 50], "7 cars, 576 tpd", normal, white, 545, 265)
        contracts = [contract1]
        for i in range ( len ( contracts ) ):
            contracts[i].drawButton()
        pygame.display.update()
    elif TOC == "SEHS":
        contract1 = button(darkGrey, [420, 250, 200, 50], "6 cars, 48 tpd", normal, white, 445, 265)
        contract2 = button(darkGrey, [670, 250, 200, 50], "12 cars, 48 tpd", normal, white, 695, 265)
        contracts = [contract1, contract2]
        for i in range ( len ( contracts ) ):
            contracts[i].drawButton()
        pygame.display.update()
    i = 0
    returnButton.drawButton()
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            for i in range(len(contracts)):
                if contracts[i].buttonCoords.collidepoint((pygame.mouse.get_pos())) and contractsList[i + 1][2] == "1":
                    contracts[i].changeButtonColour(pink)
                    if event.type == pygame.MOUSEBUTTONUP:
                         numberTrains = numberTrains + contractsList[i+1][1]
                         print(numberTrains)
                if contractsList[i + 1][2] == "0":
                    contracts[i].changeButtonColour(white)
                    returnButton.changeButtonColour(darkGrey)
                if contractsList[i+1][2] == "1":
                    contracts[i].changeButtonColour(darkGrey)
                    returnButton.changeButtonColour(darkGrey)
                if returnButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                    returnButton.changeButtonColour(pink)
                    if event.type == pygame.MOUSEBUTTONUP:
                        waiting = False
                        contracts()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                pygame.display.update()

def timetableScreen(returnButton):
    global numberTrains
    global timeHour
    global timeMinute
    global timeSecond
    global numberEntry
    global timetableArray
    remainingTrains = numberTrains    

    #from save get timetable
    i = 0
    with open("saveData/timetable.txt") as file:
        reader = csv.reader(file)
        for row in reader:
            timetableArray[i] = row
            i += 1

    #0 = locked
    #1 = train present
    
    #first clear the screen
    pygame.draw.rect(screen, black, [0, 100, 1280, 520])
    #Then make the time bar along the top
    pygame.draw.rect(screen, darkGrey, [0, 100, 1280, 64])
    for i in range(4, 24, 1):
        stringTime = str(i)
        write(str(stringTime + ":00"), normal, white, 10 + (64 * (i - 4)), 110)
        for j in range (4): # this draws the minimum increments that I shall allow.
            pygame.draw.line(screen, darkGrey, [5 + ((64 * (i - 4)) + (16 * j)), 164],[5 + ((64 * (i - 4)) + (16 * j)), 510])
        #then make the hour borders extend down
        pygame.draw.line(screen, white, [5 + (64 * (i - 4)), 100], [5 + (64 * (i - 4)), 510])
        #hours increments are 64 pixels apart
        for k in range(numberEntry + 1):
            pygame.draw.line(screen, white, [0, (164 + (k * 42))], [1280, (164 + (k * 42))])

    #now draw the placed services
    for i in range(0, len(timetableArray),1):
        for j in range(0, len(timetableArray[i]),1):
            if timetableArray[i][j] == "1":
                pygame.draw.rect(screen, white, [(j * 16) + 6, ((i + 4) * 42) - 3, 15, 41])
                remainingTrains = remainingTrains - 1
            else:
                pygame.draw.rect(screen, black, [(j * 16) + 6, ((i + 4) * 42) - 3, 15, 41])

        #quuarter-hour increments are 16 pixels apart and there are 80 slots per row
    pygame.display.update()
    #all increments are 42 pixels vertically
    
    #then define the placeable regions
    positionCoord = pygame.mouse.get_pos()# position of the mouse
    position = pygame.Rect(((positionCoord[0] + 6)-(positionCoord[0]%16),(positionCoord[1] - 3)-(positionCoord[1]%42)),(15,41))#location on the array
    storeCoordx, storeCoordy = 0, 0
    waiting = True
    while waiting:
        for event in pygame.event.get():
            positionCoord = pygame.mouse.get_pos() # variable stores the position of the mouse
            if positionCoord[1] > 164 and positionCoord[1] < (164 + (numberEntry * 42)) and positionCoord[0] > 4:
                #the above line will check if the cursor is in a buildable area before moving the rectangle.
                positionCoord = pygame.mouse.get_pos()#new position of the mouse
                pygame.draw.rect(screen, menuScreenColour, position) # draw a purple box to show where the mouse is.
                pygame.display.update()
                print(storeCoordy)
                print(storeCoordx)
                if position.collidepoint((pygame.mouse.get_pos())) == False:
                    if timetableArray[storeCoordy][storeCoordx] == "1":
                        pygame.draw.rect(screen, white, position)
                    else:
                        pygame.draw.rect(screen, black, position)
                    position = pygame.Rect(((positionCoord[0] + 6)-(positionCoord[0]%16),(positionCoord[1] - 3)-(positionCoord[1]%42)),(15,41))#location on the array
                    pygame.draw.rect(screen, menuScreenColour, position) # draw a purple box to show where the mouse is.
    #then make clicky functionality
                if event.type == pygame.MOUSEBUTTONUP:#checks for a click
                    if remainingTrains != 0 and timetableArray[storeCoordy][storeCoordx] == "0":
                        timetableArray[storeCoordy][storeCoordx] = "1"
                        remainingTrains = remainingTrains - 1
                    elif timetableArray[storeCoordy][storeCoordx] == "1":
                        timetableArray[storeCoordy][storeCoordx] = "0"
                        remainingTrains = remainingTrains + 1
                storeCoordx, storeCoordy = int((position[0]/16)), int((position[1]/42) - 3)# stores the coordinates of the mouse against the .txt grid ()

            if returnButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                returnButton.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    #save the game
                    with open("saveData/timetable.txt", "w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerows(timetableArray)
                    #return to previous screen
                    game()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                returnButton.changeButtonColour(darkGrey)
    #then make the rectangles draggable, snapping to coordinates
        #actually no, make it so that left click does place, and right click removes
    pygame.display.update()
    #then make the file to save it.
        
#new object for train
class train:
    #construct a train
    def __init__(self, colour, x, y, width, height, xDirection):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.train = pygame.Rect([x, y, width, height])
        self.xDirection = xDirection

    #draw the train
    def drawTrain(self):
        pygame.draw.rect(screen, self.colour, self.train)
        pygame.display.update()

    #move the train
    def moveTrain(self, moveX, moveY):
        #draw black rectangle over the existing train
        self.destroyTrain()
        #move the train
        self.train.move_ip(moveX, moveY)
        #change the variables so that they are remembered
        self.x = self.x + moveX
        self.y = self.y + moveY
        #draw the new train
        pygame.draw.rect(screen, self.colour, self.train)
        pygame.display.update()

    #destroy the trani
    def destroyTrain(self):
        #change rectangle colour to black
        pygame.draw.rect(screen, black, self.train)
        #replace track
        pygame.draw.line(screen, white, [self.x, self.y + (self.height/2)], [self.x + self.width, (self.y + self.height/2)])
        

    #pre-programmed approach control
    def approachPlat(self):
        #this will simulate the train slowing down
        for i in range(1, 245):
            self.moveTrain(self.xDirection,0)
            time.sleep(0.01)
        for i in range(245, 490):
            self.moveTrain(self.xDirection,0)
            time.sleep(0.02)
        for i in range(490,610):
            self.moveTrain(self.xDirection,0)
            time.sleep(0.03)

    #pre-programmed departure control
    def departPlat(self):
        #this will simulate the train speeding up
        for i in range(610,490, -1):
            self.moveTrain(self.xDirection,0)
            time.sleep(0.03)
        for i in range(490, 245,-1):
            self.moveTrain(self.xDirection,0)
            time.sleep(0.02)
        for i in range(245,1,-1):
            self.moveTrain(self.xDirection,0)
            time.sleep(0.01)

#This is our button object
class button:
    #this is how we construct a button with attributes
    def __init__(self, buttonColour, buttonPos, text, font, textColour, textx, texty):
        self.buttonColour = buttonColour
        self.buttonPos = buttonPos
        self.text=text
        self.font = font
        self.textColour = textColour
        self.textx = textx
        self.texty = texty
        self.buttonCoords = pygame.Rect(buttonPos)
        
    #We will need to draw the button so that it is visible
    def drawButton(self):
        #draw the rectangle
        pygame.draw.rect(screen, self.buttonColour, self.buttonPos)
        #write the text
        write(self.text, self.font, self.textColour, self.textx, self.texty)

    #This was irst used to change the colour of the butto when highlighted over it.
    def changeButtonColour(self, newColour):
        self.buttonColour = newColour
        self.drawButton()
        pygame.display.update()

#This class is a subclass of button and acts in the research category of buttons
class technoButton(button):

    
    #define a new drawButton to draw a line with it, with potential extra parameters
    def drawtechButton(self, xdisplacement, ydisplacement):
        #draw a rectangle
        pygame.draw.rect(screen, self.buttonColour, self.buttonPos)
        #write the text
        write(self.text, self.font, self.textColour, self.textx, self.texty)
        #Here we will draw the lines - this is where the extra arameters can be helpful
        if ydisplacement == 0:
            #draw a straight line back to the previous button
            pygame.draw.line(screen, white, [self.buttonPos[0] - xdisplacement, self.buttonPos[1] + ((self.buttonPos[3])/2)], [self.buttonPos[0], self.buttonPos[1] + ((self.buttonPos[3])/2)])
        else:
            #draw line from button to midway in the gap
            pygame.draw.line(screen, white, [self.buttonPos[0] - xdisplacement, self.buttonPos[1] +(self.buttonPos[3]/2) + ydisplacement], [self.buttonPos[0] - (xdisplacement/2), (self.buttonPos[1] + (self.buttonPos[3]/2)) + ydisplacement])
            #draw line from end of previous line to however far down the new button is
            pygame.draw.line(screen, white, [(self.buttonPos[0] - (xdisplacement/2)), self.buttonPos[1] + (self.buttonPos[3]/2)], [self.buttonPos[0] - (xdisplacement/2), self.buttonPos[1] + (self.buttonPos[3]/2) + ydisplacement])
            #draw line from end of previous line to new button
            pygame.draw.line(screen, white, [(self.buttonPos[0] - (xdisplacement/2)), self.buttonPos[1] + (self.buttonPos[3]/2)], [self.buttonPos[0], self.buttonPos[1] + (self.buttonPos[3]/2)])
        pygame.display.update()

#subclass of button and acts in the buildEntry subroutine, and represents the entry points 
class entryButton(button):
    #constructor
    def __init__(self, buttonColour, buttonPos, text, font, textColour, textx, texty, saveLocationx, saveLocationy, state):
        super().__init__(buttonColour, buttonPos, text, font, textColour, textx, texty)
        self.saveLocationx = saveLocationx # this is the x-coordinate of the save location
        self.saveLocationy = saveLocationy # this is the y-coordinate of the save location
        self.state = state # Boolean stores whether this has been unlocked or not.
    #we need to remove the text and replace it with lines. This will be done in a drawButton method
    def drawButton(self):
        #draw the rectangle
        pygame.draw.rect(screen, self.buttonColour, self.buttonPos)
        #draw the lines - we will need to add some attributes for the location of the button in the file. For this, we will need to make a new initialiser
        if self.state == "0":
            pygame.draw.line(screen, white, ((1240*self.saveLocationx),((300+(40*self.saveLocationy)))), (((1240*self.saveLocationx)+40),((300+(40*self.saveLocationy)))))
            pygame.draw.line(screen, black, (((1240*self.saveLocationx)+8),((300+(40*self.saveLocationy)))), (((1240*self.saveLocationx)+16),((300+(40*self.saveLocationy)))))
            pygame.draw.line(screen, black, (((1240*self.saveLocationx)+24),((300+(40*self.saveLocationy)))), (((1240*self.saveLocationx)+32),((300+(40*self.saveLocationy)))))
        else:
            pygame.draw.line(screen, white, ((1240*self.saveLocationx),((300+(40*self.saveLocationy)))), (((1240*self.saveLocationx)+40),((300+(40*self.saveLocationy)))))
    #we need to change changeButtonColour so that hovering is more intuitive - this will be done in a new changeButtonColour method
    #actually I don't think we do, we'll see.

    #we need to add a toggle state method, so we can change the state of the button. Actually no we don't because we needn't change it back to unbought
    def setState(self):
        self.state = "1"
        entryLayout[self.saveLocationy][self.saveLocationx] = self.state

# I will use this to increment the clock every second
class RepeatedTimer(): # https://stackoverflow.com/questions/474528/how-to-repeatedly-execute-a-function-every-x-seconds
  def __init__(self, interval, function):
    self._timer = None
    self.interval = interval
    self.function = function
    self.is_running = False
    self.next_call = time.time()
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function()

  def start(self):
    if not self.is_running:
      self.next_call += self.interval
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False
        
#will print text as the user wishes
def write(text, font, colour, xpos, ypos):
    font = font
    #create the text surface
    textSurface = font.render(text, True, colour)
    #transfer it to the screen
    screen.blit(textSurface, (xpos, ypos))

def saveGame():
    global researchProgress
    with open("saveData/researched.txt", "w", newline="") as fileOut:
        writer=csv.writer(fileOut)
        for a in range(1):
            for b in range(33):
                writer.writerow(researchProgress[b])


#This is where the game is executed
def gameLoop():
    running = True
    mainMenu()
    #this keeps the game alive
    while running:
        


        
        
        #will check if the program has been quit (necessary for pygame)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

money = 30000 #in pounds
incidentRecoverySpeed = 1 #as a mutiplier
SPADRisk = 85 #as a percentage
signalPriceBoost = 0 #as a percentage
incidentRisk = 65 #as a percentage
platPrice = 5000 #price of a new platform at the start of the game
platCount = 0
numberTrains = 0
timeHour = 4
timeMinute = 0
timeSecond = 0
numberEntry = 4

gameLoop()
