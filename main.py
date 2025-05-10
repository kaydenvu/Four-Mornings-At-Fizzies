import pygame, sys
import random as r
import os

from pygame.constants import KEYDOWN, K_a, K_d
#four mornings at fizzys
# create light buttons and update them properly
map = []
directions = ["up", "down", "left", "right"]

left_door_closed = False
right_door_closed = False
left_light_on = False
right_light_on = False

pygame.init()
screen_width = 1920 // 2
screen_height = 1080 // 2
screen = pygame.display.set_mode((screen_width, screen_height))
powerPercent = 100

pepsoImage = pygame.image.load("pepso.png")
fantaImage = pygame.image.load("fanta.png")
leftcloseoff = pygame.image.load("button stuffs/left door close, light off.png")
leftcloseon = pygame.image.load("button stuffs/left door close, light on.png")
leftopenoff = pygame.image.load("button stuffs/left door open, light off.png")
leftopenon = pygame.image.load("button stuffs/left door open, light on.png")
rightcloseoff = pygame.image.load("button stuffs/right door close, light off.png")
rightcloseon = pygame.image.load("button stuffs/right door close light on.png")
rightopenoff = pygame.image.load("button stuffs/right door open, light off.png")
rightopenon = pygame.image.load("button stuffs/right door open, light on.png")
backGround = pygame.image.load("fnaf background.png")
backGround = pygame.transform.scale(backGround, (screen_width * 1.4, screen_height))
energy1 = pygame.image.load("energybar/energy1.png")
energy2 = pygame.image.load("energybar/energy2.png")
energy3 = pygame.image.load("energybar/energy3.png")
energy4 = pygame.image.load("energybar/energy4.png")
energy5 = pygame.image.load("energybar/energy5.png")
energyBar = [energy1, energy2, energy3, energy4, energy5]
for i, image in enumerate(energyBar):
    energyBar[i] = pygame.transform.scale_by(image, (0.25, 0.25))
#pepsoImage = pygame.transform.scale_by(pepsoImage, (0.75, 0.75))
#create sprite group, update everything in sprite group in main loop
animatronics = pygame.sprite.Group()

def visualize():
    for row in map:
        for col in row:
            print(col, end = ' ')
        print()

def toggle_left_door(left_door_closed):
    if not left_door_closed and not map[4][1]:
        map[4][1] = 'XX'
        return True
    elif left_door_closed:
        map[4][1] = []
        return False
        
def toggle_right_door(right_door_closed):
    if not right_door_closed and not map[4][3]:
        map[4][3] = 'XX'
        return True
    elif right_door_closed:
        map[4][3] = []
        return False
def toggle_left_light(left_light_on):
    return not left_light_on
def toggle_right_light(right_light_on):
    return right_light_on

for i in range(5):
    map.append([[], [], [], [], []])

map[3][1] = 'XX'
map[3][2] = 'XX'
map[3][3] = 'XX'

route1 = [(), (), (), (), (), (), (), ()]
route2 = []

guardPOV = 0

def moveCam(xPos):
    mouseX = pygame.mouse.get_pos()[0]
    if mouseX >= 0.9 * screen_width and xPos > screen_width * -0.4 + 160:
        return -40
    if mouseX <= 0.1 * screen_width and xPos < 0:
        return 40
    return 0

def checkWall(x, y, newX, newY):
    return map[x+newX][y+newY] != 'XX'

class atron(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__(animatronics)
        self.x = x
        self.y = y
        self.name = name
        self.chance = 57
        self.timesincelastMOVE = 0
    def __repr__(self):
        return self.name
    def move(self):
        direction = r.choice(directions)
        if r.randint(0,100) < 100 - self.chance:
            return
        match direction:
            case "up":
                if self.y > 0 and checkWall(self.x, self.y, 0, -1):
                    map[self.x][self.y].remove(self)
                    self.y -= 1
                    map[self.x][self.y].append(self)
            case "down":
                if self.y < 4 and checkWall(self.x, self.y, 0, 1):
                    map[self.x][self.y].remove(self)
                    self.y += 1
                    map[self.x][self.y].append(self)
            case "left":
                if self.x > 0 and checkWall(self.x, self.y, -1, 0):
                    map[self.x][self.y].remove(self)
                    self.x -= 1
                    map[self.x][self.y].append(self)
            case "right":
                if self.x < 4 and checkWall(self.x, self.y, 1, 0):
                    map[self.x][self.y].remove(self)
                    self.x += 1
                    map[self.x][self.y].append(self)
    def update(self):
        curr_time = pygame.time.get_ticks()
        if curr_time - self.timesincelastMOVE >= 5000:
            self.timesincelastMOVE = pygame.time.get_ticks()
            self.move()
            if self.name == "f":
                self.move()
p = atron(0, 2, "p")
f = atron(0,2, "f")
map[4][2].append('G') 
map[p.x][p.y].append(p) 
map[f.x][f.y].append(f)
#p is for pepso
#f' #f is for fanti
#F # F is for fizzy
#c # c is for coca
#g #g is guard

class Button(pygame.sprite.Sprite): # make images an array, door adds + 1, lights adds +2
    mouseDown = False
    def __init__(self, size, pos, *images, action):
        self.size = size
        self.pos = pos
        self.images = images
        self.rect = self.images[0].get_rect(center = self.pos)
        self.rectTop = self.rect.copy()
        self.rectTop.height //= 2
        self.rectBottom = self.rectTop.copy()
        self.rectBottom.y += self.rectBottom.height
        self.toggleDoor = False
        self.toggleLight = False
        self.toggle = False
        self.action = action
    def buttonClicked(self):
        mousePos = pygame.mouse.get_pos()
        if self.rectTop.collidepoint(mousePos) and pygame.mouse.get_pressed()[0] and not Button.mouseDown:
            self.toggleDoor = not self.toggleDoor
            Button.mouseDown = True
            return True
        if self.rectBottom.collidepoint(mousePos) and pygame.mouse.get_pressed()[0] and not Button.mouseDown:
            self.toggleLight = not self.toggleLight
            Button.mouseDown = True
            return True
        return False
    def draw(self):
        idx = 0
        if self.toggleDoor:
            idx += 1
        if self.toggleLight:
            idx += 2
        screen.blit(self.images[idx], self.rect)
    def update(self):
        global left_door_closed, right_door_closed, powerPercent
        self.buttonClicked()
        if powerPercent == 0:
            self.toggleDoor = False
            self.toggleLight = False
        if self.action == "left":
            left_door_closed = toggle_left_door(not self.toggleDoor)
        if self.action == "right":
            right_door_closed = toggle_right_door(not self.toggleDoor)
        self.draw()
            

clock = pygame.time.Clock()
leftbutton = Button(1, (250, 250), leftopenoff, leftcloseoff, leftopenon, leftcloseon, action="left")
rightbutton = Button(1, (450, 250), rightopenoff, rightcloseoff, rightopenon, rightcloseon, action="right")


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def displayEnergySystem():
    global powerPercent
    energyUsage = 0
    if leftbutton.toggleLight:
         energyUsage += 1
    if leftbutton.toggleDoor:
         energyUsage += 1
    if rightbutton.toggleLight:
         energyUsage += 1
    if rightbutton.toggleDoor:
         energyUsage += 1
    drainEnergy(energyUsage)
    energyUI = energyBar[energyUsage]
    energyUIpos = energyUI.get_rect(topleft=(85, screen_height-50))
    screen.blit(energyUI, energyUIpos)
    displayText("PixelifySans-Regular.ttf", 25, "Usage: ", (0, screen_height-50), (255, 255, 255))
    displayText("PixelifySans-Regular.ttf", 25, "Power left: " + str(powerPercent)+"%", (0, screen_height-100), (255, 255, 255)) 

def displayText(font, fontSize, text, pos, color):
    textFont = pygame.font.Font(font, fontSize) 
    text = textFont.render(text, True, color)
    textPos = text.get_rect(topleft=pos)
    screen.blit(text, textPos)

def drainEnergy(energyUsage):
    global powerPercent, timeSinceDrain
    currTime = pygame.time.get_ticks()
    if currTime - timeSinceDrain >= 4000 - energyUsage * 500:
        timeSinceDrain = pygame.time.get_ticks()
        if powerPercent >= 1:
            powerPercent -= 1

timeSinceDrain = pygame.time.get_ticks()

while True:
    clock.tick(60)
    visualize()
    cls()
    #input()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP and Button.mouseDown:
            Button.mouseDown= False
            print("not clicked")
        if event.type == pygame.KEYDOWN:
            if event.key == K_a:
                left_door_closed = toggle_left_door(left_door_closed)
            if event.key == K_d:
                right_door_closed = toggle_right_door(right_door_closed)
            cls()
            visualize()
    animatronics.update()
    guardPOV += moveCam(guardPOV) 
    screen.blit(backGround, (guardPOV,0))
    screen.blit(pepsoImage, (screen_width//2, screen_height//2))
    displayEnergySystem()

    leftbutton.update()
    rightbutton.update()
    pygame.display.update()
        