"""generates a pygame image of a tiling"""
import pygame
from random import randint


class Structure:
    def __init__(self, tier, refl):
        self.tier = tier
        self.x = 0
        self.y = 0
        self.rx = refl[0]
        self.ry = refl[1]
        self.colour = [randint(164,255), randint(164,255), randint(164,255)]

        self.image = pygame.transform.flip(self.image, self.rx, self.ry)

        w, h = self.image.get_size()
        for x in range(w):
            for y in range(h):
                a = self.image.get_at((x, y))[3]
                self.image.set_at((x, y), self.colour + [a])

    def draw(self, screen, x, y):
        #print(f"drawing tier {self.tier} {self.name} at ({x+self.x},{y+self.y}) flipped ({self.rx},{self.ry})")
        if self.tier > 0:
            for child in self.childs:
                child.draw(screen, x+self.x, y+self.y)
        else:
            screen.blit(self.image, (x+self.x, y+self.y))


class Rat(Structure):
    image = pygame.image.load("rat.png")
    name = "rat"
    def __init__(self, tier, refl):
        super().__init__(tier, refl)

        self.width = 8
        self.height = 4
        if self.tier > 0:
            self.badger = Badger(self.tier-1, (1-self.rx,self.ry))
            self.rat = Rat(self.tier-1, (self.rx,1-self.ry))

            if not self.rx:
                self.rat.x = self.badger.width - self.rat.width

            if self.ry:
                self.badger.y = 1
                if self.tier > 1:
                    self.badger.y = self.rat.badger.height
            else:
                self.rat.y = 1
                if self.tier > 1:
                    self.rat.y = self.badger.badger_a.height

            self.width = self.badger.width

            self.height = 5
            if self.tier > 1:
                self.height = self.badger.badger_a.height + self.rat.height

            self.childs = [self.badger, self.rat]


class Badger(Structure):
    image = pygame.image.load("badger.png")
    name = "badger"
    def __init__(self, tier, refl):
        super().__init__(tier, refl)

        self.width = 13
        self.height = 4
        if self.tier > 0:
            self.badger_a = Badger(self.tier-1, (1-self.rx,self.ry))
            self.badger_b = Badger(self.tier-1, (1-self.rx,1-self.ry))
            self.rat = Rat(self.tier-1, (self.rx,self.ry))

            if self.rx:
                self.badger_a.x = self.rat.width
            else:
                self.badger_b.x = self.rat.width
                self.rat.x = self.badger_a.width

            if self.ry:
                self.badger_a.y = 1
                self.rat.y = 1
                if self.tier > 1:
                    self.badger_a.y = self.badger_b.badger_a.height
                    self.rat.y = self.badger_b.badger_a.height
            else:
                self.badger_b.y = 1
                if self.tier > 1:
                    self.badger_b.y = self.badger_a.badger_a.height

            self.width = self.badger_a.width + self.rat.width

            self.height = 5
            if self.tier > 1:
                self.height = self.badger_a.badger_a.height + self.badger_b.height

            self.childs = [self.badger_a, self.badger_b, self.rat]

            if self.tier == 1:
                self.frog = Frog()
                self.frog.x = (11,6)[self.rx]
                self.frog.y = (2,-11)[self.ry]
                self.childs.append(self.frog)
            

class Frog(Structure):
    image = pygame.image.load("frog.png")
    name = "frog"
    def __init__(self):
        super().__init__(0, (0,0))

        self.width = 4
        self.height = 6




tiling = Rat(8, (0,0))

pygame.init()
#screen_size = (1920, 1080)
screen_size = (1280, 720)
screen = pygame.display.set_mode(screen_size)#, pygame.FULLSCREEN)

done = False

screen.fill((0,0,0))
tiling.draw(screen, 0, 0)
pygame.display.flip()

while not done:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True
