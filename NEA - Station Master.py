#Made by Saambavan Thambiayah

#imports the rather unecessary libraries(!)
import pygame
import sys
import time

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
    write("£ 0000", buttonFont, gold, 10, 10)
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

    

    def drawTree(category):
        returnButton.changeButtonColour(darkGrey)
        #This is where we will define the fact files


        
        #draws the tech tree based on which category has been selected.
        if category == "facility":
            pygame.draw.rect(screen, black, [250, 0, 1030, 600])
            helpPoint = button(darkGrey, [300, 50, 150, 50], "Help Points", normal, white, 325, 65)
            helpPoint.drawButton()
            helpPatrol = button(darkGrey, [550, 50, 150, 50], "Help patrol", normal, white, 575, 65)
            helpPatrol.drawButton()
            bicycle = button(darkGrey, [300, 150, 150, 50], "Bicycle racks", normal, white, 322, 165)
            bicycle.drawButton()
            pAndR = button(darkGrey, [550, 150, 150, 50], "Park and Ride", normal, white, 568, 165)
            pAndR.drawButton()
            timeTable = button(darkGrey, [300, 250, 150, 50], "TimeTables", normal, white, 327, 265)
            timeTable.drawButton()
            DMI = button(darkGrey, [550, 250, 150, 50], "DMIs", normal, white, 605, 265)
            DMI.drawButton()
            LCD = button(darkGrey, [800, 250, 150, 50], "LCDs", normal, white, 855, 265)
            LCD.drawButton()
            toilet = button(darkGrey, [300, 350, 150, 50], "toilets", normal, white, 347, 365)
            toilet.drawButton()
            items = [helpPoint, helpPatrol, bicycle, pAndR, timeTable, DMI, LCD, toilet]
            pygame.draw.line(screen, white, [200, 75], [300, 75])#line between facilities and help point
            pygame.draw.line(screen, white, [450, 75], [550, 75])#line between help point and help patrol
            pygame.draw.line(screen, white, [250, 75], [250, 375])#line between facilities and lower altitudes (the big one)
            pygame.draw.line(screen, white, [250, 175], [300, 175])#line between facilities and bicycles
            pygame.draw.line(screen, white, [450, 175], [550, 175])#line between bikes and park and ride
            pygame.draw.line(screen, white, [250, 275], [300, 275])#line between facilities and timetables
            pygame.draw.line(screen, white, [450, 275], [550, 275])#line between timetables and DMIs
            pygame.draw.line(screen, white, [700, 275], [800, 275])#line between DMIs and LCDs
            pygame.draw.line(screen, white, [250, 375], [300, 375])#line between facilities and toilets
            pygame.display.update()
        elif category == "signal":
            pygame.draw.rect(screen, black, [250, 0, 1030, 600])
            semaphore = button(darkGrey, [250, 150, 150, 50], "semaphores", normal, white, 275, 165)
            semaphore.drawButton()
            repeater = button(darkGrey, [450, 150, 150, 50], "repeaters", normal, white, 485, 165)
            repeater.drawButton()
            litSems = button(darkGrey, [450, 250, 150, 50], "lit semaphores", normal, white, 465, 265)
            litSems.drawButton()
            threeCols = button(darkGrey, [650, 150, 150, 50], "3-aspect signals", normal, white, 658, 165)
            threeCols.drawButton()
            fourCols = button(darkGrey, [850, 150, 150, 50], "4-aspect signals", normal, white, 860, 165)
            fourCols.drawButton()
            TVM = button(darkGrey, [1050, 250, 150, 50], "TVM-430", normal, white, 1090, 265)
            TVM.drawButton()
            ETCS = button(darkGrey, [1050, 150, 150, 50], "ETCS", normal, white, 1100, 165)
            ETCS.drawButton()
            items = [semaphore, repeater, litSems, threeCols, fourCols, TVM, ETCS]
            pygame.draw.line(screen, white, [200, 175], [250, 175])#line between signalling and semaphores
            pygame.draw.line(screen, white, [400, 175], [450, 175])#line between semaphores and repeaters
            pygame.draw.line(screen, white, [425, 175], [425, 275])#line to descend a level
            pygame.draw.line(screen, white, [425, 275], [450, 275])#line between semaphores and lit sems
            pygame.draw.line(screen, white, [600, 275], [625, 275])#line between lit sems and 3-aspects
            pygame.draw.line(screen, white, [625, 275], [625, 175])#line to ascend a level
            pygame.draw.line(screen, white, [600, 175], [650, 175])#line between repeaters and 3 aspects
            pygame.draw.line(screen, white, [800, 175], [850, 175])#line between 3-aspect and 4-aspect
            pygame.draw.line(screen, white, [1000, 175], [1050, 175])#line between 4-aspect and TVM-430
            pygame.draw.line(screen, white, [1025, 175], [1025, 275])#line to descend a level
            pygame.draw.line(screen, white, [1025, 275], [1050, 275])#line between 4-aspect and ETCS
            pygame.display.update()
        elif category == "safety":
            pygame.draw.rect(screen, black, [250, 0, 1030, 600])
            tripCock = button(darkGrey, [300, 250, 150, 50], "trip-cocks", normal, white, 335, 265)
            tripCock.drawButton()
            AWS = button(darkGrey, [550, 250, 150, 50], "AWS", normal, white, 605, 265)
            AWS.drawButton()
            speedCamera = button(darkGrey, [800, 250, 150, 50], "Speed Cameras", normal, white, 812, 265)
            speedCamera.drawButton()
            TPWS = button(darkGrey, [550, 350, 150, 50], "TPWS", normal, white, 600, 365)
            TPWS.drawButton()
            trackCircuit = button(darkGrey, [800, 350, 150, 50], "Track-Circuits", normal, white, 816, 365)
            trackCircuit.drawButton()
            items = [tripCock, AWS, speedCamera, TPWS, trackCircuit]
            pygame.draw.line(screen, white, [200, 275], [300, 275])#line between safety systems and tripcocks
            pygame.draw.line(screen, white, [450, 275], [550, 275])#line between tripcocks and AWS
            pygame.draw.line(screen, white, [500, 275], [500, 375])#line to descend a level
            pygame.draw.line(screen, white, [500, 375], [550, 375])#line between AWS and TPWS
            pygame.draw.line(screen, white, [700, 375], [800, 375])#line between TPWS and Speed cameras and track circuits
            pygame.draw.line(screen, white, [750, 375], [750, 275])#line to chenge 1 level
            pygame.draw.line(screen, white, [700, 275], [800, 275])#line between AWS and Speed cameras and track circuits
            pygame.display.update()
        elif category == "comms":
            pygame.draw.rect(screen, black, [250, 0, 1030, 600])
            sigBoxBell = button(darkGrey, [300, 350, 150, 50], "Signal box bell", normal, white, 315, 365)
            sigBoxBell.drawButton()
            trackSidePhone = button(darkGrey, [550, 350, 150, 50], "Track-side phones", normal, white, 552, 365)
            trackSidePhone.drawButton()
            inCabPhone = button(darkGrey, [800, 350, 150, 50], "In-Cab phones", normal, white, 815, 365)
            inCabPhone.drawButton()
            GSMR = button(darkGrey, [1050, 350, 150, 50], "GSM-R", normal, white, 1095, 365)
            GSMR.drawButton()
            items = [sigBoxBell, trackSidePhone, inCabPhone, GSMR]
            pygame.draw.line(screen, white, [200, 375], [300, 375])
            pygame.draw.line(screen, white, [450, 375], [550, 375])
            pygame.draw.line(screen, white, [700, 375], [800, 375])
            pygame.draw.line(screen, white, [950, 375], [1050, 375])#The line is just straight here
            pygame.display.update()
        else:#this one is for the track - just to save memory
            pygame.draw.rect(screen, black, [250, 0, 1030, 600])
            threeRail = button(darkGrey, [300, 450, 150, 50], "3rd Rail", normal, white, 342, 465)
            threeRail.drawButton()
            OHLE = button(darkGrey, [550, 450, 150, 50], "OHLE", normal, white, 600, 465)
            OHLE.drawButton()
            OHLEspeed = button(darkGrey, [800, 450, 150, 50], "High speed OHLE", normal, white, 804, 465)
            OHLEspeed.drawButton()
            fourRail = button(darkGrey, [800, 350, 150, 50], "4th Rail", normal, white, 842, 365)
            fourRail.drawButton()
            flangeGreaser = button(darkGrey, [300, 350, 150, 50], "flange-Greasers", normal, white, 311, 365)
            flangeGreaser.drawButton()
            points = button(darkGrey, [300, 250, 150, 50], "points", normal, white, 350, 265)
            points.drawButton()
            checkRail = button(darkGrey, [550, 250, 150, 50], "check-rails", normal, white, 580, 265)
            checkRail.drawButton()
            welding = button(darkGrey, [800, 250, 150, 50], "Welding", normal, white, 840, 265)
            welding.drawButton()
            superElevate = button(darkGrey, [1050, 250, 150, 50], "Super-elevation", normal, white, 1060, 265)
            superElevate.drawButton()
            items = [threeRail, OHLE, OHLEspeed, fourRail, flangeGreaser, points, checkRail, welding, superElevate]
            pygame.draw.line(screen, white, [200, 475], [300, 475])#line between tracks and 3rd rail
            pygame.draw.line(screen, white, [450, 475], [550, 475])#line between 3rd rail and OHLE
            pygame.draw.line(screen, white, [700, 475], [800, 475])#line between OHLE and OHLE HS
            pygame.draw.line(screen, white, [750, 475], [750, 375])#line to ascend a level
            pygame.draw.line(screen, white, [750, 375], [800, 375])#line between OHLE and 4th rail
            pygame.draw.line(screen, white, [250, 475], [250, 275])#line to scend up to 2 levels
            pygame.draw.line(screen, white, [250, 375], [300, 375])#line between tracks and flange-greasers
            pygame.draw.line(screen, white, [250, 275], [300, 275])#line between tracks and points
            pygame.draw.line(screen, white, [450, 275], [550, 275])#line between points and check rails
            pygame.draw.line(screen, white, [700, 275], [800, 275])#line between check rails and welded joints
            pygame.draw.line(screen, white, [950, 275], [1050, 275])#line between welded joints and super-elevation
            pygame.display.update()
        #this is where we check whether the items are clicked
        waiting = True
        while waiting == True:
            for event in pygame.event.get():
                i = 0
                for i in range(len(items)):
                    if items[i].buttonCoords.collidepoint((pygame.mouse.get_pos())):
                        items[i].changeButtonColour(pink)
                        #if event.type == pygame.MOUSEBUTTONUP:
                            #waiting = False
                        #insert the fact files here
                    else:
                        items[i].changeButtonColour(darkGrey)
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_BACKSPACE):
                        waiting == False
                        research()
                elif event.type == pygame.QUIT:
                    waiting = False
                    pygame.quit()
                    sys.exit()
                
    
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
