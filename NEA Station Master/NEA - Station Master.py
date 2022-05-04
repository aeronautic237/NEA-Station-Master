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
    pauseClock = button(darkGrey, [840, 10, 75, 75], "", buttonFont, white, 850, 20)
    pauseIcon = pygame.image.load("pause_Icon.png")
    pauseIcon = pygame.transform.scale(pauseIcon, (70, 70))
    pauseClock.drawButton()
    screen.blit(pauseIcon, (842.5, 12.5))
    playClock = button(darkGrey, [920, 10, 75,75], "", buttonFont, white, 850, 20)
    playClockIcon = pygame.image.load("play_icon.png")
    playClockIcon = pygame.transform.scale(playClockIcon, (70, 70))
    playClock.drawButton()
    screen.blit(playClockIcon, (922.5, 12.5))
    clockX5 = button(darkGrey, [1000, 10, 75,75], "5x", clockTextFont, white, 1020, 30)
    clockX5.drawButton()
    clockX15 = button(darkGrey, [1080, 10, 75, 75], "15x", clockTextFont, white, 1090, 30)
    clockX15.drawButton()
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
            elif event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                sys.exit()
            else:
                menuButton.changeButtonColour(darkGrey)
    #train1 = train(white, 1230, 350, 50, 20, -1)
    #train1.drawTrain()
    #time.sleep(1)
    #train1.approachPlat()
    #time.sleep(5)
    #train1.departPlat()
    #train1.destroyTrain()
    #pygame.display.update()

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
