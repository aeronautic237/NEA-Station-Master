#Made by Saambavan Thambiayah

#imports the rather unecessary libraries(!)
import pygame
import sys
import time
import csv

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

#Our repository of fonts
title = pygame.font.SysFont("Sans-serif", 200)
buttonFont = pygame.font.SysFont("Sans-serif", 100)
clockTextFont = pygame.font.SysFont("Sans-serif",50)
clockFont = pygame.font.SysFont("Sans-serif",100)
normal = pygame.font.SysFont("Sans-serif", 25)
criteriaFont = pygame.font.SysFont("Sans-serif", 40)

#declaring the state of the game - may not be necessary
gamestate = "menu"


#defing the various functions of the game here
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
    #this is mainly for debugging purposes, may not be necessary in the final build
    print("Starting Game")
    gameState = "game"
    timestate = "paused"
    #this is where we draw the first part of the game
    #drawing the track and station to begin with
    screen.fill(black)
    pygame.draw.line(screen, white, [0,360],[1280,360])
    pygame.draw.rect(screen, darkGrey, [540, 300, 200, 50])
    #draw the top and bottom bar
    pygame.draw.rect(screen, menuScreenColour, [0, 0, 1280, 100])
    pygame.draw.rect(screen, menuScreenColour, [0, 620, 1280, 100])
    #add placeholders for the menu items
    #placeholder for money
    write("?? 0000", buttonFont, gold, 10, 10)
    #clock placeholder
    clockIcon = pygame.image.load("Clock_Icon.jpg")
    clockIcon = pygame.transform.scale(clockIcon, (75, 75))
    screen.blit(clockIcon, (420, 10))
    #placeholder to pause the clock
    pauseClock = button(darkGrey, [840, 10, 75, 75], "", buttonFont, white, 850, 20)
    pauseIcon = pygame.image.load("pause_Icon.png")
    pauseIcon = pygame.transform.scale(pauseIcon, (70, 70))
    pauseClock.drawButton()
    screen.blit(pauseIcon, (842.5, 12.5))
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
    write("00:00:00", clockFont, white, 510, 15)
    #RDButton
    RDButton = button(darkGrey, [10, 635, 75, 75], "R&D", clockTextFont, white, 10, 655)
    RDButton.drawButton()
    #buy things button
    constructButton = button(darkGrey, [110, 635, 75, 75], "", clockTextFont, white, 10, 10)
    constructButton.drawButton()
    #accepted and offered contracts
    contractButton = button(darkGrey, [210, 635, 75, 75], "", clockTextFont, white, 10, 10)
    contractButton.drawButton()
    #potential fact button
    factButton = button(darkGrey, [310, 635, 75, 75], "", clockTextFont, white, 10, 10)
    factButton.drawButton()
    #return to main menu button
    menuButton = button(pink, [1200, 635, 75, 75], "", clockTextFont, white, 1210, 655)
    menuButton.drawButton()
    pygame.display.update()
    #this is where we do the mechanics
    waiting = True
    while waiting == True:
        for event in pygame.event.get():
            if menuButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                menuButton.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    gamestate = "menu"
                    mainMenu()
            elif RDButton.buttonCoords.collidepoint((pygame.mouse.get_pos())):
                RDButton.changeButtonColour(pink)
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    research()
            elif event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                sys.exit()
            else:
                menuButton.changeButtonColour(darkGrey)
                RDButton.changeButtonColour(darkGrey)
    #train1 = train(white, 1230, 350, 50, 20, -1)
    #train1.drawTrain()
    #time.sleep(1)
    #train1.approachPlat()
    #time.sleep(5)
    #train1.departPlat()
    #train1.destroyTrain()
    #pygame.display.update()

def research():

    #This procedure will output an image (which is the format that the facts are in)
    #It should also show an unlock button if the criteria to unlock the technology are met, so that the user can unlock it if they want to
    def drawFact(item,i):
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
                    pass
                    with open("criteria/research.txt", "r") as fileOut:#file containing every research, their critaria, and their effects
                        reader=csv.reader(fileOut)
                        for row in reader:
                            if row[0]==str(item[i]):
                                criterion1=row[2]
                                criterion2=row[3]#takes down the criteria recquired for unlocking
                    #The below code checks if the criterion have been met
                    if criterion1 == criterion2:
                        queryDrawButton = True
                    else:
                        with open("saveData/researched.txt", "r") as fileOut:#file that saves the user's game
                            reader = csv.reader(fileOut)
                            for row in reader:
                                if row[0] == item[i]:#check if the item has already been unlocked
                                    if row[1] == "0":
                                        queryDrawButton == True
                                    else:
                                        queryDrawButton == False
                                if row[0] == criterion1:#check if criterion 1 is fulfilled
                                    if row[1] == "1":
                                        queryDrawButton == True
                                    else:
                                        queryDrawButton == False
                                        break
                                if criterion2 != "0":#validate the existence of a second criterion
                                    if row[0] == criterion2:#check if criterion 2 is fulfilled, if it exists
                                        if row[1] == "1":
                                            queryDrawButton == True
                                        else:
                                            queryDrawButton == False
                                            break
            #will draw the button if the criteria is met
            if queryDrawButton:
                unlockButton.drawButton()
                pygame.display.update()
                #Code below to be added later

                #if the button is hovered over:
                    #change button colour to pink
                    #if the button is clicked:
                        #set the sppropriate file field to 1
                        #deduct money
                        #apply effects
                        #break
                #else:
                    #return to dark grey button colour
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
                    game()
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


#will print text as the user wishes
def write(text, font, colour, xpos, ypos):
    font = font
    #create the text surface
    textSurface = font.render(text, True, colour)
    #transfer it to the screen
    screen.blit(textSurface, (xpos, ypos))


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

gameLoop()
