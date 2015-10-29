__author__ = 'Alexa'

import time
import random

#import and start pygame
import pygame
pygame.init()

#define colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

#window variables in case of resizing
display_width = 800
display_height = 600

#define image of snake head
snakeHead = pygame.image.load('snakehead.png')
apple = pygame.image.load('apple.png')

#frames per second
fps = 15

#var to hold what direction snake is travelling
direction = "right"

#initialize font object - size 25
smallFont = pygame.font.SysFont("comicsansms", 25)
medFont = pygame.font.SysFont("comicsansms", 50)
largeFont = pygame.font.SysFont("comicsansms", 80)

def pause():

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen("Paused",
                          black,
                          -100,
                          size='large')
        message_to_screen("Press C to continue or Q to quit.",
                          black,
                          25,
                          "small")
        pygame.display.update()
        clock.tick(5)

#scoring function
def score(score):
    text = smallFont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [0,0])


#draw snake func
def snake(block_size, snakeList):

    if direction == "right":
        head = pygame.transform.rotate(snakeHead, 270)
    if direction == "left":
        head = pygame.transform.rotate(snakeHead, 90)
    if direction == "up":
        head = snakeHead
    if direction == "down":
        head = pygame.transform.rotate(snakeHead, 180)


    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))

    #dont use the last element because that is the snakehead
    for XnY in snakeList[:-1]:
     #coordinates = top left (x,y), width, height
     pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1], block_size,block_size])

# generates apple location
def randAppleGen():
    randAppleX = round(random.randrange(0, display_width-appleThickness))#/10.0) * 10.0
    randAppleY = round(random.randrange(0, display_height-appleThickness))#/10.0

    return randAppleX, randAppleY

# Centers text
def text_objects(text, color, size):
    if size == "small":
        textSurface = smallFont.render(text, True, color)
    elif size == "med":
        textSurface = medFont.render(text, True, color)
    elif size == "large":
        textSurface = largeFont.render(text, True, color)
    return textSurface, textSurface.get_rect()

# func to print to screen - takes message and color
def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurface, textRect = text_objects(msg, color, size)
    #true for anti-aliasing
    textRect.center = (display_width/2), (display_height/2)+y_displace
    gameDisplay.blit(textSurface, textRect)

#game intro
def game_intro():

    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen("Welcome to Slither",
                          green,
                          -100,
                          "large")
        message_to_screen("The objective of the game is to eat red apples",
                          black,
                          -30,
                          "small")
        message_to_screen("The more apples you eat, the longer you get.",
                          black,
                          10,
                          "small")
        message_to_screen("If you run into yourself or the edges, you die.",
                          black,
                          50,
                          "small")
        message_to_screen("Press C to play, P to pause, or Q to Quit.",
                          black,
                          180,
                          "small")

        pygame.display.update()
        clock.tick(5)

#main window display
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Slither")
icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)

#setting frames per second
clock = pygame.time.Clock()

block_size = 20
appleThickness = 25

def gameLoop():
    global direction
    direction = "right"

    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height/2 #head of snake
    lead_x_change = 10
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    randAppleX, randAppleY = randAppleGen()

    while not gameExit:

        while gameOver:
            gameDisplay.fill(white)
            message_to_screen("Game over.",
                              red,
                              -50,
                              size="large")
            message_to_screen("Press C to play again or Q to quit",
                              black,
                              50,
                              size="med")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_c:
                        gameLoop()
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                gameOver = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                    direction = "left"
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                    direction = "right"
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                    direction = "up"
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0
                    direction = "down"
                elif event.key == pygame.K_p:
                    pause()
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(white)

        #draw apple
        gameDisplay.blit(apple, (randAppleX, randAppleY))

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for segment in snakeList[:-1]:
            if segment == snakeHead:
                gameOver = True
        #call snake
        snake(block_size, snakeList)

        #render score
        score(snakeLength-1)

        #better way to draw rect for processing
        #gameDisplay.fill(red, rect=[200, 200, 50,50])
        pygame.display.update()


        if lead_x > randAppleX and lead_x <randAppleX+appleThickness or lead_x+block_size > randAppleX and lead_x+block_size < randAppleX+appleThickness:
                if lead_y > randAppleY and lead_y < randAppleY+appleThickness:
                    snakeLength += 1
                    randAppleX, randAppleY = randAppleGen()
                elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + appleThickness:
                    snakeLength += 1
                    randAppleX, randAppleY = randAppleGen()

        # basically a sleep function; arg is fps
        clock.tick(fps)


    pygame.quit()
    quit()

game_intro()
gameLoop()